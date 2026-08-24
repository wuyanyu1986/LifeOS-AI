# Agent 角色设计

LifeOS AI V1.0 使用多 Agent 协作，而不是让一个通用 Agent 处理所有任务。这样可以让每个角色目标更清晰，输出更稳定。

## 1. Diary Analysis Agent

职责：

- 理解日记文本。
- 提取事实、情绪、人物、地点、主题和行动。
- 生成结构化摘要。

输入：

- 转写文本
- 日期
- 用户补充标签

输出：

- 今日摘要
- 关键事件
- 情绪轨迹
- 洞察与行动项

## 2. Cognitive Challenge Agent

职责：

- 识别叙述中的认知模式。
- 提出帮助用户反思的问题。
- 将模糊感受转化为可验证假设。

边界：

- 不做心理诊断。
- 不用攻击性语言。
- 不替用户做重大人生决定。

## 3. Memory Agent

职责：

- 判断哪些信息值得长期保存。
- 生成记忆卡片。
- 管理人物、项目、目标、偏好和经验。

记忆类型：

- `person`
- `project`
- `goal`
- `preference`
- `lesson`
- `decision`
- `risk`

## 4. Content Generator Agent

职责：

- 从私密日记中提取可公开素材。
- 生成不同格式的内容草稿。
- 保持用户原本的观点和语气。

输出类型：

- 文章提纲
- 短视频脚本
- 播客提纲
- 社交媒体草稿
- 复盘卡片

## 5. Orchestrator

职责：

- 管理 Agent 执行顺序。
- 传递上下文。
- 合并输出结果。
- 处理失败重试和人工确认。

推荐顺序：

```text
Diary Analysis Agent
  -> Cognitive Challenge Agent
  -> Memory Agent
  -> Content Generator Agent
```

