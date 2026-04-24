#!/usr/bin/env python3
"""Pretty-print a company profile from siwuya-data, for Claude / human consumption.

Usage:
    python load_company.py <slug-or-ticker>
    python load_company.py --list
    python load_company.py example-company

Output is human-readable Markdown sent to stdout. Claude reads it and uses
it as research context; the script itself is dependency-light (PyYAML only).

This script is a convenience helper, not the public API. The real loader is
`integrity_framework/src/loader.py :: load_company_yaml`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Force UTF-8 stdout/stderr so emoji glyphs render on Windows GBK consoles.
# Same pattern as scripts/validate_company.py.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
COMPANIES_DIR = REPO_ROOT / "companies"


def _require_yaml():
    try:
        import yaml  # type: ignore
    except ImportError:
        sys.stderr.write("PyYAML not installed. Run: pip install pyyaml\n")
        sys.exit(2)
    return yaml


def _find_yaml(slug_or_ticker: str) -> Path | None:
    """Search companies/{us,hk,cn,_examples}/ for a matching file.

    Match strategy: file stem == slug, or YAML's identity.primary_ticker matches.
    """
    yaml = _require_yaml()
    candidates: list[Path] = []
    for sub in ("us", "hk", "cn", "_examples"):
        for f in (COMPANIES_DIR / sub).glob("*.yaml"):
            if f.stem == slug_or_ticker:
                return f
            candidates.append(f)

    needle = slug_or_ticker.upper()
    for f in candidates:
        try:
            with f.open("r", encoding="utf-8") as fh:
                d = yaml.safe_load(fh)
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        identity = d.get("identity") or {}
        if str(identity.get("primary_ticker", "")).upper() == needle:
            return f
        if str(identity.get("slug", "")) == slug_or_ticker:
            return f
    return None


def _list_all() -> int:
    yaml = _require_yaml()
    print(f"# Companies in {COMPANIES_DIR.relative_to(REPO_ROOT)}\n")
    seen = False
    for sub in ("us", "hk", "cn", "_examples"):
        files = sorted((COMPANIES_DIR / sub).glob("*.yaml"))
        if not files:
            continue
        seen = True
        print(f"## {sub.upper()}")
        for f in files:
            try:
                with f.open("r", encoding="utf-8") as fh:
                    d = yaml.safe_load(fh) or {}
            except Exception as e:
                print(f"- {f.stem} (parse error: {e})")
                continue
            identity = d.get("identity") or {}
            ticker = identity.get("primary_ticker", "?")
            name = identity.get("name_zh") or identity.get("name_en") or "?"
            print(f"- `{f.stem}` — {name} ({ticker})")
        print()
    if not seen:
        print("_(empty — community contributions welcome)_")
    return 0


def _print_company(path: Path) -> int:
    yaml = _require_yaml()
    with path.open("r", encoding="utf-8") as f:
        d = yaml.safe_load(f) or {}

    identity = d.get("identity") or {}
    print(f"# {identity.get('name_zh') or identity.get('name_en') or path.stem}")
    print()
    print(f"**ticker**: {identity.get('primary_ticker', '?')}")
    print(f"**slug**: {identity.get('slug', path.stem)}")
    print(f"**file**: `{path.relative_to(REPO_ROOT)}`")
    print()

    if d.get("_example"):
        print("> ⚠️ This is an EXAMPLE record (not a real company).")
        print()

    for section in (
        "classification", "segments", "business_model", "moat", "management",
        "integrity_tracking", "key_risks", "further_reading",
    ):
        if section not in d:
            continue
        print(f"## {section}\n")
        print("```yaml")
        print(yaml.safe_dump({section: d[section]}, allow_unicode=True, sort_keys=False).rstrip())
        print("```")
        print()

    print("---")
    print(
        "_Source: [siwuya-data](https://github.com/duwei1018/siwuya-data) · "
        "Not investment advice — see [DISCLAIMER](../../DISCLAIMER.md)._"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", help="slug or ticker to load")
    parser.add_argument("--list", action="store_true", help="list all available companies")
    args = parser.parse_args(argv)

    if args.list:
        return _list_all()
    if not args.target:
        parser.print_help()
        return 2

    path = _find_yaml(args.target)
    if path is None:
        sys.stderr.write(
            f"No company found for '{args.target}'. Try `--list` to see what's available.\n"
        )
        return 1
    return _print_company(path)


if __name__ == "__main__":
    sys.exit(main())
