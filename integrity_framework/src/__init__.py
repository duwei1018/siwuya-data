"""思无崖 integrity_framework — public API.

For maintainers: see ../METHODOLOGY.md before changing the scoring algorithm.
Any algorithm tweak must bump METHODOLOGY_VERSION and update CHANGELOG.
"""

from .models import (
    METHODOLOGY_VERSION,
    IntegrityScore,
    Promise,
    ScoreBreakdown,
    Verdict,
    VerdictOutcome,
    VerificationType,
)
from .scorer import compute_integrity_score
from .promise_extractor import extract_promises_from_text
from .loader import (
    load_company_yaml,
    load_promises_from_company_yaml,
    load_verdicts_yaml,
)

__all__ = [
    "METHODOLOGY_VERSION",
    "IntegrityScore",
    "Promise",
    "ScoreBreakdown",
    "Verdict",
    "VerdictOutcome",
    "VerificationType",
    "compute_integrity_score",
    "extract_promises_from_text",
    "load_company_yaml",
    "load_promises_from_company_yaml",
    "load_verdicts_yaml",
]
