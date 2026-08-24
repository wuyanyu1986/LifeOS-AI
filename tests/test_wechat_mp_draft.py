import tempfile
import unittest
from pathlib import Path

from scripts.wechat_mp_draft import Article, build_draft_payload, extract_article


class WeChatMPDraftTest(unittest.TestCase):
    def test_extracts_publishable_article_and_omits_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            article_path = Path(directory) / "article.md"
            article_path.write_text(
                """> ✅ 审核状态：已通过

# 一个测试标题

> 这是一段摘要。

正文第一段。

## 小标题

正文第二段。

---

## 备选标题

1. 不应进入正文
""",
                encoding="utf-8",
            )
            article = extract_article(article_path)
            self.assertEqual(article.title, "一个测试标题")
            self.assertEqual(article.digest, "这是一段摘要。")
            self.assertIn("正文第二段", article.html)
            self.assertNotIn("备选标题", article.html)

    def test_payload_contains_supported_cover_crops(self):
        payload = build_draft_payload(
            Article("标题", "摘要", "<p>正文</p>"), "作者", "media-id"
        )
        article = payload["articles"][0]
        ratios = {
            item["ratio"] for item in article["cover_info"]["crop_percent_list"]
        }
        self.assertEqual(article["thumb_media_id"], "media-id")
        self.assertEqual(ratios, {"2.35_1", "1_1"})


if __name__ == "__main__":
    unittest.main()
