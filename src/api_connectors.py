"""State model for external data connectors under a free-only MVP policy.

The project distinguishes:
1. anonymous official/public APIs that can run without incremental fees;
2. official developer APIs that may require credentials but must be reviewed for cost;
3. paid connectors, which are disabled for the MVP;
4. private/internal browser endpoints, which are never treated as production APIs.

Secrets are never accepted from committed config. Authorized connectors may only
read secret presence from server-side environment variables such as GitHub Actions
Secrets, and secret values must never be emitted into status payloads or logs.
"""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Iterable


class ConnectorState(str, Enum):
    ACTIVE_LIVE = "ACTIVE_LIVE"
    API_REACHABLE_DATA_UNAVAILABLE = "API_REACHABLE_DATA_UNAVAILABLE"
    UNCONFIGURED_AUTH = "UNCONFIGURED_AUTH"
    PERMISSION_REQUIRED = "PERMISSION_REQUIRED"
    AUTHENTICATED_NOT_PROBED = "AUTHENTICATED_NOT_PROBED"
    FREE_ONLY_REVIEW_REQUIRED = "FREE_ONLY_REVIEW_REQUIRED"
    DISABLED_PAID_MVP = "DISABLED_PAID_MVP"
    NO_OPEN_API = "NO_OPEN_API"
    MANUAL_AUTHORIZED_ONLY = "MANUAL_AUTHORIZED_ONLY"
    ERROR = "ERROR"


@dataclass(frozen=True)
class ConnectorStatus:
    source_id: str
    state: ConnectorState
    credential_names: tuple[str, ...]
    configured_credentials: tuple[str, ...]
    missing_credentials: tuple[str, ...]
    secret_values_exposed: bool
    notes: str

    def as_dict(self) -> dict:
        data = asdict(self)
        data["state"] = self.state.value
        return data


def _credential_presence(names: Iterable[str]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    configured: list[str] = []
    missing: list[str] = []
    for name in names:
        if os.environ.get(name, "").strip():
            configured.append(name)
        else:
            missing.append(name)
    return tuple(configured), tuple(missing)


def douyin_status() -> ConnectorStatus:
    names = ("DOUYIN_CLIENT_KEY", "DOUYIN_CLIENT_SECRET")
    configured, missing = _credential_presence(names)
    return ConnectorStatus(
        source_id="DOUYIN_OPENAPI",
        state=ConnectorState.FREE_ONLY_REVIEW_REQUIRED,
        credential_names=names,
        configured_credentials=configured,
        missing_credentials=missing,
        secret_values_exposed=False,
        notes=(
            "Official Douyin OpenAPI is allowed only after the exact scopes used by this project "
            "are confirmed to have zero incremental usage fee. Credential presence alone must "
            "never activate the connector."
        ),
    )


def weibo_cli_status() -> ConnectorStatus:
    return ConnectorStatus(
        source_id="WEIBO_CLI",
        state=ConnectorState.DISABLED_PAID_MVP,
        credential_names=(),
        configured_credentials=(),
        missing_credentials=(),
        secret_values_exposed=False,
        notes=(
            "Weibo CLI requires a paid plan/credits for the intended production use, so it is "
            "disabled under the zero-paid-data MVP policy even if a local login already exists."
        ),
    )


def baidu_index_status() -> ConnectorStatus:
    return ConnectorStatus(
        source_id="BAIDU_INDEX",
        state=ConnectorState.NO_OPEN_API,
        credential_names=(),
        configured_credentials=(),
        missing_credentials=(),
        secret_values_exposed=False,
        notes=(
            "Baidu Index official help states that no open API is currently provided. "
            "Use only authorized/manual free views; never substitute reverse-engineered browser endpoints."
        ),
    )


def all_connector_statuses() -> list[ConnectorStatus]:
    return [douyin_status(), weibo_cli_status(), baidu_index_status()]
