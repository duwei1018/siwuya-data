"""MVP promise extraction — pattern + keyword based.

Why MVP-only here: this repo deliberately ships **zero** outbound network
calls. A real promise extractor needs an LLM, but adding API key plumbing
to a public, dependency-light data repo is exactly the wrong shape. The
MVP exists to:

1. Demonstrate the intended API surface (text in → list[Promise] out).
2. Give contributors a starting point they can swap for a smarter
   implementation in their own pipeline.
3. Round-trip survive an `extract → validate → score` test fixture so the
   end-to-end shape is exercised in CI.

For production-grade extraction, point a downstream LLM at the same
function signature; do not vendor an LLM client into this repo.
"""

from __future__ import annotations

import re
import unicodedata
import uuid
from datetime import date
from typing import Mapping, Sequence

from .models import Promise, VerificationType


# Heuristic vocabulary. Hand-tuned starter set — keep small.
# Bigger lists belong in a downstream LLM-backed extractor, not here.
_PROMISE_KEYWORDS_ZH: tuple[str, ...] = (
    "承诺", "将", "计划", "目标", "争取", "保证", "承担", "确保", "未来",
)
_PROMISE_KEYWORDS_EN: tuple[str, ...] = (
    "commit", "will", "plan to", "target", "guidance", "expect to",
    "intend to", "aim to", "ensure",
)

_VERIFICATION_HINTS: tuple[tuple[VerificationType, tuple[str, ...]], ...] = (
    ("financial_metric", ("revenue", "营收", "利润", "毛利", "净利", "增长", "%", "yoy", "qoq")),
    ("product_launch", ("发布", "上线", "推出", "ga", "launch", "release", "ship")),
    ("ESG_target", ("碳", "ESG", "减排", "可持续", "carbon", "sustainability", "diversity")),
    ("strategic_initiative", ("战略", "重组", "并购", "扩张", "strategy", "M&A", "expansion")),
)


_SENTENCE_SPLIT_RE = re.compile(r"(?<=[。！？!?\.])\s+|\n+")


def _normalise(text: str) -> str:
    """NFKC normalise — collapses fullwidth digits, decomposed unicode, etc."""
    return unicodedata.normalize("NFKC", text).strip()


def _looks_like_promise(sentence: str) -> bool:
    lower = sentence.lower()
    if any(kw in sentence for kw in _PROMISE_KEYWORDS_ZH):
        return True
    if any(kw in lower for kw in _PROMISE_KEYWORDS_EN):
        return True
    return False


def _guess_verification_type(sentence: str) -> VerificationType:
    lower = sentence.lower()
    for vtype, hints in _VERIFICATION_HINTS:
        if any(h in lower for h in hints):
            return vtype
    return "other"


def _slugify(seed: str) -> str:
    """Rough slug — stable enough for `Promise.id` if no caller-supplied id."""
    cleaned = re.sub(r"[^a-z0-9]+", "-", seed.lower()).strip("-")
    cleaned = cleaned[:40] or "promise"
    return f"{cleaned}-{uuid.uuid4().hex[:6]}"


def extract_promises_from_text(
    text: str,
    context: Mapping[str, object] | None = None,
) -> list[Promise]:
    """Extract candidate promises from a text source.

    Args:
        text: raw text (earnings call transcript, press release, blog post).
        context: optional metadata. Recognised keys:
            - `source` (str): URL backing this text — copied to every Promise.
              Required if the resulting promises will be persisted.
            - `made_on` (date): date the statements were made.
            - `subject_ticker` (str): ticker the speaker represents.
            - `made_by` (str): named individual who said it.

    Returns:
        List of `Promise` objects. Empty list if no candidate sentence
        matched. The list is a starting draft — every entry must be
        human-reviewed before it lands in a YAML file.
    """
    ctx: Mapping[str, object] = context or {}
    source = str(ctx.get("source") or "https://example.invalid/extracted-draft")
    made_on_raw = ctx.get("made_on")
    made_on = made_on_raw if isinstance(made_on_raw, date) else None
    subject_ticker = ctx.get("subject_ticker")
    made_by = ctx.get("made_by")

    promises: list[Promise] = []
    for raw_sentence in _SENTENCE_SPLIT_RE.split(_normalise(text)):
        sentence = raw_sentence.strip()
        if not sentence:
            continue
        if not _looks_like_promise(sentence):
            continue

        promises.append(
            Promise(
                id=_slugify(sentence[:30]),
                promise_zh=sentence,
                source=source,
                verification_type=_guess_verification_type(sentence),
                made_on=made_on,
                subject_ticker=str(subject_ticker) if subject_ticker else None,
                made_by=str(made_by) if made_by else None,
            )
        )
    return promises


__all__: Sequence[str] = ["extract_promises_from_text"]
