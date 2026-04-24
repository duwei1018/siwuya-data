"""Tests for YAML ↔ dataclass loaders.

Coverage: loading promises from the existing EXAMPLE company yaml
(round-trip fidelity), parsing a sidecar verdicts yaml, and rejecting
malformed input shapes.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
import yaml

from integrity_framework.src.loader import (
    load_company_yaml,
    load_promises_from_company_yaml,
    load_verdicts_yaml,
)


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
EXAMPLE_PATH = REPO_ROOT / "companies" / "_examples" / "example-company.yaml"


def test_example_company_yaml_loads():
    data = load_company_yaml(EXAMPLE_PATH)
    assert isinstance(data, dict)
    assert "integrity_tracking" in data


def test_example_promises_load_and_validate():
    promises = load_promises_from_company_yaml(EXAMPLE_PATH)
    assert len(promises) >= 1
    for p in promises:
        assert p.id
        assert p.promise_zh
        assert p.source
        assert p.verification_type in (
            "financial_metric",
            "product_launch",
            "strategic_initiative",
            "ESG_target",
            "other",
        )


def test_subject_ticker_pulled_from_identity_when_present():
    promises = load_promises_from_company_yaml(EXAMPLE_PATH)
    # EXAMPLE company has identity.primary_ticker = "EXAMPLE.US"
    assert all(p.subject_ticker == "EXAMPLE.US" for p in promises)


def test_load_verdicts_yaml_round_trip(tmp_path):
    sample = {
        "verdicts": [
            {
                "promise_id": "fy24-revenue-25pct",
                "outcome": "broken",
                "reasoning": "FY24 +18%, missed guidance by 7pp.",
                "judged_at": date(2025, 4, 30),
                "judged_by": "@analyst-handle",
                "evidence_urls": ["https://example.com/fy24-results"],
                "severity_tag": None,
            }
        ]
    }
    p = tmp_path / "verdicts.yaml"
    with p.open("w", encoding="utf-8") as f:
        yaml.safe_dump(sample, f, allow_unicode=True)

    verdicts = load_verdicts_yaml(p)
    assert len(verdicts) == 1
    v = verdicts[0]
    assert v.promise_id == "fy24-revenue-25pct"
    assert v.outcome == "broken"
    assert v.judged_at == date(2025, 4, 30)
    assert v.evidence_urls == ("https://example.com/fy24-results",)


def test_load_verdicts_rejects_top_level_list(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("- foo\n- bar\n", encoding="utf-8")
    with pytest.raises(ValueError, match="expected top-level mapping"):
        load_verdicts_yaml(p)


def test_load_verdicts_rejects_wrong_inner_type(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("verdicts: 42\n", encoding="utf-8")
    with pytest.raises(ValueError, match="verdicts must be a list"):
        load_verdicts_yaml(p)


def test_load_verdicts_rejects_anonymous_judge(tmp_path):
    bad = {
        "verdicts": [
            {
                "promise_id": "p1",
                "outcome": "broken",
                "reasoning": "x",
                "judged_at": date(2025, 1, 1),
                "judged_by": "anonymous",
            }
        ]
    }
    p = tmp_path / "anon.yaml"
    with p.open("w", encoding="utf-8") as f:
        yaml.safe_dump(bad, f, allow_unicode=True)
    # Verdict's __post_init__ enforces this — loader is just a thin adapter.
    with pytest.raises(ValueError, match="judged_by must be a real signed handle"):
        load_verdicts_yaml(p)


def test_load_company_yaml_rejects_non_mapping(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("- not\n- a\n- mapping\n", encoding="utf-8")
    with pytest.raises(ValueError, match="top-level YAML is not a mapping"):
        load_company_yaml(p)


def test_iso_string_dates_coerced(tmp_path):
    """If a contributor wrote dates as plain strings, the loader still accepts them."""
    sample = {
        "verdicts": [
            {
                "promise_id": "p1",
                "outcome": "fulfilled",
                "reasoning": "ok",
                "judged_at": "2025-04-30",   # string, not date
                "judged_by": "@a",
            }
        ]
    }
    p = tmp_path / "v.yaml"
    with p.open("w", encoding="utf-8") as f:
        yaml.safe_dump(sample, f, allow_unicode=True)
    verdicts = load_verdicts_yaml(p)
    assert verdicts[0].judged_at == date(2025, 4, 30)
