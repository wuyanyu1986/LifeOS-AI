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

## Output Structure

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

