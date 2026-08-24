---
name: video-diary-script-copy-generator
version: 0.1.0
description: "将飞书「每日成长」标准解析稿转化为可直接口播/配音的短视频脚本、发布文案、标题备选和拍摄提示。"
---

# Video Diary Script Copy Generator

Use this skill after a daily reflection recording has already been parsed into the standard `每日成长` format.

## Goal

Create a directly recordable short-video script and copy draft from a standard parsed note.

This skill is downstream of `audio-diary-standard-parser`.

## Required Input

- Standard parsed note
- Desired video length
- Desired tone
- Privacy preference

## Output Structure

Always output:

```text
时长：约 X 分钟 / 风格：XXXX

（音乐或画面提示）

正文口播脚本

## 发布文案

## 标题备选

## 拍摄提示
```

## Processing Rules

1. Use first-person narration.
2. Preserve real events, details, dialogue, and feelings.
3. Start with a concrete hook or conflict.
4. Include scene, action, bodily feeling, environment, and interaction.
5. Use sensory details when the source supports them.
6. Let the insight emerge from the story.
7. Avoid motivational over-writing.
8. Avoid platform-marketing language unless explicitly requested.
9. Protect private medical, location, identity, and license plate details.
10. Do not invent dialogue or facts.

## Script Structure

Use this narrative pattern:

1. Hook
2. Context
3. Scene
4. Friction or difficulty
5. Human interaction
6. Reflection
7. Closing line

## Style Standard

The final script should feel like:

- quiet first-person monologue
- direct enough to record
- concrete enough to visualize
- restrained enough to remain believable

It should not feel like:

- a knowledge-base summary
- a motivational speech
- a product ad
- a medical essay
- a generic social media caption

## Reference Prompt

Use `prompts/video-diary-script-copy-generator.md` as the full prompt template.

## Reference Workflow

Use `workflows/video-diary-script-copy-generation-flow.md` for the end-to-end process.

