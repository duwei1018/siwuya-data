#!/usr/bin/env python3
"""
Validate one or more company-profile YAML files against company.schema.json.

Usage:
    python scripts/validate_company.py companies/us/AAPL.yaml
    python scripts/validate_company.py companies/us/*.yaml
    python scripts/validate_company.py --all
    python scripts/validate_company.py --all --quiet

Exit codes:
    0 = all files valid
    1 = at least one file failed validation
    2 = environment problem (missing dep / file not found)

Dependencies:
    pip install pyyaml jsonschema
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

# Force UTF-8 stdout/stderr so emoji glyphs render on Windows GBK consoles.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "companies" / "_schema" / "company.schema.json"


def load_yaml(path: Path) -> object:
    try:
        import yaml  # type: ignore
    except ImportError:
        sys.stderr.write(
            "ERROR: pyyaml not installed. Run: pip install pyyaml jsonschema\n"
        )
        sys.exit(2)
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_schema() -> dict:
    if not SCHEMA_PATH.exists():
        sys.stderr.write(f"ERROR: schema not found at {SCHEMA_PATH}\n")
        sys.exit(2)
    with SCHEMA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def discover_company_files(include_examples: bool) -> list[Path]:
    """Find all *.yaml files under companies/{us,hk,cn}/ and optionally _examples/."""
    files: list[Path] = []
    for market in ("us", "hk", "cn"):
        files.extend(sorted((REPO_ROOT / "companies" / market).glob("*.yaml")))
    if include_examples:
        files.extend(sorted((REPO_ROOT / "companies" / "_examples").glob("*.yaml")))
        files.extend(sorted((REPO_ROOT / "companies" / "_schema").glob("*.example.yaml")))
    return files


def validate_one(path: Path, validator) -> tuple[bool, list[str]]:
    try:
        data = load_yaml(path)
    except Exception as e:
        return False, [f"YAML parse error: {e}"]
    if data is None:
        return False, ["YAML parsed to None (empty file?)"]
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path))
    if not errors:
        return True, []
    msgs = []
    for err in errors:
        path_str = "/".join(str(p) for p in err.absolute_path) or "<root>"
        msgs.append(f"  [{path_str}] {err.message}")
    return False, msgs


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "files",
        nargs="*",
        help="YAML files to validate (omit + --all to validate everything)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="validate every *.yaml under companies/{us,hk,cn,_examples,_schema}",
    )
    parser.add_argument(
        "--include-examples",
        action="store_true",
        help="include _examples/ + _schema/*.example.yaml in --all (default: off)",
    )
    parser.add_argument("--quiet", "-q", action="store_true", help="only print failures")
    args = parser.parse_args(argv)

    try:
        from jsonschema import Draft202012Validator  # type: ignore
    except ImportError:
        sys.stderr.write(
            "ERROR: jsonschema not installed. Run: pip install pyyaml jsonschema\n"
        )
        return 2

    schema = load_schema()
    validator = Draft202012Validator(schema)

    if args.all:
        targets = discover_company_files(include_examples=args.include_examples)
    else:
        targets = [Path(p) for p in args.files]

    if not targets:
        sys.stderr.write(
            "ERROR: no targets. Pass file paths or --all.\n"
        )
        return 2

    pass_count = 0
    fail_count = 0
    for path in targets:
        if not path.exists():
            sys.stderr.write(f"❌ {path} — file not found\n")
            fail_count += 1
            continue
        ok, errs = validate_one(path, validator)
        if ok:
            pass_count += 1
            if not args.quiet:
                print(f"✅ {path.relative_to(REPO_ROOT)} — schema valid")
        else:
            fail_count += 1
            print(f"❌ {path.relative_to(REPO_ROOT)} — {len(errs)} error(s):")
            for e in errs:
                print(e)

    if not args.quiet:
        print(f"\nSummary: {pass_count} passed, {fail_count} failed")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
