"""Tests for `compute_integrity_score`.

These exercise the algorithm contract end-to-end: weights, time decay,
severity amplification, skipped outcomes, clamping, and breakdown
visibility. If any of these fail, METHODOLOGY.md and the scorer have
silently drifted apart.
"""

from __future__ import annotations

from datetime import date

import pytest

from integrity_framework.src.models import METHODOLOGY_VERSION, Verdict
from integrity_framework.src.scorer import (
    BASE_SCORE,
    DECAY_YEARS,
    SEVERITY_AMPLIFICATION,
    WEIGHTS,
    compute_integrity_score,
)


def _v(promise_id, outcome, judged_at=date(2026, 4, 1), severity_tag=None) -> Verdict:
    return Verdict(
        promise_id=promise_id,
        outcome=outcome,
        reasoning=f"test {outcome}",
        judged_at=judged_at,
        judged_by="@test-judge",
        severity_tag=severity_tag,
    )


def test_no_verdicts_gives_base_score():
    s = compute_integrity_score([])
    assert s.score == BASE_SCORE
    assert s.counted_verdicts == 0
    assert s.skipped_verdicts == 0
    assert s.methodology_version == METHODOLOGY_VERSION


def test_all_fulfilled_keeps_base_score():
    s = compute_integrity_score(
        [_v(f"p{i}", "fulfilled") for i in range(5)],
        as_of=date(2026, 4, 24),
    )
    assert s.score == BASE_SCORE
    assert s.counted_verdicts == 5


def test_one_broken_deducts_15():
    s = compute_integrity_score([_v("p1", "broken")], as_of=date(2026, 4, 24))
    assert s.score == BASE_SCORE + WEIGHTS["broken"]
    assert s.counted_verdicts == 1


def test_partial_deducts_5():
    s = compute_integrity_score([_v("p1", "partial")], as_of=date(2026, 4, 24))
    assert s.score == BASE_SCORE + WEIGHTS["partial"]


def test_pending_and_unverifiable_are_skipped_not_counted():
    s = compute_integrity_score(
        [_v("p1", "pending"), _v("p2", "unverifiable")],
        as_of=date(2026, 4, 24),
    )
    assert s.score == BASE_SCORE
    assert s.counted_verdicts == 0
    assert s.skipped_verdicts == 2
    # Skipped verdicts still show in the breakdown so the audit trail is honest.
    assert {b.outcome for b in s.breakdown} == {"pending", "unverifiable"}
    assert all(b.final_delta == 0.0 for b in s.breakdown)


def test_old_broken_promise_decays_to_half_weight():
    now = date(2026, 4, 24)
    old_judged_at = date(now.year - DECAY_YEARS - 1, now.month, now.day)
    s = compute_integrity_score([_v("p1", "broken", judged_at=old_judged_at)], as_of=now)
    expected = BASE_SCORE + WEIGHTS["broken"] * 0.5
    assert s.score == pytest.approx(expected)


def test_recent_broken_promise_full_weight():
    now = date(2026, 4, 24)
    fresh_judged_at = date(now.year - DECAY_YEARS + 1, now.month, now.day)
    s = compute_integrity_score([_v("p1", "broken", judged_at=fresh_judged_at)], as_of=now)
    assert s.score == BASE_SCORE + WEIGHTS["broken"]


def test_severity_amplification_only_on_broken_with_amplified_tag():
    now = date(2026, 4, 24)
    s = compute_integrity_score(
        [_v("p1", "broken", severity_tag="financial_misconduct")],
        as_of=now,
    )
    expected = BASE_SCORE + WEIGHTS["broken"] - SEVERITY_AMPLIFICATION
    assert s.score == pytest.approx(expected)


def test_severity_tag_ignored_when_outcome_is_not_broken():
    s = compute_integrity_score(
        [_v("p1", "partial", severity_tag="financial_misconduct")],
        as_of=date(2026, 4, 24),
    )
    # Bonus only fires for broken — partial stays at base partial weight.
    assert s.score == BASE_SCORE + WEIGHTS["partial"]


def test_unrecognised_severity_tag_is_a_no_op():
    s = compute_integrity_score(
        [_v("p1", "broken", severity_tag="just-a-note")],
        as_of=date(2026, 4, 24),
    )
    assert s.score == BASE_SCORE + WEIGHTS["broken"]


def test_score_clamped_to_zero():
    """Many extreme broken promises must not push the score below zero."""
    verdicts = [
        _v(f"p{i}", "broken", severity_tag="financial_misconduct")
        for i in range(20)
    ]
    s = compute_integrity_score(verdicts, as_of=date(2026, 4, 24))
    assert s.score == 0.0
    assert s.counted_verdicts == 20


def test_breakdown_records_each_verdict():
    s = compute_integrity_score(
        [_v("p1", "broken"), _v("p2", "fulfilled"), _v("p3", "pending")],
        as_of=date(2026, 4, 24),
    )
    assert len(s.breakdown) == 3
    assert {b.promise_id for b in s.breakdown} == {"p1", "p2", "p3"}


def test_breakdown_severity_notes_present_only_when_amplified():
    s = compute_integrity_score(
        [_v("p1", "broken", severity_tag="financial_misconduct"), _v("p2", "broken")],
        as_of=date(2026, 4, 24),
    )
    notes_by_id = {b.promise_id: b.notes for b in s.breakdown}
    assert "severity_tag=financial_misconduct" in notes_by_id["p1"]
    assert notes_by_id["p2"] == ""


def test_methodology_version_stamped_on_score():
    s = compute_integrity_score([], as_of=date(2026, 4, 24))
    assert s.methodology_version == METHODOLOGY_VERSION
