"""Tests for Promise / Verdict / IntegrityScore data models.

These tests pin invariants that the rest of the framework depends on:
required-field validation, enum constraints, and the anonymous-judge
rejection rule. Loosen any of these and the audit trail story breaks.
"""

from __future__ import annotations

from datetime import date

import pytest

from integrity_framework.src.models import (
    METHODOLOGY_VERSION,
    IntegrityScore,
    Promise,
    ScoreBreakdown,
    Verdict,
)


# ---------- Promise ----------

def _ok_promise(**overrides) -> Promise:
    base = dict(
        id="fy24-revenue-25pct",
        promise_zh="承诺 FY24 营收同比增长 25%",
        source="https://example.com/q1-call",
        verification_type="financial_metric",
    )
    base.update(overrides)
    return Promise(**base)


def test_promise_minimum_required_fields_succeeds():
    p = _ok_promise()
    assert p.id == "fy24-revenue-25pct"
    assert p.text == p.promise_zh   # `text` alias
    assert p.made_on is None
    assert p.subject_ticker is None


def test_promise_blank_id_rejected():
    with pytest.raises(ValueError, match="id is required"):
        _ok_promise(id="   ")


def test_promise_blank_promise_zh_rejected():
    with pytest.raises(ValueError, match="promise_zh is required"):
        _ok_promise(promise_zh="")


def test_promise_blank_source_rejected():
    with pytest.raises(ValueError, match="source is required"):
        _ok_promise(source="")


def test_promise_invalid_verification_type_rejected():
    with pytest.raises(ValueError, match="verification_type must be one of"):
        _ok_promise(verification_type="bogus_category")


def test_promise_with_all_optionals():
    p = _ok_promise(
        promise_en="25% YoY revenue growth",
        made_on=date(2024, 5, 1),
        due_by=date(2025, 2, 15),
        subject_ticker="EXAMPLE.US",
        made_by="@example-ceo",
    )
    assert p.made_by == "@example-ceo"
    assert p.due_by.year == 2025


def test_promise_is_frozen_immutable():
    p = _ok_promise()
    with pytest.raises(Exception):
        p.id = "tampered"   # type: ignore[misc]


# ---------- Verdict ----------

def _ok_verdict(**overrides) -> Verdict:
    base = dict(
        promise_id="fy24-revenue-25pct",
        outcome="broken",
        reasoning="FY24 actual +18%, missed by 7pp.",
        judged_at=date(2025, 4, 30),
        judged_by="@analyst-handle",
    )
    base.update(overrides)
    return Verdict(**base)


def test_verdict_happy_path():
    v = _ok_verdict()
    assert v.outcome == "broken"
    assert v.evidence_urls == ()


def test_verdict_blank_promise_id_rejected():
    with pytest.raises(ValueError, match="promise_id is required"):
        _ok_verdict(promise_id="")


def test_verdict_invalid_outcome_rejected():
    with pytest.raises(ValueError, match="outcome must be one of"):
        _ok_verdict(outcome="kinda-broken")


def test_verdict_blank_reasoning_rejected():
    with pytest.raises(ValueError, match="reasoning is required"):
        _ok_verdict(reasoning="   ")


@pytest.mark.parametrize("forbidden", ["", "anonymous", "Anonymous", "ANONYMOUS", "unknown", "n/a", "none"])
def test_verdict_anonymous_judge_rejected(forbidden):
    with pytest.raises(ValueError, match="judged_by must be a real signed handle"):
        _ok_verdict(judged_by=forbidden)


def test_verdict_evidence_list_coerced_to_tuple():
    v = _ok_verdict(evidence_urls=["https://a", "https://b"])
    assert v.evidence_urls == ("https://a", "https://b")
    # Frozen dataclass — replacing the field would raise; this proves the
    # post_init coercion landed.
    assert isinstance(v.evidence_urls, tuple)


def test_verdict_severity_tag_optional():
    v = _ok_verdict(severity_tag="financial_misconduct")
    assert v.severity_tag == "financial_misconduct"


# ---------- IntegrityScore ----------

def test_integrity_score_to_dict_round_trip_keys():
    bk = ScoreBreakdown(
        promise_id="p1",
        outcome="broken",
        raw_delta=-15.0,
        decay_multiplier=1.0,
        severity_bonus=0.0,
        final_delta=-15.0,
        judged_by="@a",
        judged_at=date(2025, 1, 1),
        notes="",
    )
    score = IntegrityScore(
        score=85.0,
        breakdown=(bk,),
        methodology_version=METHODOLOGY_VERSION,
        counted_verdicts=1,
        skipped_verdicts=0,
    )
    d = score.to_dict()
    assert d["score"] == 85.0
    assert d["methodology_version"] == METHODOLOGY_VERSION
    assert d["breakdown"][0]["promise_id"] == "p1"
    assert d["breakdown"][0]["judged_at"] == "2025-01-01"   # ISO string
