from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RepositoryRecoveryContractTests(unittest.TestCase):
    def test_agents_locks_durable_recovery_protocol(self):
        text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("## Durable execution and recovery protocol — LOCKED", text)
        self.assertIn("GitHub's current repository state is the operational source of truth", text)
        self.assertIn("If GitHub facts and `TASK_STATE.md` disagree, GitHub wins.", text)
        self.assertIn("On interruption, timeout, connection loss or a new chat, resume before replanning", text)

    def test_task_state_has_required_operational_sections(self):
        text = (ROOT / "TASK_STATE.md").read_text(encoding="utf-8")
        required = [
            "## Current Mission",
            "## Goal",
            "## Current Unique Commercial Research Goal",
            "## Current Phase",
            "## Last Verified Main",
            "## Active Issue",
            "## Active Branch",
            "## Active PR",
            "## CI",
            "## Latest Artifact / Persisted State",
            "## Completed",
            "## Current Findings",
            "## Blockers",
            "## Next Action",
            "## Do Not Repeat",
            "## Guardrails",
        ]
        for heading in required:
            with self.subTest(heading=heading):
                self.assertIn(heading, text)

    def test_task_state_is_explicitly_subordinate_to_live_github(self):
        text = (ROOT / "TASK_STATE.md").read_text(encoding="utf-8")
        self.assertIn("GitHub live state wins", text)
        self.assertIn("exactly one", (ROOT / "AGENTS.md").read_text(encoding="utf-8"))


    def test_web_session_checkpoint_branch_is_locked(self):
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        protocol = (ROOT / "docs" / "WEB_SESSION_RECOVERY.md").read_text(encoding="utf-8")
        self.assertIn("## Durable web-session checkpoint branch — LOCKED", agents)
        self.assertIn("state/chatgpt-recovery:RECOVERY_STATE.json", agents)
        self.assertIn("live GitHub refs/PRs/Actions/artifacts/persisted data > recovery checkpoint", agents)
        for state in ("FRESH", "STALE", "CONFLICTED"):
            self.assertIn(state, agents)
        self.assertIn("## Atomic checkpoint procedure", protocol)
        self.assertIn("## Mandatory checkpoint boundaries", protocol)
        self.assertIn("## Resume algorithm", protocol)
        self.assertIn("## Crash-window rule", protocol)
        self.assertIn("GitHub Contents API updates use the current blob SHA", protocol)


if __name__ == "__main__":
    unittest.main()
