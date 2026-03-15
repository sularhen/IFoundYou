from __future__ import annotations

from typing import Any


def _line(label: str, value: Any) -> str:
    if value in (None, "", [], {}):
        value = "n/a"
    if isinstance(value, list):
        value = ", ".join(str(item) for item in value) if value else "n/a"
    return f"{label:<16} {value}"


def render_human_report(report: dict[str, Any]) -> str:
    target = report["target"]
    network = report["network"]
    location = report["location"]
    provider = report["provider"]
    ssl_info = report.get("ssl")
    risk = report["risk_flags"]

    sections = [
        "IFoundYou Report",
        "=" * 56,
        _line("Input", target["input"]),
        _line("Host", target["host"]),
        _line("Primary IP", network["primary_ip"]),
        _line("Reverse DNS", target["reverse_dns"]),
        _line("IPv4", network["ipv4"]),
        _line("IPv6", network["ipv6"]),
        "",
        "Location",
        "-" * 56,
        _line("Continent", location["continent"]),
        _line("Country", location["country"]),
        _line("Region", location["region"]),
        _line("City", location["city"]),
        _line("Postal", location["postal"]),
        _line("Timezone", location["timezone"]),
        _line("Local time", location["local_time"]),
        _line("OpenStreetMap", location["maps"]["openstreetmap"]),
        _line("Google Maps", location["maps"]["google_maps"]),
        "",
        "Provider",
        "-" * 56,
        _line("ISP", provider["isp"]),
        _line("Organization", provider["organization"]),
        _line("ASN", provider["asn"]),
        _line("Domain", provider["domain"]),
        "",
        "Signals",
        "-" * 56,
        _line("Proxy", risk["proxy"]),
        _line("VPN", risk["vpn"]),
        _line("Tor", risk["tor"]),
        _line("Hosting", risk["hosting"]),
    ]

    if ssl_info:
        sections.extend(
            [
                "",
                "TLS Certificate",
                "-" * 56,
                _line("Common Name", ssl_info["common_name"]),
                _line("Issuer", ssl_info["issuer"]),
                _line("Valid From", ssl_info["valid_from"]),
                _line("Valid To", ssl_info["valid_to"]),
                _line("SANs", ssl_info["subject_alt_names"]),
            ]
        )

    sections.extend(
        [
            "",
            _line("Generated", report["meta"]["generated_at_utc"]),
            _line("Source", report["meta"]["source"]),
        ]
    )
    return "\n".join(sections)


def render_markdown_report(report: dict[str, Any]) -> str:
    target = report["target"]
    network = report["network"]
    location = report["location"]
    provider = report["provider"]
    ssl_info = report.get("ssl")
    risk = report["risk_flags"]

    lines = [
        f"# IFoundYou report for `{target['input']}`",
        "",
        "## Target",
        f"- Host: `{target['host']}`",
        f"- Primary IP: `{network['primary_ip']}`",
        f"- Reverse DNS: `{target['reverse_dns'] or 'n/a'}`",
        "",
        "## Location",
        f"- Country: `{location['country'] or 'n/a'}`",
        f"- Region: `{location['region'] or 'n/a'}`",
        f"- City: `{location['city'] or 'n/a'}`",
        f"- Timezone: `{location['timezone'] or 'n/a'}`",
        f"- OpenStreetMap: {location['maps']['openstreetmap'] or 'n/a'}",
        "",
        "## Provider",
        f"- ISP: `{provider['isp'] or 'n/a'}`",
        f"- Organization: `{provider['organization'] or 'n/a'}`",
        f"- ASN: `{provider['asn'] or 'n/a'}`",
        "",
        "## Risk Signals",
        f"- Proxy: `{risk['proxy']}`",
        f"- VPN: `{risk['vpn']}`",
        f"- Tor: `{risk['tor']}`",
        f"- Hosting: `{risk['hosting']}`",
    ]

    if ssl_info:
        lines.extend(
            [
                "",
                "## TLS Certificate",
                f"- Common Name: `{ssl_info['common_name'] or 'n/a'}`",
                f"- Issuer: `{ssl_info['issuer'] or 'n/a'}`",
                f"- Valid To: `{ssl_info['valid_to'] or 'n/a'}`",
            ]
        )

    lines.extend(
        [
            "",
            f"_Generated at {report['meta']['generated_at_utc']}_",
        ]
    )
    return "\n".join(lines)

