# Storage Locations

This file records the current local input location and Feishu output destination for the v0.2 manual video diary workflow.

## Recording Input

Local recording folder:

```text
/Users/wuyanyu/Desktop/每日感想录音记录
```

Current detected recording:

```text
/Users/wuyanyu/Desktop/每日感想录音记录/2026:08:24.m4a
```

Detected audio metadata:

- Format: M4A / AAC
- Channels: 2
- Sample rate: 48000 Hz
- Estimated duration: 271.36 seconds
- Size: 4.3 MB

## Final Content Output

Feishu wiki destination:

```text
https://jp09qsvu8c.feishu.cn/wiki/YCRZwOZ8GibC7pkt9L1cHh8enXf?fromScene=spaceOverview
```

Target behavior:

- Create one child document under this wiki node for each processed diary entry.
- Use the date as the document title.
- Store the final reviewed journal content in that document.

Example title:

```text
2026-08-24
```

## Access Status

Local recording folder:

- Status: readable
- Checked on: 2026-08-24

Feishu wiki destination:

- Status: blocked
- Reason: current `lark-cli` identity is bot only, and the wiki API returned `node permission denied`.
- Required next step: authorize user identity with at least `wiki:node:read`, then retry node lookup.

## Privacy Rule

Real diary transcripts and final local journal drafts should be created under local `entries/` and remain ignored by Git. Only reusable templates, schemas, workflows, and non-private examples should be committed.

