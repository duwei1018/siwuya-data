"""Tests for the MVP promise extractor.

The MVP is a heuristic — these tests pin behavioural floors, not ceilings.
Anyone replacing the MVP with an LLM-backed extractor should keep these
shapes (function signature, return type, normalisation) so downstream
consumers do not have to change.
"""

from __future__ import annotations

from datetime import date

import pytest

from integrity_framework.src.models import Promise
from integrity_framework.src.promise_extractor import extract_promises_from_text


def test_empty_text_returns_empty_list():
    assert extract_promises_from_text("") == []


def test_text_with_no_promise_keywords_returns_empty():
    assert extract_promises_from_text("天气很好。今天上海气温二十度。") == []


def test_chinese_keyword_detected():
    text = "管理层承诺 2025 年营收增长 25%。这只是背景介绍。"
    out = extract_promises_from_text(text)
    assert len(out) == 1
    assert "承诺" in out[0].promise_zh


def test_english_keyword_detected():
    text = "We will launch the AI Agent in Q1 2025. Background: it has been in beta."
    out = extract_promises_from_text(text)
    assert len(out) == 1
    assert "will launch" in out[0].promise_zh.lower()


def test_verification_type_inferred_financial():
    text = "We commit to 25% YoY revenue growth in FY24."
    out = extract_promises_from_text(text)
    assert out[0].verification_type == "financial_metric"


def test_verification_type_inferred_product_launch():
    text = "我们计划 2025 Q1 推出新产品 GA。"
    out = extract_promises_from_text(text)
    assert out[0].verification_type == "product_launch"


def test_verification_type_inferred_esg():
    text = "We will reach carbon neutrality by 2030."
    out = extract_promises_from_text(text)
    assert out[0].verification_type == "ESG_target"


def test_verification_type_default_other():
    text = "管理层承诺加强公司治理。"   # no obvious keyword
    out = extract_promises_from_text(text)
    assert out[0].verification_type in ("strategic_initiative", "other")


def test_context_metadata_propagates():
    text = "We will deliver Q4 guidance on schedule."
    out = extract_promises_from_text(
        text,
        context={
            "source": "https://example.com/q3-call",
            "made_on": date(2024, 11, 1),
            "subject_ticker": "EXAMPLE.US",
            "made_by": "@example-ceo",
        },
    )
    assert out[0].source == "https://example.com/q3-call"
    assert out[0].made_on == date(2024, 11, 1)
    assert out[0].subject_ticker == "EXAMPLE.US"
    assert out[0].made_by == "@example-ceo"


def test_each_extracted_promise_has_unique_id():
    text = "We will deliver A. We will deliver B. We will deliver C."
    out = extract_promises_from_text(text)
    assert len(out) == 3
    assert len({p.id for p in out}) == 3   # no collisions


def test_extracted_promises_pass_promise_validation():
    """Round-trip: anything the extractor produces must satisfy Promise's invariants."""
    text = "We will achieve 30% margin by 2025."
    out = extract_promises_from_text(text)
    for p in out:
        assert isinstance(p, Promise)
        # Re-construct to re-trigger __post_init__ — must not raise.
        Promise(
            id=p.id,
            promise_zh=p.promise_zh,
            source=p.source,
            verification_type=p.verification_type,
        )


def test_default_source_when_no_context_is_invalid_url_marker():
    """If caller forgot to pass a source, the placeholder URL is obviously fake.

    This is intentional: it forces a downstream review step to notice and
    fix the URL before persisting.
    """
    out = extract_promises_from_text("We will improve.")
    assert "example.invalid" in out[0].source
