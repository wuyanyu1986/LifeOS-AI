import json
import tempfile
import unittest
from pathlib import Path

from scripts.review_message_listener import (
    apply_review_command,
    build_acknowledgement,
    find_review_state,
    parse_review_command,
)


class ReviewMessageListenerTest(unittest.TestCase):
    def test_find_review_state_by_entry_date_for_named_recording(self):
        with tempfile.TemporaryDirectory() as directory:
            entries_dir = Path(directory)
            state_path = entries_dir / "2026-08-28-召楼路-8" / "review-state.json"
            state_path.parent.mkdir()
            state_path.write_text(
                json.dumps({"entry_date": "2026-08-28"}), encoding="utf-8"
            )

            self.assertEqual(
                find_review_state(entries_dir, "2026-08-28"), state_path
            )

    def test_find_review_state_rejects_ambiguous_date(self):
        with tempfile.TemporaryDirectory() as directory:
            entries_dir = Path(directory)
            for suffix in ("morning", "evening"):
                state_path = entries_dir / f"2026-08-28-{suffix}" / "review-state.json"
                state_path.parent.mkdir()
                state_path.write_text(
                    json.dumps({"entry_date": "2026-08-28"}), encoding="utf-8"
                )

            self.assertIsNone(find_review_state(entries_dir, "2026-08-28"))

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

    def test_parse_command_copied_with_literal_newline_escapes(self):
        self.assertEqual(
            parse_review_command(r"\n通过 2026-08-24-2 公众号文章\n\n"),
            {
                "decision": "approved",
                "entry_key": "2026-08-24-2",
                "stage": "wechat_article",
                "comment": "",
            },
        )

    def test_all_reviews_completed_acknowledgement_is_manual(self):
        acknowledgement = build_acknowledgement(
            {
                "decision": "approved",
                "entry_key": "2026-08-24-2",
                "stage": "wechat_article",
                "comment": "",
            },
            {"action": "all_reviews_completed"},
        )
        self.assertIn("均已就绪", acknowledgement)
        self.assertIn("手工写入", acknowledgement)

    def test_article_approval_completes_reviews_without_draft_branch(self):
        with tempfile.TemporaryDirectory() as directory:
            state_path = Path(directory) / "review-state.json"
            state_path.write_text(
                json.dumps(
                    {
                        "pipeline_status": "derivatives_pending_review",
                        "parsed_note": {"status": "approved"},
                        "video_script": {"status": "approved"},
                        "wechat_article": {
                            "status": "pending_review",
                            "reviewer_open_id": None,
                            "reviewed_at": None,
                            "review_comment": None,
                        },
                    }
                ),
                encoding="utf-8",
            )
            result = apply_review_command(
                state_path,
                {
                    "decision": "approved",
                    "entry_key": "2026-08-24-2",
                    "stage": "wechat_article",
                    "comment": "",
                },
                "ou_reviewer",
            )
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(result["action"], "all_reviews_completed")
            self.assertEqual(state["pipeline_status"], "ready_for_manual_publish")

    def test_video_approval_completes_reviews_when_article_is_approved(self):
        acknowledgement = build_acknowledgement(
            {
                "decision": "approved",
                "entry_key": "2026-08-24-2",
                "stage": "video_script",
                "comment": "",
            },
            {"action": "all_reviews_completed"},
        )
        self.assertIn("手工写入", acknowledgement)

    def test_approvals_wait_for_current_cover_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            state_path = Path(directory) / "review-state.json"
            state_path.write_text(
                json.dumps(
                    {
                        "pipeline_status": "derivatives_pending_review",
                        "parsed_note": {"status": "approved"},
                        "video_script": {"status": "approved"},
                        "wechat_article": {
                            "status": "pending_review",
                            "revision": 2,
                            "reviewer_open_id": None,
                            "reviewed_at": None,
                            "review_comment": None,
                        },
                        "cover_assets": {
                            "status": "archived",
                            "source_article_revision": 1,
                        },
                    }
                ),
                encoding="utf-8",
            )
            result = apply_review_command(
                state_path,
                {
                    "decision": "approved",
                    "entry_key": "2026-08-24-2",
                    "stage": "wechat_article",
                    "comment": "",
                },
                "ou_reviewer",
            )
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(result["action"], "wait_for_cover_assets")
            self.assertEqual(state["pipeline_status"], "generating_derivatives")

    def test_article_change_supersedes_cover_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            state_path = Path(directory) / "review-state.json"
            state_path.write_text(
                json.dumps(
                    {
                        "pipeline_status": "derivatives_pending_review",
                        "parsed_note": {"status": "approved"},
                        "video_script": {"status": "approved"},
                        "wechat_article": {
                            "status": "pending_review",
                            "revision": 1,
                            "reviewer_open_id": None,
                            "reviewed_at": None,
                            "review_comment": None,
                        },
                        "cover_assets": {
                            "status": "archived",
                            "source_article_revision": 1,
                        },
                    }
                ),
                encoding="utf-8",
            )
            apply_review_command(
                state_path,
                {
                    "decision": "changes_requested",
                    "entry_key": "2026-08-24-2",
                    "stage": "wechat_article",
                    "comment": "修改观点",
                },
                "ou_reviewer",
            )
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state["cover_assets"]["status"], "superseded")

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
