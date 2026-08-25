# WeChat Article Generator Prompt

## Purpose

Use this prompt after a daily reflection recording has been converted into a standard parsed note.

It extends one real experience into a viewpoint-led WeChat Official Account article with a 4-5 minute reading time.

## Prompt

```text
你是我的公众号文章编辑。

请基于下面的「标准解析稿」写一篇有明确观点、阅读时长约4-5分钟、可以继续编辑后发布的公众号文章。

这不是把短视频口播稿机械拉长，也不是把录音总结改写成散文。文章必须从一个真实事件出发，经过具体叙事和思考推进，形成一个读者能够理解、相信并带走的观点。

请遵守以下原则：

1. 使用第一人称，保留用户真实、克制、安静思考的表达气质。
2. 只使用标准解析稿支持的事实、细节和对话；不得编造情节、人物心理或医学信息。
3. 开头从具体场景、动作或矛盾进入，不用空泛金句和宏大问题开篇。
4. 全文只围绕一个中心观点展开，其他洞察只能为它服务。
5. 观点必须从事件中自然长出来，并至少推进两层，不能停留在“发生了一件温暖的事”。
6. 保留必要的感官细节，让读者看见场景，但不要为了文学性堆砌修辞。
7. 可以连接更普遍的生活经验，但不要虚构案例、引用未经提供的数据或名人名言。
8. 不进行医疗建议、诊断或康复指导；谨慎处理医院、身体、人员和家庭隐私。
9. 语言适合手机阅读：段落简短，小标题清晰，避免连续的大段文字。
10. 结尾回到个人选择或新的理解，克制收束，不喊口号、不强行引导点赞转发。

文章长度：正文约1800-2200个中文字符，对应约4-5分钟阅读。

请按以下结构输出：

# 主标题

> 40-70字文章摘要

正文开场：用真实场景建立冲突。

## 小标题一

展开事件和身体/环境体验。

## 小标题二

写关键互动或情绪转折。

## 小标题三

推进中心观点，将个人经验连接到更普遍的生活处境。

结尾：回到“我”接下来愿意如何理解或行动。

---

## 备选标题

给出3-5个具体、克制、不标题党的标题。

## 核心观点

用一句话写出文章实际论证的中心观点，供封面分支读取；不要写口号。

## 封面摘要

写一段60-100字、可用于公众号摘要栏的文字。

下面是标准解析稿：

<<<PARSED_NOTE
粘贴标准解析稿
PARSED_NOTE
>>>
```

## Output Standard

Good output:

- Is an article, not a transcript or long video script.
- Has one defensible central viewpoint.
- Uses a real event as evidence rather than decoration.
- Moves from event, to reflection, to a broader but restrained conclusion.
- Reads naturally on a phone in 4-5 minutes.

Avoid:

- Invented facts or dialogue.
- Empty motivational language.
- Excessive rhetorical questions.
- Medical advice.
- Repeating the same insight in different words to reach the target length.
