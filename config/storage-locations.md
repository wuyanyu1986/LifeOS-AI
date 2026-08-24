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

- Status: readable and writable
- Checked profile: `siyangyuan-tiantu`
- Checked user: 饲养员本员
- Wiki title: 每日成长
- Wiki node token: `YCRZwOZ8GibC7pkt9L1cHh8enXf`
- Wiki space ID: `7618037226496543945`

Created document for the first processed entry:

```text
2026-08-24
https://jp09qsvu8c.feishu.cn/wiki/UvW0wnogNisxYpkCtXtcMArangb
```

## Privacy Rule

Real diary transcripts and final local journal drafts should be created under local `entries/` and remain ignored by Git. Only reusable templates, schemas, workflows, and non-private examples should be committed.
