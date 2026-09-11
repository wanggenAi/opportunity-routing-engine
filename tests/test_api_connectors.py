import os
import unittest
from unittest.mock import patch

from src.api_connectors import (
    ConnectorState,
    baidu_index_status,
    douyin_status,
    weibo_cli_status,
)


class ApiConnectorStatusTests(unittest.TestCase):
    def test_reachable_but_empty_api_state_is_distinct_from_active_or_error(self):
        self.assertEqual(
            ConnectorState.API_REACHABLE_DATA_UNAVAILABLE.value,
            "API_REACHABLE_DATA_UNAVAILABLE",
        )
        self.assertNotEqual(
            ConnectorState.API_REACHABLE_DATA_UNAVAILABLE,
            ConnectorState.ACTIVE_LIVE,
        )
        self.assertNotEqual(
            ConnectorState.API_REACHABLE_DATA_UNAVAILABLE,
            ConnectorState.ERROR,
        )

    def test_douyin_is_not_activated_before_free_scope_review(self):
        with patch.dict(os.environ, {}, clear=True):
            status = douyin_status()
        self.assertEqual(status.state, ConnectorState.FREE_ONLY_REVIEW_REQUIRED)
        self.assertEqual(
            set(status.missing_credentials),
            {"DOUYIN_CLIENT_KEY", "DOUYIN_CLIENT_SECRET"},
        )
        self.assertFalse(status.secret_values_exposed)

    def test_douyin_secret_presence_never_bypasses_free_only_gate(self):
        env = {
            "DOUYIN_CLIENT_KEY": "client-key-value",
            "DOUYIN_CLIENT_SECRET": "super-secret-value",
        }
        with patch.dict(os.environ, env, clear=True):
            payload = douyin_status().as_dict()
        self.assertEqual(payload["state"], "FREE_ONLY_REVIEW_REQUIRED")
        serialized = repr(payload)
        self.assertNotIn("client-key-value", serialized)
        self.assertNotIn("super-secret-value", serialized)
        self.assertEqual(
            set(payload["configured_credentials"]),
            {"DOUYIN_CLIENT_KEY", "DOUYIN_CLIENT_SECRET"},
        )

    def test_weibo_cli_is_disabled_under_zero_paid_data_policy(self):
        status = weibo_cli_status()
        self.assertEqual(status.state, ConnectorState.DISABLED_PAID_MVP)
        self.assertIn("zero-paid-data", status.notes)

    def test_baidu_index_is_not_treated_as_open_api(self):
        status = baidu_index_status()
        self.assertEqual(status.state, ConnectorState.NO_OPEN_API)
        self.assertIn("reverse-engineered", status.notes)


if __name__ == "__main__":
    unittest.main()
