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
│   └── 06-技术架构方案.md
├── prompts/
│   ├── diary-analysis-agent.md
│   ├── cognition-challenge-agent.md
│   ├── memory-agent.md
│   └── content-generator-agent.md
├── roadmap/
│   └── product-roadmap.md
└── decisions/
    └── architecture-decisions.md
```

## 核心工作流

```text
视频日记输入
  -> 语音转写
  -> 日记理解 Agent
  -> 认知挑战 Agent
  -> 个人记忆 Agent
  -> 内容生成 Agent
  -> 飞书知识库归档
```

## 版本状态

当前处于 `v0.1` 产品定义阶段。优先把问题定义、信息架构和 Agent 协作方式写清楚，再进入最小可运行原型开发。

