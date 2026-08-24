# Review-Gated Diary Orchestration

**Version**: 0.1  
**Status**: Draft  
**Trigger**: A new date document is detected under the `每日成长` Wiki root.

## Goal

Require explicit human approval of the standard parsed note before generating derivative content. Notify and review the video script and WeChat article independently.

## Actors

| Actor | Responsibility |
| --- | --- |
| Wiki scanner | Detect new date documents and deduplicate them |
| Review orchestrator | Persist state and enforce review gates |
| Feishu bot | Send reminders and receive review commands |
| Reviewer | Approve or request changes |
| Content generators | Create video and article drafts after approval |

## Trigger Strategy

### MVP

Poll the direct children of Wiki root `YCRZwOZ8GibC7pkt9L1cHh8enXf` every 60 seconds.

Accept a node only when:

- `obj_type` is `docx`;
- title matches `YYYY-MM-DD` or `YYYY-MM-DD-N` for multiple recordings on the same date;
- its `node_token` is not in the local review registry.

The scanner is the source of detection, not the source of approval.

### Future Optimization

Replace polling with a native Wiki/Drive creation event only after the event is confirmed available for the app. Keep a periodic reconciliation scan even after event delivery is enabled.

## Happy Path

```text
new parsed note detected
  -> parsed_pending_review
  -> send parsed-note review reminder
  -> reviewer approves
  -> generating_derivatives
     -> create video script -> send video review reminder
     -> create WeChat article -> send article review reminder
  -> derivatives_pending_review
     -> video approved independently
     -> article approved independently
  -> completed
```

## Hard Gates

1. `parsed_note.status` must equal `approved` before either derivative generator can run.
2. Video approval never implies article approval, and article approval never implies video approval.
3. `pipeline_status` becomes `completed` only when both derivative statuses equal `approved`.
4. A change request updates only the affected output and increments its revision.

## Review Commands

MVP commands received in the bot conversation:

```text
通过 YYYY-MM-DD 标准解析稿
修改 YYYY-MM-DD 标准解析稿：修改意见
通过 YYYY-MM-DD 视频脚本
修改 YYYY-MM-DD 视频脚本：修改意见
通过 YYYY-MM-DD 公众号文章
修改 YYYY-MM-DD 公众号文章：修改意见
```

Reject ambiguous commands and reply with the accepted syntax. Only the configured reviewer may change review state.

## Notification Rules

- Parsed note: send one `待审核` message after first detection.
- Video script: send a separate `待审核` message after creation or revision.
- WeChat article: send a separate `待审核` message after creation or revision.
- Use an idempotency key composed of `stage + wiki_node_token + revision`.
- Retry transient send failures three times with backoff; persist `notification_status=failed` after the final attempt.

Every reminder must contain the date, content type, document link, revision, current status, and accepted review commands.

## Failure And Recovery

| Failure | Required behavior |
| --- | --- |
| Wiki list timeout | Retry; do not alter review state |
| Duplicate detection | Return existing state; do not notify again |
| Parsed note fetch fails | Mark processing failure and retry; do not generate content |
| Reminder send fails | Keep content pending review and retry notification |
| One derivative fails | Preserve the successful sibling; retry only the failed branch |
| Invalid reviewer command | Keep existing state and send syntax guidance |
| Concurrent approvals | First valid transition wins; later duplicates are idempotent |

## Persistence

Persist one state record per date using `schemas/review-state.schema.json`. The Wiki node token is the stable external identifier. Store raw audio and transcripts locally; never include them in review messages.

## Assumptions

- MVP uses polling because a Wiki child-created event has not been confirmed for the current app.
- The bot has one configured reviewer or review chat.
- Review messages use bot identity; Wiki reads and writes continue using `siyangyuan-tiantu --as user`.

## Acceptance Tests

1. A new date node causes exactly one parsed-note reminder.
2. No derivative is created before parsed-note approval.
3. Parsed-note approval creates both derivative jobs.
4. Video and article each produce their own reminder.
5. Requesting changes to one derivative does not regenerate the other.
6. Re-running the scanner creates no duplicate reminders or documents.
7. The pipeline completes only after both derivative approvals.
