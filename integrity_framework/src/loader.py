"""YAML ↔ dataclass adapters.

Two distinct loaders, intentionally separate:

* `load_promises_from_company_yaml` — promises live inside the public
  company YAML (`integrity_tracking.tracked_promises[]`). Companies in
  this repo are CC-BY-SA, so the loader only ever reads, never writes.

* `load_verdicts_yaml` — verdicts live **outside** the public repo by
  design (legal boundary). This loader reads a sidecar YAML format
  documented in `../docs/03_edge_cases.md` so notebooks and downstream
  tools have one shared schema; the file format itself is not part of
  the public data contract.

The split exists so a contributor cannot accidentally check verdicts
into the public companies/ tree.
"""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import Any

from .models import Promise, Verdict


def _coerce_date(raw: Any) -> date | None:
    """YAML may parse dates as `date`, `datetime`, or stringly. Normalise."""
    if raw is None:
        return None
    if isinstance(raw, date) and not isinstance(raw, datetime):
        return raw
    if isinstance(raw, datetime):
        return raw.date()
    if isinstance(raw, str):
        return date.fromisoformat(raw)
    raise TypeError(f"Cannot coerce {raw!r} ({type(raw).__name__}) to date.")


def _require_yaml():
    try:
        import yaml  # type: ignore
    except ImportError as e:  # pragma: no cover - hard env error
        raise ImportError(
            "PyYAML is required. Run: pip install pyyaml"
        ) from e
    return yaml


def load_company_yaml(path: str | Path) -> dict:
    """Load a company YAML file. Returns the raw dict; no schema check.

    Use `scripts/validate_company.py` for schema validation; this loader
    intentionally stays unaware of the schema so it keeps working when the
    schema evolves.
    """
    yaml = _require_yaml()
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{p}: top-level YAML is not a mapping.")
    return data


def load_promises_from_company_yaml(
    path: str | Path,
    subject_ticker_override: str | None = None,
) -> list[Promise]:
    """Read promises from `integrity_tracking.tracked_promises[]`.

    `subject_ticker_override` is for tests / fixtures where the YAML lacks
    an `identity.primary_ticker`; in normal use the loader pulls the
    ticker from the document.
    """
    data = load_company_yaml(path)

    integrity = data.get("integrity_tracking") or {}
    raw_promises = integrity.get("tracked_promises") or []
    if not isinstance(raw_promises, list):
        raise ValueError(
            f"{path}: integrity_tracking.tracked_promises must be a list, "
            f"got {type(raw_promises).__name__}."
        )

    identity = data.get("identity") or {}
    ticker = subject_ticker_override or identity.get("primary_ticker")

    out: list[Promise] = []
    for raw in raw_promises:
        if not isinstance(raw, dict):
            raise ValueError(
                f"{path}: each tracked_promise must be a mapping, got {type(raw).__name__}."
            )
        out.append(
            Promise(
                id=raw["id"],
                promise_zh=raw["promise_zh"],
                source=raw["source"],
                verification_type=raw["verification_type"],
                promise_en=raw.get("promise_en"),
                made_on=_coerce_date(raw.get("made_on")),
                due_by=_coerce_date(raw.get("due_by")),
                subject_ticker=ticker,
                made_by=raw.get("made_by"),
            )
        )
    return out


def load_verdicts_yaml(path: str | Path) -> list[Verdict]:
    """Read a sidecar verdicts YAML.

    Expected shape::

        verdicts:
          - promise_id: fy24-revenue-25pct
            outcome: broken
            reasoning: "FY24 revenue +18%, missed guidance by 7pp."
            judged_at: 2025-04-30
            judged_by: "@analyst-handle"
            evidence_urls:
              - https://...
            severity_tag: null   # optional

    The repo does not ship any verdicts file — this loader exists so
    notebooks and downstream tools can pass a YAML path instead of
    constructing Verdicts inline.
    """
    yaml = _require_yaml()
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict) or "verdicts" not in data:
        raise ValueError(f"{p}: expected top-level mapping with a `verdicts:` list.")

    raw_verdicts = data["verdicts"] or []
    if not isinstance(raw_verdicts, list):
        raise ValueError(
            f"{p}: verdicts must be a list, got {type(raw_verdicts).__name__}."
        )

    out: list[Verdict] = []
    for raw in raw_verdicts:
        if not isinstance(raw, dict):
            raise ValueError(
                f"{p}: each verdict must be a mapping, got {type(raw).__name__}."
            )
        evidence = raw.get("evidence_urls") or []
        if not isinstance(evidence, list):
            raise ValueError(
                f"{p}: verdict[{raw.get('promise_id')}].evidence_urls must be a list."
            )
        out.append(
            Verdict(
                promise_id=raw["promise_id"],
                outcome=raw["outcome"],
                reasoning=raw["reasoning"],
                judged_at=_coerce_date(raw["judged_at"]),
                judged_by=raw["judged_by"],
                evidence_urls=tuple(str(u) for u in evidence),
                severity_tag=raw.get("severity_tag"),
            )
        )
    return out
