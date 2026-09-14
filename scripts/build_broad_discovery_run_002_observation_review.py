#!/usr/bin/env python3
"""Compatibility wrapper for the generalized Broad Discovery observation-review builder.

New runs must use ``scripts/build_broad_discovery_observation_review.py`` directly.
This file remains only so historical Run 002 workflows/imports keep working.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_broad_discovery_observation_review import (  # noqa: E402,F401
    ALIGNMENT_SCHEMA,
    ALIGNMENT_SEMANTICS,
    GENERIC_TRUTH_BOUNDARIES,
    REVIEW_SEMANTICS,
    _alignment,
    _build_research_evidence,
    _combine_reviewed,
    _load_dynamic_terms,
    _load_object,
    build_observation_review,
    main,
)


if __name__ == "__main__":
    raise SystemExit(main())
