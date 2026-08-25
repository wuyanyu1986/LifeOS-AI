# 公众号与小红书封面生成流程

**Version**: 0.1  
**Status**: Review  
**Trigger**: `parsed_note.status=approved`

## 目标

在视频脚本和公众号文章之外启动第三个并行分支，生成可同时用于小红书与微信公众号的封面图片，并在公众号文章知识库节点下创建子页面归档图片。

本流程不打开或操作任何内容平台后台，也不发布内容。

## 并行与依赖

```text
parsed note approved
  -> video branch
  -> article branch
  -> cover branch: create visual brief
       -> wait for article title, viewpoint and cover summary
       -> generate and crop cover assets
       -> archive under the article node
```

封面分支与另外两项同时启动，但图像定稿必须等待公众号文章产出。这样既保留并行执行，又避免封面观点与最终文章不一致。

## 输入

- 已审核标准解析稿：事实、真实场景、情绪与隐私边界
- 公众号文章：主标题、中心观点、封面摘要
- `wechat_article.wiki_node_token`：封面子页面的父节点

## 输出文件

保存到对应本地条目目录：

```text
cover-master-1440.png       # 1440×1440 母图
cover-xiaohongshu.png       # 1080×1440，3:4
cover-wechat-wide.png       # 900×383，约 2.35:1
cover-wechat-square.png     # 900×900，1:1
```

母图必须为中心安全构图。小红书、公众号横版和公众号方形图均由同一母图导出，避免视觉主题漂移。

## 执行步骤

1. 标准解析稿审核通过时设置 `cover_assets.status=briefing`。
2. 从解析稿提取一个真实核心场景、情绪转折、关键物件和隐私限制。
3. 若公众号文章尚未生成，设置 `cover_assets.status=waiting_for_article`，不生成最终图片。
4. 文章生成后读取主标题、中心观点和封面摘要，并记录 `source_article_revision`。
5. 使用 `prompts/social-cover-generator.md` 生成至少 1440×1440 的正方形母图。
6. 从中央安全区域导出 3:4、约 2.35:1 和 1:1 三种成品。
7. 检查尺寸、裁剪、隐私、事实一致性和无文字要求。
8. 在公众号文章节点下创建 `YYYY-MM-DD 公众号与小红书封面` 子页面。
9. 将三张成品图片依次插入子页面并写明用途。
10. 设置 `cover_assets.status=archived`，记录节点、文档 token 和本地路径，发送一次“封面图片已生成”提醒。

## 飞书归档

创建子页面：

```bash
lark-cli docs +create \
  --profile siyangyuan-tiantu \
  --as user \
  --title "YYYY-MM-DD 公众号与小红书封面" \
  --wiki-node "ARTICLE_WIKI_NODE_TOKEN" \
  --markdown "## 使用说明\n\n- 小红书：3:4\n- 公众号主封面：约 2.35:1\n- 公众号方形分享图：1:1"
```

使用创建结果中的 `doc_id` 插入图片：

```bash
lark-cli docs +media-insert --profile siyangyuan-tiantu --as user \
  --doc "COVER_DOC_ID" --file "cover-xiaohongshu.png" \
  --align center --caption "小红书封面｜1080×1440｜3:4"

lark-cli docs +media-insert --profile siyangyuan-tiantu --as user \
  --doc "COVER_DOC_ID" --file "cover-wechat-wide.png" \
  --align center --caption "公众号主封面｜900×383"

lark-cli docs +media-insert --profile siyangyuan-tiantu --as user \
  --doc "COVER_DOC_ID" --file "cover-wechat-square.png" \
  --align center --caption "公众号方形图｜900×900"
```

所有飞书读写必须使用 `--profile siyangyuan-tiantu --as user`。

## 版本与幂等

- `source_article_revision` 必须等于当前文章 revision，才视为当前封面。
- 同一文章 revision 已存在 `archived` 封面时不得重复创建子页面或插图。
- 文章需要修改时将当前封面设为 `superseded`；新文章 revision 完成后只重跑封面分支。
- 图片生成或上传失败时保留文章和视频分支，只重试封面分支。

## 完成条件

条目进入 `ready_for_manual_publish` 前必须同时满足：

```text
video_script.status = approved
wechat_article.status = approved
cover_assets.status = archived
cover_assets.source_article_revision = wechat_article.revision
```

旧条目没有 `cover_assets` 字段时按历史流程处理，不自动补生成。
