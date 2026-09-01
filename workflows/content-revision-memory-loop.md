# 内容修订记忆与风格反向学习流程

**Version**: 0.1  
**Status**: Draft  
**Trigger**: 用户修订并保存任一平台内容

## 目标

把用户对生成稿的修改分成两类：只影响本篇内容的局部修订，以及可以复用于未来创作的稳定风格偏好。只有经过确认的稳定偏好才能写入 Viral Writer 的风格约束。

## 流程

```text
生成稿保存
  -> 保存 original 文件
  -> 用户修订
  -> 保存 revised 文件
  -> 对比差异
  -> 提取风格约束候选
  -> 用户确认候选
      -> 写入 style-constraints.md
      -> 写入 preference memory card
      -> 下次生成自动读取
      -> 当前内容不自动重写
```

## 记忆分层

### 局部修订

只写入当前条目的修订记录，例如删掉一个段落、替换一个标题、调整一个事实。它影响当前 revision，不改变 Skill。

### 风格约束候选

从多次或明确表达的修订中提取可泛化规则，例如“减少抽象金句”“开头先写场景”“不要使用夸张词”。候选记录在 `content-feedback.schema.json` 中，状态为 `candidate`。

### 已确认风格记忆

用户确认后才将规则追加到 `skills/viral-writer/style-constraints.md`，并在 `templates/memory-card-template.md` 对应的记忆卡中记录为 `preference`。每条规则必须保留来源修订、适用平台、确认日期和状态。

## 反向写入规则

- 不根据一次普通改字自动改变 Skill。
- 用户明确说“以后都这样”“我的风格是……”时，可将该条作为高置信候选，但仍保留确认记录。
- 只把风格、结构、措辞偏好写入约束；事实、人物、单次选题不写入全局 Skill。
- 新约束与旧约束冲突时，不覆盖旧记录，新增记录并将旧记录标为 `retired`。
- 约束写入后只影响下一次生成，不回溯改写历史内容。

## 最小输出

```text
feedback.json
content-revision-memory.md
```

其中 `feedback.json` 机器读取，`content-revision-memory.md` 供用户审阅；所有原稿、修订稿和差异文件保存在本地隐私目录，不发送到公开平台。
