# Review-Gated Diary Orchestration

**Version**: 0.1  
**Status**: Draft  
**Trigger**: A new date document is detected under the `每日成长` Wiki root.

## Goal

Require explicit human approval of the standard parsed note before generating
derivative content. Run the Viral Writer strategy layer, then generate video,
WeChat, Xiaohongshu, Douyin, and cover branches independently; notify and
review each selected content branch independently.

## Actors

| Actor | Responsibility |
| --- | --- |
| Wiki scanner | Detect new date documents and deduplicate them |
| Review orchestrator | Persist state and enforce review gates |
| Feishu bot | Send reminders and receive review commands |
| Reviewer | Approve or request changes |
| Content generators | Create video, article, and cross-platform cover assets after approval |

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
     -> Viral Writer strategy
     -> create selected platform branches -> send independent review reminders
     -> create cover brief -> wait for article metadata -> render platform covers
        -> create a cover child page under the article -> upload three images
  -> derivatives_pending_review
     -> video approved independently
     -> article approved independently
     -> current cover assets archived
  -> ready_for_manual_publish
  -> owner manually writes and publishes the approved article
```

## Hard Gates

1. `parsed_note.status` must equal `approved` before any derivative generator can run.
2. Video approval never implies article approval, and article approval never implies video approval.
3. Article approval never writes to the WeChat Official Account backend.
4. The automated pipeline stops at `ready_for_manual_publish` after all
   selected content approvals plus current-revision visual archival.
5. A change request updates only the affected output and increments its revision.

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
- Cover assets: send one `已生成` message after the child page contains all three images.
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
| One derivative fails | Preserve successful siblings; retry only the failed branch |
| Cover image upload partially fails | Keep the child page and retry only missing images |
| Invalid reviewer command | Keep existing state and send syntax guidance |
| Concurrent approvals | First valid transition wins; later duplicates are idempotent |

## Persistence

Persist one state record per date using `schemas/review-state.schema.json`. The Wiki node token is the stable external identifier. Store raw audio and transcripts locally; never include them in review messages.

Review actions are a durable queue, not a notification-only log. Every automation
run must call:

```bash
python3 scripts/review_action_queue.py pending
```

Process pending actions in order. Advance the source cursor only after the action
has completed successfully:

```bash
python3 scripts/review_action_queue.py ack \
  --queue "/absolute/path/to/review-actions.ndjson" \
  --line ACTION_LINE
```

Never acknowledge an action before its requested documents, state transitions,
uploads, and notifications have settled. A failed run must leave the action
pending for the next reconciliation run.

## Assumptions

- MVP uses polling because a Wiki child-created event has not been confirmed for the current app.
- The bot has one configured reviewer or review chat.
- Review messages use bot identity; Wiki reads and writes continue using `siyangyuan-tiantu --as user`.

## Acceptance Tests

1. A new date node causes exactly one parsed-note reminder.
2. No derivative is created before parsed-note approval.
3. Parsed-note approval creates three derivative jobs.
4. Video and article each produce review reminders; cover completion produces an informational reminder.
5. Requesting changes to one derivative does not regenerate the other.
6. Re-running the scanner creates no duplicate reminders or documents.
7. Article approval never creates a WeChat draft or opens a platform backend.
8. All selected content approvals plus current-revision visual archival set
   `ready_for_manual_publish`.
