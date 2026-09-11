#!/usr/bin/env python3
"""Emit sanitized API connector readiness states without exposing secrets."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.api_connectors import all_connector_statuses


def main() -> None:
    payload = {
        "connectors": [status.as_dict() for status in all_connector_statuses()],
        "truth_note": (
            "Credential presence is not proof of API permission or live access. "
            "No secret values are emitted."
        ),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
