# Standard Parsed Note Review

**Version**: 0.1  
**Status**: Draft

## Trigger

The Wiki scanner detects a new direct child document whose title matches `YYYY-MM-DD` under `每日成长`.

## Flow

1. Fetch and validate the parsed note structure.
2. Create a review-state record with `parsed_note.status=pending_review`.
3. Insert a visible `🟡 审核状态：待审核` marker at the top of the Feishu document.
4. Send a Feishu message titled `标准解析稿待审核` with the document link.
5. Wait for an explicit approve or change-request command from the configured reviewer.
6. On approval, set `parsed_note.status=approved`, update the document marker to `✅ 审核状态：已通过`, and start both derivative generators.
7. On change request, set `parsed_note.status=changes_requested`, update the marker to `⚠️ 审核状态：需修改`, retain the feedback, revise the same document, increment the revision, and notify again.

## Review Checklist

- Events, people, dialogue, and chronology are faithful to the recording.
- Uncertain information is not written as fact.
- Summary, chapter outline, quotes, and action items follow the standard structure.
- Sensitive details are handled according to the user's intent.
- No downstream content exists before approval.
