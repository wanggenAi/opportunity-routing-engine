#!/usr/bin/env python3
"""Compatibility wrapper for the generalized Broad Discovery observation-review builder.

New runs must use ``scripts/build_broad_discovery_observation_review.py`` directly.
This file remains only so historical Run 002 workflows/imports keep working.
"""

from scripts.build_broad_discovery_observation_review import (  # noqa: F401
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
