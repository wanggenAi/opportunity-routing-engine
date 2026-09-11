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
    def test_douyin_without_secrets_is_unconfigured(self):
        with patch.dict(os.environ, {}, clear=True):
            status = douyin_status()
        self.assertEqual(status.state, ConnectorState.UNCONFIGURED_AUTH)
        self.assertEqual(
            set(status.missing_credentials),
            {"DOUYIN_CLIENT_KEY", "DOUYIN_CLIENT_SECRET"},
        )
        self.assertFalse(status.secret_values_exposed)

    def test_douyin_with_secret_presence_never_exposes_values(self):
        env = {
            "DOUYIN_CLIENT_KEY": "client-key-value",
            "DOUYIN_CLIENT_SECRET": "super-secret-value",
        }
        with patch.dict(os.environ, env, clear=True):
            payload = douyin_status().as_dict()
        self.assertEqual(payload["state"], "AUTHENTICATED_NOT_PROBED")
        serialized = repr(payload)
        self.assertNotIn("client-key-value", serialized)
        self.assertNotIn("super-secret-value", serialized)
        self.assertEqual(
            set(payload["configured_credentials"]),
            {"DOUYIN_CLIENT_KEY", "DOUYIN_CLIENT_SECRET"},
        )

    @patch("src.api_connectors.shutil.which", return_value=None)
    def test_weibo_cli_missing_binary_is_not_live(self, _which):
        status = weibo_cli_status()
        self.assertEqual(status.state, ConnectorState.UNCONFIGURED_AUTH)

    @patch("src.api_connectors.shutil.which", return_value="/usr/local/bin/weibo")
    def test_weibo_cli_binary_presence_is_not_live_proof(self, _which):
        status = weibo_cli_status()
        self.assertEqual(status.state, ConnectorState.AUTHENTICATED_NOT_PROBED)
        self.assertIn("whoami", status.notes)

    def test_baidu_index_is_not_treated_as_open_api(self):
        status = baidu_index_status()
        self.assertEqual(status.state, ConnectorState.NO_OPEN_API)
        self.assertIn("reverse-engineered", status.notes)


if __name__ == "__main__":
    unittest.main()
