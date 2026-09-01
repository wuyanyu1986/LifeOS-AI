# LifeOS AI

LifeOS AI 是一个面向个人成长、记忆沉淀和内容复用的 AI 系统。当前第一阶段聚焦“视频日记智能体”：用户通过口述、视频或转写文本记录日常经历，系统帮助完成理解、反思、记忆归档和内容生成。

## 项目目标

- 把零散的视频日记转化为可检索、可回顾、可行动的个人知识资产。
- 通过多 Agent 协作完成日记理解、认知挑战、个人记忆和内容生成。
- 与飞书知识库、日历、任务等工具连接，形成可持续的 LifeOS 工作流。
- 保留用户原始表达，同时沉淀结构化数据，方便长期复盘和产品化。

## 当前范围

第一版不追求完整 App，而是先完成可运行的产品骨架：

- 产品定义与 PRD
- 视频日记处理流程
- Agent 角色与 Prompt
- 飞书知识库结构
- 技术架构草案
- 版本路线图和关键决策记录

## 目录结构

```text
.
├── README.md
├── docs/
│   ├── 00-项目介绍.md
│   ├── 01-产品愿景与定位.md
│   ├── 02-PRD-V1.0.md
│   ├── 03-用户旅程与核心流程.md
│   ├── 04-Agent角色设计.md
│   ├── 05-飞书知识库架构设计.md
│   ├── 06-技术架构方案.md
│   └── 07-跨系统架构与审核同步方案.md
├── prompts/
│   ├── diary-analysis-agent.md
│   ├── cognition-challenge-agent.md
│   ├── memory-agent.md
│   └── content-generator-agent.md
├── skills/
│   └── viral-writer/
│       ├── SKILL.md
│       ├── style-constraints.md
│       └── agents/openai.yaml
├── workflows/
│   ├── multi-platform-content-production-flow.md
│   ├── content-revision-memory-loop.md
│   └── manual-video-diary-workflow.md
├── templates/
│   ├── source-notes-template.md
│   ├── daily-journal-template.md
│   └── memory-card-template.md
├── schemas/
│   └── diary-entry.schema.json
├── examples/
│   ├── sample-diary-entry.json
│   └── sample-final-journal.md
├── roadmap/
│   └── product-roadmap.md
└── decisions/
    └── architecture-decisions.md
```

## 核心工作流

```text
音频日记输入
  -> 本地语音转写
  -> 标准解析稿
  -> 飞书归档并提醒审核
  -> 标准解析稿审核通过
     -> Viral Writer 内容策略层
        -> 视频脚本 -> 独立提醒与审核
        -> 4-5分钟公众号文章 -> 独立提醒与审核
        -> 小红书笔记 -> 独立提醒与审核
        -> 抖音口播文案 -> 独立提醒与审核
     -> 封面视觉 brief -> 等待最终内容元数据 -> guizang-social-card-skill 生成社交卡片
        -> 小红书 3:4 轮播图
        -> 公众号 21:9 + 1:1 封面对
        -> 归档到公众号文章下的飞书子页面
  -> 所有选定分支审核完成且视觉资源归档完成
  -> 用户手工写入并发布
```

## 版本状态

当前处于 `v0.2` 手工工作流原型阶段。优先用真实或模拟的视频日记转写文本跑通一次完整闭环，再进入本地自动化开发。

## v0.2 本地使用方式

1. 阅读 `workflows/manual-video-diary-workflow.md`。
2. 为一条日记创建本地 `entries/YYYY-MM-DD-title/` 目录。
3. 复制 `templates/source-notes-template.md` 和 `templates/daily-journal-template.md`。
4. 粘贴视频或音频转写文本。
5. 标准解析稿审核通过后，运行 Viral Writer 内容策略，再按平台运行内容分支；各分支独立审核。
6. 生成 `final-journal.md`，必要时手动归档到飞书。

注意：`entries/` 默认不纳入仓库初始化，因为真实日记内容通常包含隐私。

更完整的多平台运行契约见 `workflows/multi-platform-content-production-flow.md`；Viral Writer 的项目内版本见 `skills/viral-writer/SKILL.md`。
