# Review Notification Configuration

## Fixed Scope

- Wiki profile: `siyangyuan-tiantu`
- Wiki identity: `user`
- Wiki root node: `YCRZwOZ8GibC7pkt9L1cHh8enXf`
- Wiki space ID: `7618037226496543945`
- Detection interval: 60 seconds

## Required Before Runtime

Configure exactly one notification destination:

```text
reviewer_open_id: TO_BE_CONFIGURED
review_chat_id: TO_BE_CONFIGURED
```

Only one is required. Prefer a direct message to the reviewer for the MVP.

## Identity Split

- Wiki listing, reading, creation, and update: `--profile siyangyuan-tiantu --as user`
- Review reminder sending and review-command events: `--profile siyangyuan-tiantu --as bot`

## Message Types

1. `标准解析稿待审核`
2. `视频脚本待审核`
3. `公众号文章待审核`
4. `修改完成，请重新审核`
5. `本条日记全部审核完成`

Do not send reminders until the reviewer or review chat is explicitly configured and verified.
