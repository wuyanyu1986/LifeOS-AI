# LifeOS AI for WorkBuddy

这是从 LifeOS AI 原型整理出的 WorkBuddy 可导入 Skill 包。

## 导入

在 WorkBuddy 的“技能”中选择“上传技能”，上传本目录或打包后的目录。WorkBuddy 支持导入本地技能包，导入后可在对话中启用；建议先用脱敏样本试跑，并只启用本任务需要的工具权限。

## 运行前选择

- 输入音视频：启用语音转写能力；
- 生成封面：启用图片生成能力；
- HTML/CSS 排版：启用浏览器或图片渲染能力；
- 飞书归档：启用飞书/知识库连接器；
- 飞书提醒：启用消息连接器。

未启用的能力会降级为本地 Markdown、JSON、提示词和视觉 brief 输出。

## 配置

将 `config.example.json` 复制为当前工作区的 `lifeos.config.json`，再按需修改本地目录、飞书连接器、知识库根节点、默认平台和自动同步开关。不要在配置文件中保存 Token、Cookie、密码或 API Key；这些信息应在 WorkBuddy 的连接器或模型设置中配置。

默认配置只写入 WorkBuddy 当前工作区，不同步飞书、不发送审核提醒。需要同步时，将 `feishu.enabled` 设为 `true`，并在 WorkBuddy 中启用与 `feishu.connector` 同名的飞书连接器。

## 定时自动化

定时触发不在 Skill 包内实现，需要在 WorkBuddy 的“自动化”页面创建任务。建议创建以下 4 个可独立启停的任务：

1. **新日记扫描**：每 30—60 分钟扫描 `storage.source_dir`，发现新材料后创建解析任务。
2. **审核状态检查**：每天 1—4 次汇总待审核条目，必要时发送提醒。
3. **审核后内容生成**：每 30—60 分钟处理 `parsed_note.status=approved` 的条目。
4. **已批准内容同步**：每小时或每天同步已批准且未同步的内容，默认关闭。

创建自动化时选择：本 Skill、当前工作区、对应任务 Prompt 和所需连接器。WorkBuddy 的自动化任务会保存工作区、提示词、技能、模型和调度规则，并在设定时间触发 Agent。citehttps://www.workbuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Automation-Guide

原项目的 `config/com.lifeos.review-listener.plist`、`scripts/review_message_listener.py` 和 60 秒 Wiki 扫描逻辑不直接迁移；它们由 WorkBuddy 自动化节点和连接器替代。

## 迁移说明

该 Skill 不依赖 `lark-cli`、固定本地路径、后台监听器或 `op7418/guizang-social-card-skill`。原仓库中的 `docs/`、`prompts/`、`workflows/`、`schemas/` 和脚本仍作为开发参考保留；WorkBuddy 运行规则以 `SKILL.md` 为准。
