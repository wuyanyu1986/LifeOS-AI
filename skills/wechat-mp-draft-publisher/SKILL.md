---
name: wechat-mp-draft-publisher
description: Create a WeChat Official Account draft from an approved LifeOS article, including an article-specific cover and final manual review notification. Never publishes content.
---

# WeChat MP Draft Publisher

## Trigger

Run only when `wechat_article.status` equals `approved` and the unconsumed action is
`prepare_wechat_draft`.

## Required Reading

1. `workflows/wechat-mp-draft-publishing-flow.md`
2. `prompts/wechat-cover-generator.md`
3. The approved `wechat-article.md`
4. The entry's `review-state.json`

## Procedure

1. Refuse to run if the article is not approved.
2. Generate a center-safe square cover based on the article's central mood.
3. Produce exact 900x900 and 900x383 PNG files.
4. Run `scripts/wechat_mp_draft.py --dry-run`.
5. If local credentials are missing, persist `configuration_required` and notify
   once. Never request that the secret be pasted into chat.
6. Otherwise create the draft and persist `cover_media_id` and `draft_media_id`.
7. Set `wechat_mp_draft.status=pending_review` and
   `pipeline_status=wechat_draft_pending_review`.
8. Notify the owner to perform the final review at `https://mp.weixin.qq.com/`.

## Safety

- Never call publish or mass-send APIs.
- Never print AppSecret, access tokens, or credential files.
- Never create a second draft for the same article revision.
- Keep video review independent from this branch.
