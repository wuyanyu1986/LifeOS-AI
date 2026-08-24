# Video Diary Script Copy Generation Flow

This workflow turns a standard parsed daily reflection note into a short-video script and copy draft.

## Position In The Full Pipeline

Use this as step two:

```text
audio recording
  -> transcription
  -> standard parsed note
  -> video script and copy
```

Do not skip the standard parsed note unless the user explicitly asks for a quick draft.

## Input

Required:

- Standard parsed note
- Recording date
- Intended video length
- Desired tone

Optional:

- Platform
- Privacy constraints
- Whether medical or location details should be removed
- Whether the script should be personal, educational, or narrative

## Standard Output Shape

The preferred output is:

```text
时长：约 X 分钟 / 风格：XXXX

（音乐或画面提示）

可直接口播的正文脚本

## 发布文案

## 标题备选

## 拍摄提示
```

## Step 1: Read The Parsed Note

Extract:

- core event
- emotional turn
- key sensory details
- original quotes
- final insight
- privacy risks

For the current `每日成长` style, useful source sections are:

- 智能总结
- 章节概要
- 金句精选
- 处理说明

## Step 2: Choose The Emotional Spine

Pick one clear emotional spine.

Examples:

- from rushing to allowing slowness
- from inconvenience to being seen
- from physical limitation to new perception
- from everyday detail to quiet warmth

Do not combine too many themes in one short video.

## Step 3: Draft The Script

Use this structure:

1. Hook: a concrete question or conflict.
2. Context: date, situation, place, limitation.
3. Scene: what happened step by step.
4. Detail: sensory observation and specific action.
5. Human moment: dialogue or interaction.
6. Realization: restrained personal insight.
7. Closing line: memorable but not slogan-like.

## Step 4: Add Minimal Production Cues

Add only useful cues:

- background music entrance
- music lift/drop
- pause
- simple picture direction

Avoid over-directing every sentence.

## Step 5: Add Publishing Copy

The publishing copy should:

- summarize the video in 80-150 Chinese characters
- preserve privacy
- avoid clickbait
- invite resonance without forcing engagement

## Step 6: Add Title Options

Generate 5 title options.

Good titles are:

- specific
- scene-based
- emotionally clear
- not sensational

## Step 7: Add Shooting Notes

Include:

- privacy constraints
- suggested visuals
- voice tone
- what not to show

## Feishu Creation

Create the video script as a child document under the daily parsed note:

```bash
lark-cli docs +create \
  --profile siyangyuan-tiantu \
  --as user \
  --title "YYYY-MM-DD 视频脚本和视频文案" \
  --wiki-node "DAILY_NOTE_WIKI_NODE_TOKEN" \
  --markdown @entries/YYYY-MM-DD-daily-reflection/video-script-and-copy.md
```

For a process/spec document, create it under the sample video script node or the project process node.

## Quality Checklist

- [ ] Script is first-person.
- [ ] Opening hook is concrete.
- [ ] Story has a clear beginning, middle, and ending.
- [ ] At least one sensory detail is included.
- [ ] Any dialogue comes from the source note.
- [ ] Final insight is restrained.
- [ ] Publishing copy is included.
- [ ] Title options are included.
- [ ] Shooting notes include privacy handling.

