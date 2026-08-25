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
4. Generate `wechat-browser-package.json` with
   `scripts/wechat_mp_draft.py --browser-package`.
5. Open the local browser at `mp.weixin.qq.com`. If login is required, persist
   `login_required`, show the QR page, and wait for the owner.
6. Fill one new draft from the package and upload the square cover.
7. Stop before `save as draft` and obtain explicit action-time confirmation.
8. Save once, verify success, and persist the package fingerprint. Do not treat a
   click or timeout as proof that a draft exists.
9. Set `wechat_mp_draft.status=pending_review` and
   `pipeline_status=wechat_draft_pending_review`.
10. Notify the owner to perform the final review at `https://mp.weixin.qq.com/`.

## Safety

- Never call publish or mass-send APIs.
- Never print AppSecret, access tokens, or credential files.
- Never create a second draft for the same article revision.
- Never solve a CAPTCHA or security challenge without the owner's confirmation.
- Never read or store browser passwords, cookies, or login tokens.
- Keep video review independent from this branch.
