---
name: wechat-article-generator
description: "将每日感想的标准解析稿延展为有明确观点、阅读时长约4-5分钟的公众号文章，并生成备选标题和封面摘要。用于录音已完成转写和标准解析，需要形成公众号长文、观点文章或图文发布稿时。"
---

# WeChat Article Generator

Generate the article directly from the standard parsed note. Treat an existing video script only as a voice reference, not as the factual source.

## Required Input

- Standard parsed note
- Recording date
- Privacy constraints
- Target reading time, default 4-5 minutes

## Workflow

1. Separate verified facts, original dialogue, sensory details, emotional changes, and privacy risks.
2. Choose one central viewpoint that is supported by the event and broader than a diary summary.
3. Build the article from concrete scene to event, turn, reflection, broader meaning, and personal choice.
4. Draft 1800-2200 Chinese characters with short mobile-friendly paragraphs and two to four useful subheadings.
5. Check every concrete claim against the parsed note or transcript.
6. Add three to five alternate titles and a 60-100 character cover summary.

## Writing Rules

- Write in first person with a quiet, reflective, restrained tone.
- Preserve real events and dialogue without inventing facts or intentions.
- Start with a concrete scene or conflict.
- Advance the central viewpoint by at least two layers.
- Use sensory detail only when supported by the source.
- Avoid medical advice, empty motivation, excessive rhetoric, and engagement bait.
- Minimize unnecessary medical, location, identity, and family details.

## Output

```text
# 主标题

> 文章摘要

正文与小标题

---

## 备选标题

## 封面摘要
```

Use `prompts/wechat-article-generator.md` as the full prompt and `workflows/wechat-article-generation-flow.md` as the execution checklist.
