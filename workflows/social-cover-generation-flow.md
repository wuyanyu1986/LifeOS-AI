# 公众号与小红书社交卡片生成流程

**Version**: 0.1  
**Status**: Review  
**Trigger**: `parsed_note.status=approved`

## 目标

在视频脚本和公众号文章之外启动第三个并行分支，使用
`op7418/guizang-social-card-skill` 生成小红书轮播图和公众号封面对，并在公众号文章知识库节点下创建子页面归档图片。

该分支使用 `skills/viral-writer/SKILL.md` 产出的标题、核心观点和视觉 brief；最终渲染仍然等待最终文章元数据，不把草稿标题当作最终版本。

本流程不打开或操作任何内容平台后台，也不发布内容。

## 并行与依赖

```text
parsed note approved
  -> video branch
  -> article branch
  -> cover branch: create visual brief
       -> wait for article title, viewpoint and cover summary
       -> guizang-social-card-skill 页面规划与 HTML/CSS 渲染
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
task-folder/index.html      # 外部 Skill 生成的单文件 HTML
task-folder/output/*.png    # 小红书轮播图及公众号 21:9 / 1:1 封面对
task-folder/qa/*             # 可选验证结果和检查记录
```

公众号 21:9 与 1:1 封面对必须在同一个 HTML 中生成并预览，避免视觉主题漂移。小红书图片按页面规划生成，不强制从一张母图裁剪。

## 执行步骤

1. 标准解析稿审核通过时设置 `cover_assets.status=briefing`。
2. 从解析稿提取一个真实核心场景、情绪转折、关键物件和隐私限制。
3. 若公众号文章尚未生成，设置 `cover_assets.status=waiting_for_article`，不生成最终图片。
4. 文章生成后读取主标题、中心观点和封面摘要，并记录 `source_article_revision`。
5. 读取 `op7418/guizang-social-card-skill` 的 `SKILL.md` 及所需 references。
6. 生成页面规划，选择 Editorial 或 Swiss 模式，并复制对应种子模板到任务目录。
7. 用标准解析稿支持的事实和文章元数据填充 HTML，使用浏览器截图导出图片。
8. 检查尺寸、溢出、字号、裁剪、隐私和事实一致性；如用户要求再执行自动验证脚本。
9. 在公众号文章节点下创建 `YYYY-MM-DD 公众号与小红书封面` 子页面。
10. 将成品图片插入子页面并写明用途。
11. 设置 `cover_assets.status=archived`，记录节点、文档 token、任务目录和本地路径，发送一次“社交卡片已生成”提醒。

## 飞书归档

创建子页面：

```bash
lark-cli docs +create \
  --profile siyangyuan-tiantu \
  --as user \
  --title "YYYY-MM-DD 公众号与小红书封面" \
  --wiki-node "ARTICLE_WIKI_NODE_TOKEN" \
  --markdown "## 使用说明\n\n- 小红书：3:4 轮播图\n- 公众号主封面：21:9\n- 公众号方形分享图：1:1\n- 生成 Skill：op7418/guizang-social-card-skill"
```

使用创建结果中的 `doc_id` 插入图片：

```bash
lark-cli docs +media-insert --profile siyangyuan-tiantu --as user \
  --doc "COVER_DOC_ID" --file "task-folder/output/xhs-01.png" \
  --align center --caption "小红书图文｜3:4"

lark-cli docs +media-insert --profile siyangyuan-tiantu --as user \
  --doc "COVER_DOC_ID" --file "task-folder/output/wechat-wide.png" \
  --align center --caption "公众号主封面｜21:9"

lark-cli docs +media-insert --profile siyangyuan-tiantu --as user \
  --doc "COVER_DOC_ID" --file "task-folder/output/wechat-square.png" \
  --align center --caption "公众号方形分享图｜1:1"
```

所有飞书读写必须使用 `--profile siyangyuan-tiantu --as user`。

## 版本与幂等

- `source_article_revision` 必须等于当前文章 revision，才视为当前封面。
- 同一文章 revision 已存在 `archived` 封面时不得重复创建子页面或插图。
- 文章需要修改时将当前封面设为 `superseded`；新文章 revision 完成后只重跑封面分支。
- 社交卡片渲染或上传失败时保留文章和视频分支，只重试封面分支。

## 完成条件

条目进入 `ready_for_manual_publish` 前必须同时满足：

```text
video_script.status = approved
wechat_article.status = approved
cover_assets.status = archived
cover_assets.source_article_revision = wechat_article.revision
```

旧条目没有 `cover_assets` 字段时按历史流程处理，不自动补生成。
