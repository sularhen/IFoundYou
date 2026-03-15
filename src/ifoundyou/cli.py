from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ifoundyou.core import TargetInspectionError, inspect_batch, inspect_public_ip, inspect_target
from ifoundyou.formatters import render_human_report, render_markdown_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ifoundyou",
        description="Inspect an IP, domain or URL with DNS, location and SSL context.",
    )
    parser.add_argument("target", nargs="?", help="IP, domain or full URL to inspect")
    parser.add_argument(
        "--self",
        action="store_true",
        dest="inspect_self",
        help="Inspect your current public IP instead of a target",
    )
    parser.add_argument(
        "--batch",
        type=Path,
        help="Read one target per line from a text file",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON",
    )
    parser.add_argument(
        "--save",
        type=Path,
        help="Save the report to .json or .md",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=6.0,
        help="Network timeout in seconds (default: 6)",
    )
    parser.add_argument(
        "--no-ssl",
        action="store_true",
        help="Skip SSL certificate inspection",
    )
    return parser


def _write_report(path: Path, inspections: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix.lower() == ".json":
        path.write_text(json.dumps(inspections, indent=2, ensure_ascii=False), encoding="utf-8")
        return

    if path.suffix.lower() in {".md", ".markdown"}:
        content = "\n\n".join(render_markdown_report(item) for item in inspections)
        path.write_text(content + "\n", encoding="utf-8")
        return

    raise TargetInspectionError("Use .json or .md when saving a report.")


def _print_output(inspections: list[dict], as_json: bool) -> None:
    if as_json:
        json.dump(inspections if len(inspections) > 1 else inspections[0], sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")
        return

    for index, item in enumerate(inspections):
        if index:
            print()
        print(render_human_report(item))


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.batch:
            inspections = inspect_batch(args.batch, timeout=args.timeout, include_ssl=not args.no_ssl)
        elif args.inspect_self:
            inspections = [inspect_public_ip(timeout=args.timeout, include_ssl=False)]
        elif args.target:
            inspections = [inspect_target(args.target, timeout=args.timeout, include_ssl=not args.no_ssl)]
        else:
            parser.error("Provide a target, --batch, or --self.")

        _print_output(inspections, as_json=args.json)

        if args.save:
            _write_report(args.save, inspections)
            if not args.json:
                print(f"\nSaved report to {args.save}")
        return 0
    except KeyboardInterrupt:
        print("Interrupted by user.", file=sys.stderr)
        return 130
    except TargetInspectionError as exc:
        print(f"ifoundyou: {exc}", file=sys.stderr)
        return 1

