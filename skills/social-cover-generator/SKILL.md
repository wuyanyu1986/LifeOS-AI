---
name: social-cover-generator
description: "基于已审核标准解析稿和公众号文章，生成适配小红书与微信公众号的跨平台封面，并归档到公众号文章下的飞书子页面。"
---

# Social Cover Generator

## 触发条件

- `parsed_note.status=approved`
- 封面分支与视频脚本、公众号文章分支同时启动
- 最终图像生成必须等待公众号文章标题、观点和封面摘要就绪

## 必读

1. `workflows/social-cover-generation-flow.md`
2. `prompts/social-cover-generator.md`
3. 当前标准解析稿
4. 当前 revision 的公众号文章
5. 当前 `review-state.json`

## 输出

- `cover-master-1440.png`：1440×1440 母图
- `cover-xiaohongshu.png`：1080×1440，3:4
- `cover-wechat-wide.png`：900×383
- `cover-wechat-square.png`：900×900
- 飞书子页面：`YYYY-MM-DD 公众号与小红书封面`

## 执行规则

1. 只使用标准解析稿支持的事实、场景和情绪。
2. 使用文章标题、中心观点和封面摘要确定最终视觉方向。
3. 生成一张中心安全的无文字正方形母图，再导出三种平台成品。
4. 检查所有裁剪后的主体完整性，不允许拉伸变形。
5. 使用文章的 `wiki_node_token` 作为父节点创建飞书子页面。
6. 使用创建结果的 `doc_id` 插入三张图片。
7. 成功后记录 `source_article_revision` 并设置 `cover_assets.status=archived`。

## 安全与边界

- 不打开或操作小红书、微信公众号后台。
- 不发布、上传到内容平台或调用平台 API。
- 不生成可识别车牌、地址、病历、聊天记录、账号或二维码。
- 不重复创建同一文章 revision 的封面子页面。
