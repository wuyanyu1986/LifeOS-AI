import json
import tempfile
import unittest
from pathlib import Path

from scripts.review_message_listener import (
    apply_review_command,
    parse_review_command,
)


class ReviewMessageListenerTest(unittest.TestCase):
    def test_parse_approve_command(self):
        self.assertEqual(
            parse_review_command("通过 2026-08-24-1 标准解析稿"),
            {
                "decision": "approved",
                "entry_key": "2026-08-24-1",
                "stage": "parsed_note",
                "comment": "",
            },
        )

    def test_change_request_requires_comment(self):
        self.assertIsNone(parse_review_command("修改 2026-08-24-1 视频脚本"))

    def test_parsed_approval_queues_derivative_generation(self):
        with tempfile.TemporaryDirectory() as directory:
            state_path = Path(directory) / "review-state.json"
            state_path.write_text(
                json.dumps(
                    {
                        "pipeline_status": "parsed_pending_review",
                        "parsed_note": {
                            "status": "pending_review",
                            "reviewer_open_id": None,
                            "reviewed_at": None,
                            "review_comment": None,
                        },
                        "video_script": {"status": "not_created"},
                        "wechat_article": {"status": "not_created"},
                    }
                ),
                encoding="utf-8",
            )
            result = apply_review_command(
                state_path,
                {
                    "decision": "approved",
                    "entry_key": "2026-08-24-1",
                    "stage": "parsed_note",
                    "comment": "",
                },
                "ou_reviewer",
            )
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertTrue(result["changed"])
            self.assertEqual(result["action"], "generate_derivatives")
            self.assertEqual(state["parsed_note"]["status"], "approved")
            self.assertEqual(state["pipeline_status"], "generating_derivatives")


if __name__ == "__main__":
    unittest.main()
