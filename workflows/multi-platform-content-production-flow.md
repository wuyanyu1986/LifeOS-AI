# 多平台内容生产流程

**Version**: 0.1  
**Status**: Draft  
**Trigger**: `parsed_note.status=approved`

## 目标

把一份已审核的标准解析稿，经过一次统一的内容策略分析后，生成适配微信公众号、小红书、抖音的独立内容分支，并让每个分支独立审核、独立修订。

## 总体流程

```text
音频/视频
  -> 转写
  -> 标准解析稿
  -> 标准解析稿人工审核
      -> 内容策略层（Viral Writer，11 维洞见）
          -> 微信公众号文章 ──-> 独立审核
          -> 小红书笔记   ──-> 独立审核
          -> 抖音口播文案 ──-> 独立审核
          -> 视觉 brief
                -> 等待最终标题/核心观点
                -> 生成封面与正文配图指导
                -> 独立审核/归档
  -> 所有选定分支通过
  -> ready_for_manual_publish
  -> 用户手工发布
```

## 阶段与职责

### 1. 源稿阶段

转写和标准解析负责事实、情绪、事件和隐私边界；它们不负责平台文案。标准解析稿未通过审核，内容生产不得启动。

### 2. 策略阶段

Viral Writer 读取标准解析稿，形成内部策略对象：核心观点、副观点、说服策略、情绪曲线、语言参数和互动设计。策略对象只服务于本次内容生成，并记录源稿 revision。

### 3. 平台分支阶段

公众号、小红书、抖音分别读取标准解析稿和策略对象。不得把一个平台的成稿作为另一个平台的事实来源；如需复用，只能复用经过源稿校验的事实和核心观点。

默认生成全部三个分支；用户指定平台时只生成指定分支。每个分支都记录 `content_revision`，并发送自己的待审核提醒。

### 4. 视觉阶段

视觉 brief 可与平台文案并行准备，但最终封面必须等待选定平台的最终标题和核心观点。公众号与小红书封面沿用 `workflows/social-cover-generation-flow.md` 的母图与归档规则；抖音补充 9:16 分镜/画面建议时，不自动生成视频。

### 5. 发布阶段

系统只推进到 `ready_for_manual_publish`。不自动写入公众号、小红书或抖音后台，不代替用户发布。

## 状态模型

```text
parsed_pending_review
  -> parsed_approved
  -> content_strategy_ready
  -> content_branches_generating
  -> content_pending_review
  -> content_ready
  -> ready_for_manual_publish
```

分支状态独立：`pending_generation`、`pending_review`、`approved`、`changes_requested`、`failed`、`superseded`。

## 修订与幂等

- 源稿 revision 变化：重新生成受影响的全部内容分支。
- 单个平台请求修改：只重跑该平台；其他分支保持原 revision。
- 同一 `platform + source_revision + content_revision` 不重复创建文档或提醒。
- 视觉资源必须记录 `source_article_revision` 或对应平台 revision；旧资源标记为 `superseded`。
- 失败只重试失败分支，保留已成功的兄弟分支。

## 完成条件

只有当用户选定的内容分支全部 `approved`，并且对应视觉资源已归档（若该分支需要视觉资源）时，条目才可进入 `ready_for_manual_publish`。

## 质量检查

- [ ] 源稿审核已通过且 revision 可追溯
- [ ] 只有一个核心观点，且由源稿支持
- [ ] 平台字数、节奏、标题和互动方式符合平台规范
- [ ] 无编造事实、对话、数据、意图或未经授权的隐私
- [ ] 每个平台有 5 个标题并标注策略
- [ ] 视觉 prompt 描述具体画面、风格、色调和构图
- [ ] 各平台审核提醒和修订均可幂等重放
