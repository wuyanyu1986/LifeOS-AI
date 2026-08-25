# Decision 002: WeChat Integration Stops At The Draft Box

**Status**: Accepted

## Decision

After a LifeOS WeChat article is approved in Feishu, the system may generate a
cover and create a WeChat Official Account draft. It may not publish, mass-send,
schedule, or delete WeChat content.

The default draft-creation path is local browser automation. Direct API creation
is a fallback for a future environment with stable, allowlisted public egress.
Browser automation must stop for QR login, CAPTCHA, security challenges, and the
final save confirmation.

## Reason

The WeChat backend is the final place where the account owner can inspect platform
rendering, cover crops, title limits, privacy details, and any manual edits. Keeping
publication outside the automation prevents an upstream review mistake from
becoming a public post.

## Consequence

`wechat_article.status=approved` is no longer the end of the article branch. The
terminal automated state is `wechat_draft_pending_review`; publication remains a
manual external action. The browser package fingerprint and verified save result
form the duplicate-prevention boundary.
