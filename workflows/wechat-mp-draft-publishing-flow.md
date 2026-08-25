# WeChat Official Account Draft Publishing Flow

**Version**: 0.2
**Status**: Review
**Trigger**: `wechat_article.status=approved`

## Goal

Copy an approved article into the configured WeChat Official Account draft box,
attach an article-specific cover, and ask the owner to perform the final review in
the WeChat backend. This workflow never publishes or broadcasts content.

## State Transition

```text
wechat_article approved
  -> preparing_wechat_draft
  -> generate cover master and wide preview
  -> render Markdown as WeChat-safe HTML
  -> prepare a browser package
  -> open mp.weixin.qq.com and wait for login when required
  -> fill the editor and upload the cover
  -> save one draft after explicit confirmation
  -> wechat_draft_pending_review
  -> notify owner to review in mp.weixin.qq.com
  -> manual edit or manual publish
```

Article approval starts this branch immediately. Video approval is independent and
must not block draft preparation.

## Cover Contract

Generate both files:

- `wechat-cover-square.png`: exactly 900x900 pixels; uploaded as the permanent
  cover material and designed with a center-safe composition.
- `wechat-cover-wide.png`: exactly 900x383 pixels; local preview of the 2.35:1
  main cover crop.

The image must express the article's central mood through a concrete scene. Avoid
generic abstract decoration, stock-photo staging, logos, QR codes, account names,
and baked-in title text unless the reviewer explicitly requests text.

The square master must remain meaningful in both crops:

- `2.35_1`: main article card
- `1_1`: square card and sharing contexts

Use `prompts/wechat-cover-generator.md` for image generation.

## Default Draft Creation: Local Browser

Prepare a validated browser package first:

```bash
python3 scripts/wechat_mp_draft.py \
  --article entries/ENTRY/wechat-article.md \
  --cover-square entries/ENTRY/wechat-cover-square.png \
  --env-file "/Users/wuyanyu/Library/Application Support/LifeOS-AI/wechat-mp.env" \
  --browser-package entries/ENTRY/wechat-browser-package.json
```

The browser runner then:

1. Opens `https://mp.weixin.qq.com/` in the local browser.
2. If the session is expired, sets `login_required`, leaves the page visible, and
   waits for the owner to scan the QR code. It never reads or stores credentials.
3. Opens a new single-article graphic draft and fills title, author, digest, and
   approved body content from the package.
4. Uploads the 900x900 cover and verifies both the 2.35:1 and 1:1 previews.
5. Stops immediately before the final `save as draft` action and requests explicit
   confirmation because saving creates external account content.
6. After confirmation, saves exactly once and verifies a success toast or the
   draft-list entry before setting `pending_review`.

Never infer success from a click alone. A CAPTCHA or account security challenge
sets `wechat_draft_interaction_required` and is handled only by the owner.

## API Fallback

`scripts/wechat_mp_draft.py --dry-run` and the direct API mode remain available
for a future fixed-egress environment. They are not the default on a dynamic home
IP and must not be retried automatically after error 40164.

## Browser Login Gate

Only `WECHAT_MP_AUTHOR` is read from the local env file in browser mode. AppID and
AppSecret are unnecessary. When login is required:

- set `wechat_mp_draft.status=login_required`;
- set `pipeline_status=wechat_draft_login_required`;
- preserve the package, cover, and article;
- notify once and keep the login tab available;
- resume only after the authenticated dashboard is visible.

## Success Notification

Send one Feishu message:

```text
【微信公众号草稿待审核】
条目：ENTRY
状态：已写入草稿箱
封面：2.35:1 + 1:1 已配置
请前往 https://mp.weixin.qq.com/ 检查标题、摘要、正文、封面裁剪和隐私信息。
系统不会自动发布。
```

## Idempotency

- Store `browser_package_fingerprint` before opening the editor.
- If the same fingerprint has status `pending_review`, do not create another draft.
- While status is `editing` or `save_confirmation_required`, resume the existing
  editor tab; do not open a new draft.
- A save timeout is `save_verification_required`, not success. Inspect the draft
  list before any retry.
- A revised approved article increments the draft revision and updates or replaces
  only the WeChat draft branch.
- Persist API errors without secrets, access tokens, or raw credential responses.

## Acceptance Tests

1. Pending or rejected articles never create a WeChat draft.
2. Article approval queues `prepare_wechat_draft` even when video review is pending.
3. Both official crop ratios are included.
4. An expired login creates a visible login gate, not a false success.
5. Reprocessing the same action does not create a duplicate draft.
6. Success produces one Feishu review reminder and never publishes the article.
7. CAPTCHA and security prompts stop for owner interaction.
