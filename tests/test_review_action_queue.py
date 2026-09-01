import json
import tempfile
import unittest
from pathlib import Path

from scripts.review_action_queue import acknowledge_action, pending_actions


class ReviewActionQueueTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.queue = self.root / "actions.ndjson"
        self.cursor = self.root / "cursor.json"
        self.queue.write_text(
            "\n".join(
                [
                    json.dumps(
                        {
                            "created_at": "2026-08-25T01:00:00+00:00",
                            "entry_key": "2026-08-25",
                            "action": "generate_derivatives",
                            "message_id": "one",
                        }
                    ),
                    json.dumps(
                        {
                            "created_at": "2026-08-25T02:00:00+00:00",
                            "entry_key": "2026-08-25",
                            "action": "wait_for_sibling_review",
                            "message_id": "two",
                        }
                    ),
                ]
            )
            + "\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temporary.cleanup()

    def test_pending_does_not_advance_cursor(self):
        pending = pending_actions([self.queue], self.cursor)
        self.assertEqual([item["line"] for item in pending], [1, 2])
        self.assertFalse(self.cursor.exists())

    def test_acknowledgement_advances_exactly_one_action(self):
        result = acknowledge_action(self.cursor, self.queue, 1)
        self.assertTrue(result["changed"])
        self.assertEqual(pending_actions([self.queue], self.cursor)[0]["line"], 2)
        cursor = json.loads(self.cursor.read_text(encoding="utf-8"))
        self.assertEqual(cursor["last_consumed_message_id"], "one")

    def test_acknowledgement_cannot_skip_action(self):
        with self.assertRaisesRegex(ValueError, "cannot skip"):
            acknowledge_action(self.cursor, self.queue, 2)


if __name__ == "__main__":
    unittest.main()
