# WeChat Official Account Draft Publishing Flow

**Version**: 0.1
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
  -> upload permanent cover material
  -> create draft
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

## Draft Creation

Run a validation preview first:

```bash
python3 scripts/wechat_mp_draft.py \
  --article entries/ENTRY/wechat-article.md \
  --cover-square entries/ENTRY/wechat-cover-square.png \
  --env-file "/Users/wuyanyu/Library/Application Support/LifeOS-AI/wechat-mp.env" \
  --dry-run
```

After validation, remove `--dry-run`. The client:

1. Gets a stable access token using a server-side POST request.
2. Uploads the square cover as permanent image material.
3. Uses the returned `media_id` as `thumb_media_id`.
4. Creates one `news` item in the draft box.
5. Returns only material and draft IDs; it never prints credentials or tokens.

## Configuration Gate

Credentials must exist only in:

```text
/Users/wuyanyu/Library/Application Support/LifeOS-AI/wechat-mp.env
```

Required values:

```text
WECHAT_MP_APP_ID=...
WECHAT_MP_APP_SECRET=...
WECHAT_MP_AUTHOR=...
```

The file must be mode `600`. The calling IP must be accepted by the WeChat account
when the platform requires administrator confirmation or an IP allowlist.

When configuration is absent:

- set `wechat_mp_draft.status=configuration_required`;
- set `pipeline_status=wechat_draft_configuration_required`;
- preserve the generated cover and rendered article;
- notify once, without repeated retries or duplicate drafts.

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

- If `draft_media_id` already exists for the same article revision, do not call
  `draft/add` again.
- A revised approved article increments the draft revision and updates or replaces
  only the WeChat draft branch.
- Persist API errors without secrets, access tokens, or raw credential responses.

## Acceptance Tests

1. Pending or rejected articles never create a WeChat draft.
2. Article approval queues `prepare_wechat_draft` even when video review is pending.
3. Both official crop ratios are included.
4. Missing credentials create a visible configuration gate, not a false success.
5. Reprocessing the same action does not create a duplicate draft.
6. Success produces one Feishu review reminder and never publishes the article.
