# WeChat Article Review

**Version**: 0.1  
**Status**: Draft

## Prerequisite

`parsed_note.status=approved`.

## Flow

1. Generate the article from the approved parsed-note revision.
2. Create or update the WeChat article child document.
3. Set `wechat_article.status=pending_review`.
4. Send a dedicated `公众号文章待审核` Feishu message with the document link.
5. On approval, set `wechat_article.status=approved` and queue `prepare_wechat_draft`.
6. On change request, revise only the article document, increment its revision, and send a new article reminder.

Approval does not publish the article. It starts
`workflows/wechat-mp-draft-publishing-flow.md`, which creates a cover and a draft
for final review in the WeChat backend.

## Review Checklist

- The article has one clear and supportable viewpoint.
- The body is approximately 1800-2200 Chinese characters.
- Facts remain faithful to the approved parsed note.
- The article does not mechanically stretch the video script.
- Privacy-sensitive details are acceptable for public publishing.
