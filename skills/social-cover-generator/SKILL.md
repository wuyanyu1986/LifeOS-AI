---
name: social-cover-generator
description: "通过 op7418/guizang-social-card-skill 基于已审核内容生成小红书图文及微信公众号封面对，并归档到公众号文章下的飞书子页面。"
---

# Social Cover Generator Adapter

本项目的图片生成实现统一改用外部 Skill：
`op7418/guizang-social-card-skill`。

上游 Skill：<https://github.com/op7418/guizang-social-card-skill>

它负责 HTML/CSS 卡片设计、浏览器渲染、平台尺寸导出和可选 QA；本文件只负责
LifeOS 的输入契约、审核状态、版本幂等和飞书归档，不再定义独立的 PIL 图片生成方案。

## 触发条件

- `parsed_note.status=approved`
- 封面分支与视频脚本、公众号文章分支同时启动
- 最终图像生成必须等待公众号文章标题、观点和封面摘要就绪

## 必读

1. `workflows/social-cover-generation-flow.md`
2. `prompts/social-cover-generator.md`
3. 外部 `guizang-social-card-skill/SKILL.md`
4. 外部 Skill 所需的相关 references：平台规格、布局配方、样式系统、内容规划和 QA 清单
5. `style-constraints.md`
6. 当前标准解析稿
7. 当前 revision 的公众号文章
8. 当前 `review-state.json`

## 输出

- 小红书：封面及内容轮播图，默认 3:4，具体尺寸以外部 Skill 的 platform specs 为准
- 公众号：21:9 主封面 + 1:1 方形分享图
- 外部 Skill 任务目录中的 `index.html`、`output/` 和验证结果
- 飞书子页面：`YYYY-MM-DD 公众号与小红书封面`

## 执行规则

1. 只使用标准解析稿支持的事实、场景和情绪。
2. 使用文章标题、中心观点和封面摘要确定最终视觉方向。
3. 由外部 Skill 先做页面规划，再选择 Editorial 或 Swiss 视觉系统和对应主题。
4. 使用外部 Skill 的种子 HTML 模板，不从空白 HTML 开始；通过浏览器截图导出图片。
5. 公众号必须在同一 HTML 中同时生成 21:9 和 1:1 封面对，便于检查视觉一致性。
6. 小红书按内容拆成封面 + 观点页，通常 5–9 页；不要把文章全文塞进图片。
7. 检查溢出、字体可读性、裁剪、主体安全区、隐私和事实一致性。
8. 使用文章的 `wiki_node_token` 作为父节点创建飞书子页面，并归档所有最终图片。
9. 成功后记录 `source_article_revision` 并设置 `cover_assets.status=archived`。
10. 有已确认的视觉风格记忆时，必须将其作为生成和版式的优先约束；只有用户明确提出时才偏离。

## 安全与边界

- 不打开或操作小红书、微信公众号后台。
- 不发布、上传到内容平台或调用平台 API。
- 不生成可识别车牌、地址、病历、聊天记录、账号或二维码。
- 不重复创建同一文章 revision 的封面子页面。
- 不在本项目中调用 `scripts/render_social_covers.py` 作为新任务的生成器；该脚本仅保留作历史兼容。
