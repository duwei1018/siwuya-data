"""Integrity scoring algorithm v0.1.0.

The algorithm is deliberately simple so it can be audited in one sitting.
Anything more sophisticated belongs in a dated successor module
(`scorer_v0_2_0.py`, etc.) with its own METHODOLOGY entry — never silent
in-place tweaks.

Algorithm summary (see `../METHODOLOGY.md` for justification):

    base = 100
    for each verdict:
        raw_delta = WEIGHTS[outcome]              # see WEIGHTS below
        decay = 0.5 if judged_at older than DECAY_YEARS else 1.0
        severity_bonus = -SEVERITY_AMPLIFICATION
                         if outcome == "broken"
                         and severity_tag in SEVERITY_AMPLIFIED_TAGS
                         else 0.0
        final_delta = (raw_delta + severity_bonus) * decay
        score += final_delta
    score = clamp(score, 0, 100)

`pending` and `unverifiable` verdicts are deliberately not counted —
they do not penalise (no evidence) but they are surfaced in
`IntegrityScore.skipped_verdicts` so the reader can see how thin the
sample is.

All threshold/weight constants are annotated with provenance:
    Claude@2026-04-24 v0.1.0 first cut · placeholder weights pending
    backtest. WHY: spec L549-563 default. WHEN-TO-RECHECK: after first
    50 real verdicts land in companies/<market>/*.yaml.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Iterable

from .models import (
    METHODOLOGY_VERSION,
    IntegrityScore,
    ScoreBreakdown,
    Verdict,
    VerdictOutcome,
)


# Claude@2026-04-24 v0.1.0 default weights — placeholder pending backtest.
# Source: SIWUYA_DATA_BOOTSTRAP.md L549-563 default. Re-evaluate after first
# 50 real verdicts; document any change in METHODOLOGY.md "Version History".
WEIGHTS: dict[VerdictOutcome, float] = {
    "fulfilled": 0.0,        # baseline — fulfilment is expected, not bonus
    "partial": -5.0,
    "broken": -15.0,
    "pending": 0.0,          # not counted (see SKIPPED_OUTCOMES)
    "unverifiable": 0.0,     # not counted (see SKIPPED_OUTCOMES)
}

SKIPPED_OUTCOMES: frozenset[VerdictOutcome] = frozenset({"pending", "unverifiable"})

# Claude@2026-04-24 v0.1.0 — verdicts older than DECAY_YEARS get half weight,
# so an ancient broken promise still affects the score but a new one dominates.
# WHY: people / strategy change; recent behaviour is more predictive.
DECAY_YEARS: int = 3
DECAY_MULTIPLIER_OLD: float = 0.5

# Claude@2026-04-24 v0.1.0 — qualitative severity tags that further deduct
# beyond the base "broken" weight. The list intentionally starts narrow
# (only frauds + audit-flagged misstatements) so the framework does not
# over-penalise on judgement calls. Expand only after community discussion
# (open a methodology_discussion issue).
SEVERITY_AMPLIFICATION: float = 30.0
SEVERITY_AMPLIFIED_TAGS: frozenset[str] = frozenset(
    {
        "financial_misconduct",
        "audit_qualification",
        "fraud_admission",
    }
)

BASE_SCORE: float = 100.0


def _decay_multiplier(judged_at: date, now: date) -> float:
    """Return 1.0 for fresh verdicts, DECAY_MULTIPLIER_OLD for old ones.

    `now` is injected so tests are deterministic and so callers can score
    a snapshot "as of date X" without wall-clock dependency.
    """
    cutoff = now - timedelta(days=365 * DECAY_YEARS)
    return 1.0 if judged_at >= cutoff else DECAY_MULTIPLIER_OLD


def _severity_bonus(verdict: Verdict) -> float:
    """Extra penalty when a broken promise carries an amplified severity tag."""
    if verdict.outcome != "broken":
        return 0.0
    if verdict.severity_tag is None:
        return 0.0
    if verdict.severity_tag not in SEVERITY_AMPLIFIED_TAGS:
        return 0.0
    return -SEVERITY_AMPLIFICATION


def compute_integrity_score(
    verdicts: Iterable[Verdict],
    *,
    as_of: date | None = None,
) -> IntegrityScore:
    """Compute an integrity score for a bundle of verdicts.

    Args:
        verdicts: iterable of `Verdict` objects covering the same subject
            (the framework does not split by ticker — caller filters).
        as_of: anchor date for decay. Defaults to `date.today()`.

    Returns:
        `IntegrityScore` with the final number plus a per-verdict breakdown.

    Raises:
        ValueError: if a verdict's score-time invariants would silently drop
            the audit trail. (Construction-time invariants are enforced in
            `Verdict.__post_init__`.)
    """
    now = as_of or date.today()
    score = BASE_SCORE
    breakdown: list[ScoreBreakdown] = []
    counted = 0
    skipped = 0

    for v in verdicts:
        if v.outcome in SKIPPED_OUTCOMES:
            skipped += 1
            breakdown.append(
                ScoreBreakdown(
                    promise_id=v.promise_id,
                    outcome=v.outcome,
                    raw_delta=0.0,
                    decay_multiplier=1.0,
                    severity_bonus=0.0,
                    final_delta=0.0,
                    judged_by=v.judged_by,
                    judged_at=v.judged_at,
                    notes="skipped (no evidence yet — pending or unverifiable)",
                )
            )
            continue

        raw = WEIGHTS[v.outcome]
        decay = _decay_multiplier(v.judged_at, now)
        bonus = _severity_bonus(v)
        final = (raw + bonus) * decay
        score += final
        counted += 1
        breakdown.append(
            ScoreBreakdown(
                promise_id=v.promise_id,
                outcome=v.outcome,
                raw_delta=raw,
                decay_multiplier=decay,
                severity_bonus=bonus,
                final_delta=final,
                judged_by=v.judged_by,
                judged_at=v.judged_at,
                notes="" if bonus == 0.0 else f"severity_tag={v.severity_tag}",
            )
        )

    score = max(0.0, min(BASE_SCORE, score))

    return IntegrityScore(
        score=round(score, 2),
        breakdown=tuple(breakdown),
        methodology_version=METHODOLOGY_VERSION,
        counted_verdicts=counted,
        skipped_verdicts=skipped,
    )
