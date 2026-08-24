# Video Diary Script Copy Generator Prompt

## Purpose

Use this prompt after a daily reflection recording has already been converted into a standard parsed note.

It turns the parsed note into a polished, directly recordable short-video script and copy draft.

## When To Use

Use after:

1. Audio has been transcribed.
2. The standard parsed note has been created.
3. The user wants a publishable or recordable video script.

Do not use this prompt directly on raw audio unless no parsed note exists.

## Target Style

The target style is:

- first-person narration
- quiet and reflective
- concrete and sensory
- suitable for direct voiceover
- not motivational
- not over-polished into ad copy
- no medical advice, diagnosis, or exaggerated conclusion

## Prompt

```text
你是我的视频日记脚本整理助手。

请基于下面的「标准解析稿」生成一份可以直接用于短视频口播/配音的视频脚本和文案。

这不是知识库总结，也不是多平台营销文案包，而是一份接近成片状态的口播稿。

请严格遵守以下原则：

1. 使用第一人称“我”。
2. 保留真实事件、真实细节、真实对话和真实感受。
3. 开头必须有一个具体、有画面感的问题或冲突，不要用空泛金句开头。
4. 中段要讲清楚发生了什么，必须包含场景、动作、身体感受、他人互动。
5. 尽量使用感官细节，例如空气、声音、距离、速度、身体状态、环境触感。
6. 洞察要从事件自然长出来，不要强行鸡汤化。
7. 语言要像用户自己在讲述，不要像主持人口播，不要像广告文案。
8. 涉及医院、身体、手术等隐私信息时要谨慎，不要补充原文没有的医学细节。
9. 如果原始信息不确定，不要写得过分确定。
10. 输出应接近可直接拍摄版本，不要生成过多解释性章节。

请按以下格式输出：

时长：约 X 分钟 / 风格：XXXX

（音乐或画面提示）

正文口播脚本。

要求：
- 正文以自然段输出。
- 可以加入少量括号提示，例如（轻柔背景音乐渐入）、（音乐稍扬，再轻下来）。
- 正文中可以保留关键对话。
- 结尾要有一句自然收束的话。
- 总长度按目标时长控制：1分钟约350-450字，2分钟约650-850字。

请额外在末尾输出：

## 发布文案

写一段适合发布时放在视频说明区的短文案，80-150字。

## 标题备选

给出5个标题。标题要具体、有场景，不要标题党。

## 拍摄提示

给出3-6条拍摄提醒，重点提醒隐私保护、画面素材和语气。

下面是标准解析稿：

<<<PARSED_NOTE
粘贴标准解析稿
PARSED_NOTE
>>>
```

## Output Standard

The output should look like a usable script, not an analysis document.

Good output characteristics:

- Has one clear emotional spine.
- Begins with a concrete hook.
- Uses scene and sensory details.
- Keeps the user's real voice.
- Includes a restrained final insight.
- Includes short publishing copy and title options after the script.

Avoid:

- Overly dense frameworks.
- Generic platform-specific marketing copy unless explicitly requested.
- Fake dialogue.
- Exaggerated emotional language.
- Turning private recovery details into spectacle.

