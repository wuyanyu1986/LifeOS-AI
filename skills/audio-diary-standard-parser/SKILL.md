---
name: audio-diary-standard-parser
version: 0.1.0
description: "将每日感想录音转写文本整理成飞书「每日成长」知识库标准解析格式：智能总结、章节概要、金句精选、待办事项和处理说明。"
---

# Audio Diary Standard Parser

Use this skill after a daily reflection recording has been transcribed.

## Goal

Turn raw speech-to-text output into the standard `每日成长` Feishu note format.

This skill does not create a video script. It creates a structured parsed note.

## Required Input

- Recording date
- Recording duration
- Speaker count
- Raw transcript
- Timestamped transcript if available
- Privacy preference

## Output Files

每次解析必须同时生成两个文件：

1. `current-content.md`：当前可供用户审核、归档和下游内容生成的整理稿。
2. `audio-parse-unabridged.md`：基于音频转写的无删减解析稿，保留原始表达、重复、停顿标记、未决信息和完整时间顺序；只允许修复明确的 ASR 错字，不做摘要、不删减、不润色。

`current-content.md` 可以被用户修改；`audio-parse-unabridged.md` 是不可变的来源档案。下游内容生成只读取审核通过的 `current-content.md`，需要核对原话时再读取无删减档案。

## Current Content Structure

Always output:

```text
### 📑 智能总结
#### 录音信息
#### 录音总结
#### 主题段落

### 📅 章节概要

### ✨ 金句精选

### 📋 待办事项

### 🔍 处理说明
```

在 `current-content.md` 顶部记录：`source_unabridged_file`、`source_revision` 和 `content_revision`。

## Unabridged Parse Rules

- 按音频时间顺序保留全部可辨识内容，包括重复、口头语和自我修正。
- 不把推测补成事实；听不清处写 `[听不清 00:12:03]`。
- 不为了可读性删除内容；必要的隐私遮罩必须记录在处理说明中。
- 无删减稿不进入公开内容生成，也不作为公开内容的默认展示稿。

## Processing Rules

1. Do not invent facts.
2. Correct obvious ASR mistakes conservatively.
3. Keep real time, place, people, actions, feelings, and quotes when they matter.
4. Mark uncertain information explicitly.
5. Avoid motivational over-writing.
6. Do not transform the content into a video script.
7. Keep the user's own wording for quote-worthy lines.

## Section Requirements

### 智能总结

Include recording metadata and a concise overview.

Then group the content into thematic sections. Each thematic section should use this style:

```text
#### 主题标题

- **要点标题**：具体解释。
- **要点标题**：具体解释。
```

### 章节概要

Use chronological order.

Format:

```text
00:00:01 **章节标题** 摘要内容。
```

If exact timestamps are unavailable, estimate and mark as approximate.

### 金句精选

Extract 3-6 quote-worthy lines.

Format:

```text
- “原话内容。” (类型)
```

Allowed types:

- 情绪共鸣
- 思考启发
- 人生感悟
- 行动提醒
- 关系洞察
- 创作素材

### 待办事项

Only include explicit actions from the recording.

If there are no explicit actions:

```text
无
```

### 处理说明

Briefly document:

- ASR corrections
- uncertain information
- privacy handling

## Reference Prompt

Use `prompts/audio-diary-standard-parser.md` as the full prompt template.

## Reference Workflow

Use `workflows/audio-diary-standard-processing-flow.md` for the end-to-end local and Feishu process.
