from __future__ import annotations

import ipaddress
import json
import socket
import ssl
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


DEFAULT_HEADERS = {
    "User-Agent": "IFoundYou/2.0 (+https://github.com/sularhen/IFoundYou)"
}


class TargetInspectionError(RuntimeError):
    """Raised when an inspection cannot be completed."""


def fetch_json(url: str, timeout: float) -> dict[str, Any]:
    request = Request(url, headers=DEFAULT_HEADERS)
    try:
        with urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise TargetInspectionError(f"Remote service returned HTTP {exc.code} for {url}") from exc
    except URLError as exc:
        raise TargetInspectionError(f"Could not reach remote service for {url}: {exc.reason}") from exc
    except TimeoutError as exc:
        raise TargetInspectionError(f"Timed out while requesting {url}") from exc


def normalize_target(raw_target: str) -> dict[str, Any]:
    candidate = raw_target.strip()
    if not candidate:
        raise TargetInspectionError("Empty target.")

    if "://" in candidate:
        parsed = urlparse(candidate)
        host = parsed.hostname
        scheme = parsed.scheme
        port = parsed.port
    else:
        parsed = None
        host = candidate
        scheme = None
        port = None

    if not host:
        raise TargetInspectionError(f"Could not extract a host from {raw_target!r}.")

    try:
        ipaddress.ip_address(host)
        is_ip = True
    except ValueError:
        is_ip = False

    return {
        "raw": raw_target,
        "host": host,
        "scheme": scheme,
        "port": port,
        "is_ip": is_ip,
        "parsed": parsed.geturl() if parsed else None,
    }


def resolve_dns(host: str) -> dict[str, list[str]]:
    ipv4: set[str] = set()
    ipv6: set[str] = set()
    try:
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        return {"ipv4": [], "ipv6": []}

    for family, _, _, _, sockaddr in infos:
        if family == socket.AF_INET:
            ipv4.add(sockaddr[0])
        elif family == socket.AF_INET6:
            ipv6.add(sockaddr[0])

    return {"ipv4": sorted(ipv4), "ipv6": sorted(ipv6)}


def reverse_dns(ip: str) -> str | None:
    try:
        host, _, _ = socket.gethostbyaddr(ip)
        return host
    except (socket.herror, socket.gaierror, OSError):
        return None


def fetch_geodata(query: str, timeout: float) -> dict[str, Any]:
    data = fetch_json(f"https://ipwho.is/{query}", timeout=timeout)
    if not data.get("success", False):
        message = data.get("message", "Unknown lookup failure")
        raise TargetInspectionError(f"Lookup failed for {query}: {message}")
    return data


def fetch_public_ip(timeout: float) -> str:
    data = fetch_json("https://api.ipify.org?format=json", timeout=timeout)
    ip = data.get("ip")
    if not ip:
        raise TargetInspectionError("The public IP service did not return an IP address.")
    return ip


def inspect_ssl_certificate(host: str, port: int, timeout: float) -> dict[str, Any] | None:
    context = ssl.create_default_context()
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=host) as wrapped:
                cert = wrapped.getpeercert()
    except OSError:
        return None
    except ssl.SSLError:
        return None

    subject = dict(x[0] for x in cert.get("subject", []))
    issuer = dict(x[0] for x in cert.get("issuer", []))
    san = [entry[1] for entry in cert.get("subjectAltName", []) if entry[0] == "DNS"]
    return {
        "common_name": subject.get("commonName"),
        "issuer": issuer.get("commonName"),
        "valid_from": cert.get("notBefore"),
        "valid_to": cert.get("notAfter"),
        "subject_alt_names": san[:10],
    }


def build_report(target_data: dict[str, Any], geo: dict[str, Any], dns: dict[str, list[str]], ssl_info: dict[str, Any] | None) -> dict[str, Any]:
    resolved_ips = dns["ipv4"] + dns["ipv6"]
    primary_ip = geo.get("ip") or (resolved_ips[0] if resolved_ips else target_data["host"])
    lat = geo.get("latitude")
    lon = geo.get("longitude")
    connection = geo.get("connection") or {}
    timezone = geo.get("timezone") or {}

    return {
        "target": {
            "input": target_data["raw"],
            "host": target_data["host"],
            "scheme": target_data["scheme"],
            "port": target_data["port"],
            "is_ip": target_data["is_ip"],
            "reverse_dns": reverse_dns(primary_ip) if primary_ip else None,
        },
        "network": {
            "primary_ip": primary_ip,
            "ipv4": dns["ipv4"],
            "ipv6": dns["ipv6"],
            "type": geo.get("type"),
        },
        "location": {
            "continent": geo.get("continent"),
            "country": geo.get("country"),
            "region": geo.get("region"),
            "city": geo.get("city"),
            "postal": geo.get("postal"),
            "latitude": lat,
            "longitude": lon,
            "timezone": timezone.get("id"),
            "local_time": timezone.get("current_time"),
            "maps": {
                "openstreetmap": f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=9/{lat}/{lon}" if lat and lon else None,
                "google_maps": f"https://www.google.com/maps/search/?api=1&query={lat},{lon}" if lat and lon else None,
            },
        },
        "provider": {
            "isp": connection.get("isp"),
            "organization": connection.get("org"),
            "asn": connection.get("asn"),
            "domain": connection.get("domain"),
        },
        "risk_flags": {
            "proxy": geo.get("security", {}).get("proxy"),
            "vpn": geo.get("security", {}).get("vpn"),
            "tor": geo.get("security", {}).get("tor"),
            "hosting": connection.get("type") == "hosting",
        },
        "ssl": ssl_info,
        "meta": {
            "generated_at_utc": datetime.now(UTC).isoformat(),
            "source": "ipwho.is + local DNS/SSL inspection",
        },
    }


def inspect_target(raw_target: str, timeout: float = 6.0, include_ssl: bool = True) -> dict[str, Any]:
    target = normalize_target(raw_target)
    dns = resolve_dns(target["host"])
    resolved_ips = dns["ipv4"] + dns["ipv6"]
    query = target["host"] if target["is_ip"] else (resolved_ips[0] if resolved_ips else None)
    if not query:
        raise TargetInspectionError(f"Could not resolve {target['host']} to an IP address.")
    geo = fetch_geodata(query, timeout=timeout)

    ssl_info = None
    if include_ssl and not target["is_ip"]:
        port = target["port"] or (443 if target["scheme"] in {None, "https"} else 443)
        ssl_info = inspect_ssl_certificate(target["host"], port, timeout=timeout)

    return build_report(target, geo, dns, ssl_info)


def inspect_public_ip(timeout: float = 6.0, include_ssl: bool = False) -> dict[str, Any]:
    ip = fetch_public_ip(timeout=timeout)
    return inspect_target(ip, timeout=timeout, include_ssl=include_ssl)


def inspect_batch(path: Path, timeout: float = 6.0, include_ssl: bool = True) -> list[dict[str, Any]]:
    if not path.exists():
        raise TargetInspectionError(f"Batch file not found: {path}")

    targets = [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not targets:
        raise TargetInspectionError(f"No targets found in {path}")

    return [inspect_target(target, timeout=timeout, include_ssl=include_ssl) for target in targets]
