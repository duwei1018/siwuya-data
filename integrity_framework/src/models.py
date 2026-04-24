"""Data models for the integrity framework.

Two core entities:

* `Promise` — a public, time-bounded commitment from named management,
  loaded from `companies/<market>/<slug>.yaml :: integrity_tracking.tracked_promises[]`.
  Promises store **facts** (what was said, by whom, when, by when), never
  judgments. Aligning the dataclass with the published YAML schema (rather
  than the spec L519 sketch) keeps a single source of truth for the data
  contract; see `.reports/STAGE_4_REPORT.md` for the deviation rationale.

* `Verdict` — a research judgment about whether a `Promise` was kept.
  Verdicts live **outside** the public YAML by design (legal boundary):
  every verdict is signed by `judged_by` and is rebuttable. The framework
  consumes verdicts at runtime; how they are stored (notebook, private DB,
  command-line input) is the caller's choice.

Anyone can construct a `Verdict` without `judged_by` set to a real handle —
the constructor refuses `""`, `None`, and the literal `"anonymous"` so the
attribution requirement cannot be silently bypassed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Literal


METHODOLOGY_VERSION = "0.1.0"


VerificationType = Literal[
    "financial_metric",
    "product_launch",
    "strategic_initiative",
    "ESG_target",
    "other",
]


VerdictOutcome = Literal[
    "fulfilled",
    "partial",
    "broken",
    "pending",
    "unverifiable",
]


_VERIFICATION_TYPES: frozenset[str] = frozenset(
    [
        "financial_metric",
        "product_launch",
        "strategic_initiative",
        "ESG_target",
        "other",
    ]
)


_VERDICT_OUTCOMES: frozenset[str] = frozenset(
    ["fulfilled", "partial", "broken", "pending", "unverifiable"]
)


_FORBIDDEN_JUDGED_BY: frozenset[str] = frozenset(["", "anonymous", "unknown", "n/a", "none"])


@dataclass(frozen=True)
class Promise:
    """A tracked public commitment from a named member of management.

    Field set is the same shape the YAML schema enforces, so a Promise can
    round-trip through the published company file without losing or
    inventing fields.
    """

    id: str
    promise_zh: str
    source: str
    verification_type: VerificationType
    promise_en: str | None = None
    made_on: date | None = None
    due_by: date | None = None
    subject_ticker: str | None = None
    made_by: str | None = None

    def __post_init__(self) -> None:
        if not self.id or not self.id.strip():
            raise ValueError("Promise.id is required and must not be blank.")
        if not self.promise_zh or not self.promise_zh.strip():
            raise ValueError(
                f"Promise[{self.id}].promise_zh is required (a promise must have its original text)."
            )
        if not self.source or not self.source.strip():
            raise ValueError(
                f"Promise[{self.id}].source is required (every claim needs an attestable URL)."
            )
        if self.verification_type not in _VERIFICATION_TYPES:
            raise ValueError(
                f"Promise[{self.id}].verification_type must be one of "
                f"{sorted(_VERIFICATION_TYPES)}, got {self.verification_type!r}."
            )

    @property
    def text(self) -> str:
        """Convenience accessor — Chinese is canonical; English is auxiliary."""
        return self.promise_zh


@dataclass(frozen=True)
class Verdict:
    """A signed research judgment on whether a `Promise` was kept.

    `reasoning` is mandatory: a score with no reasoning has no audit trail
    and cannot be challenged, which would defeat the framework's purpose.
    `judged_by` must be a real handle so accountability is unambiguous; the
    literal "anonymous" (and similar placeholders) is rejected at
    construction time, not at scoring time.
    """

    promise_id: str
    outcome: VerdictOutcome
    reasoning: str
    judged_at: date
    judged_by: str
    evidence_urls: tuple[str, ...] = field(default_factory=tuple)
    severity_tag: str | None = None

    def __post_init__(self) -> None:
        if not self.promise_id or not self.promise_id.strip():
            raise ValueError("Verdict.promise_id is required (it must reference a Promise.id).")
        if self.outcome not in _VERDICT_OUTCOMES:
            raise ValueError(
                f"Verdict[{self.promise_id}].outcome must be one of "
                f"{sorted(_VERDICT_OUTCOMES)}, got {self.outcome!r}."
            )
        if not self.reasoning or not self.reasoning.strip():
            raise ValueError(
                f"Verdict[{self.promise_id}].reasoning is required — every judgment must be explainable."
            )
        if not self.judged_by or self.judged_by.strip().lower() in _FORBIDDEN_JUDGED_BY:
            raise ValueError(
                f"Verdict[{self.promise_id}].judged_by must be a real signed handle, "
                f"not {self.judged_by!r}."
            )
        # `tuple()` here also coerces lists for ergonomic callers; the field
        # itself stays immutable so a Verdict instance is hashable / safe to share.
        if not isinstance(self.evidence_urls, tuple):
            object.__setattr__(self, "evidence_urls", tuple(self.evidence_urls))


@dataclass(frozen=True)
class ScoreBreakdown:
    """Per-Verdict contribution to the final integrity score.

    Exposing the breakdown is non-negotiable: without it, the score is a
    black box and cannot be reviewed.
    """

    promise_id: str
    outcome: VerdictOutcome
    raw_delta: float
    decay_multiplier: float
    severity_bonus: float
    final_delta: float
    judged_by: str
    judged_at: date
    notes: str = ""


@dataclass(frozen=True)
class IntegrityScore:
    """Output of `compute_integrity_score`.

    `score` is clamped to [0, 100]; `breakdown` is the full audit trail.
    `methodology_version` is captured at scoring time so an old score can
    always be re-derived against the algorithm version that produced it.
    """

    score: float
    breakdown: tuple[ScoreBreakdown, ...]
    methodology_version: str
    counted_verdicts: int
    skipped_verdicts: int

    def to_dict(self) -> dict:
        """Plain-dict form for JSON serialisation in notebooks / web layers."""
        return {
            "score": self.score,
            "methodology_version": self.methodology_version,
            "counted_verdicts": self.counted_verdicts,
            "skipped_verdicts": self.skipped_verdicts,
            "breakdown": [
                {
                    "promise_id": b.promise_id,
                    "outcome": b.outcome,
                    "raw_delta": b.raw_delta,
                    "decay_multiplier": b.decay_multiplier,
                    "severity_bonus": b.severity_bonus,
                    "final_delta": b.final_delta,
                    "judged_by": b.judged_by,
                    "judged_at": b.judged_at.isoformat(),
                    "notes": b.notes,
                }
                for b in self.breakdown
            ],
        }
