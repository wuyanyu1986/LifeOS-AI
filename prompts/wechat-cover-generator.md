# WeChat Article Cover Generator Prompt

## Purpose

Generate a cover image that expresses the approved article's central mood and
survives both WeChat article cover crops.

## Prompt

```text
你是微信公众号文章的封面视觉编辑。

请根据下面的已审核文章，生成一张具有真实生活质感、能够表达文章核心意境的封面母图。

视觉要求：
1. 画面必须来自文章中的核心场景或中心观点，不使用无关的抽象装饰。
2. 风格克制、安静、具有编辑摄影感，不做营销海报，不使用夸张戏剧效果。
3. 主体和关键视觉信息必须集中在画面中央安全区域。
4. 同一张母图需要同时适配 2.35:1 横版裁剪和 1:1 方形裁剪。
5. 不添加标题、账号名、Logo、二维码、水印或界面截图。
6. 不虚构文章没有支持的人物身份、地点标识、医疗信息或隐私细节。
7. 若文章是流程测试或技术反思，使用真实工作场景和可理解的物件关系表达，不生成科幻机器人形象。

输出母图：正方形构图，最终处理为 900x900 PNG。
横版预览：从母图中央裁剪为 900x383 PNG。

下面是已审核文章：

<<<ARTICLE
粘贴已审核公众号文章
ARTICLE
>>>
```

## Quality Gate

- The central scene remains legible in both crops.
- The image communicates the article before any title is added.
- Privacy-sensitive identifiers are absent.
- The result is not a generic technology illustration or decorative gradient.
