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
5. On approval, set `wechat_article.status=approved`. The publishing branch stops,
   while the cover branch may finish or refresh the platform cover assets.
6. On change request, revise only the article document, increment its revision, and send a new article reminder.

Approval does not publish or copy the article to any external platform. The owner
manually writes the approved article into the WeChat Official Account backend.

If a change request alters the title, central viewpoint, or cover summary, mark
the current `cover_assets` as `superseded` and regenerate only the cover branch
after the revised article is ready.

## Review Checklist

- The article has one clear and supportable viewpoint.
- The body is approximately 1800-2200 Chinese characters.
- Facts remain faithful to the approved parsed note.
- The article does not mechanically stretch the video script.
- Privacy-sensitive details are acceptable for public publishing.
