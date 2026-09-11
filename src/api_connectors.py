"""State model for public and authorized external API connectors.

This module deliberately separates three very different things:
1. public APIs that can run anonymously;
2. official developer APIs/connectors that require credentials or OAuth;
3. private/internal browser endpoints that are not an authorized production contract.

Secrets are never accepted from config files or committed source.  Authorized
connectors read only environment-variable presence here; actual secret values must
remain in a server-side secret store such as GitHub Actions Secrets.
"""

from __future__ import annotations

import os
import shutil
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Iterable


class ConnectorState(str, Enum):
    ACTIVE_LIVE = "ACTIVE_LIVE"
    UNCONFIGURED_AUTH = "UNCONFIGURED_AUTH"
    PERMISSION_REQUIRED = "PERMISSION_REQUIRED"
    AUTHENTICATED_NOT_PROBED = "AUTHENTICATED_NOT_PROBED"
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
    state = (
        ConnectorState.AUTHENTICATED_NOT_PROBED
        if not missing
        else ConnectorState.UNCONFIGURED_AUTH
    )
    return ConnectorStatus(
        source_id="DOUYIN_OPENAPI",
        state=state,
        credential_names=names,
        configured_credentials=configured,
        missing_credentials=missing,
        secret_values_exposed=False,
        notes=(
            "Official Douyin OpenAPI. Credentials prove only that auth can be attempted; "
            "individual scopes still require platform permission and must be probed before ACTIVE_LIVE."
        ),
    )


def weibo_cli_status() -> ConnectorStatus:
    executable = shutil.which("weibo")
    state = (
        ConnectorState.AUTHENTICATED_NOT_PROBED
        if executable
        else ConnectorState.UNCONFIGURED_AUTH
    )
    return ConnectorStatus(
        source_id="WEIBO_CLI",
        state=state,
        credential_names=(),
        configured_credentials=(),
        missing_credentials=(),
        secret_values_exposed=False,
        notes=(
            "Official Weibo CLI connector. Binary presence is not proof of authenticated session; "
            "`weibo auth whoami` must pass before ACTIVE_LIVE."
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
            "Do not substitute reverse-engineered browser endpoints for an authorized API."
        ),
    )


def all_connector_statuses() -> list[ConnectorStatus]:
    return [douyin_status(), weibo_cli_status(), baidu_index_status()]
