# WeChat Article Generation Flow

This workflow turns a standard daily reflection note into a viewpoint-led WeChat Official Account article.

## Position In The Full Pipeline

```text
audio recording
  -> transcription
  -> standard parsed note
     -> video script and copy
     -> WeChat article
     -> social cover visual brief
```

The article, video script, and social-cover brief are parallel outputs. Generate
each directly from the standard parsed note so that one derivative does not
distort the other. The cover branch waits for the article metadata before final
image generation.

Hard prerequisite:

```text
parsed_note.status = approved
```

If the parsed note is pending review or has changes requested, stop without generating an article.

## Required Input

- Standard parsed note
- Recording date
- Privacy constraints
- Target reading time, default 4-5 minutes

Optional:

- User-edited video script as a voice reference only
- Preferred article angle
- Publishing account style

## Step 1: Separate Facts From Interpretation

Extract verified events, original dialogue, supported sensory details, emotional turns, candidate insights, and privacy risks.

Do not treat generated sensory language from a video script as fact unless the parsed note or transcript supports it.

## Step 2: Select One Central Viewpoint

Write the viewpoint in one sentence before drafting. It must be supported by the event, broader than a diary summary, and restrained enough to remain credible.

## Step 3: Build The Argument

Use this progression:

1. Concrete scene and tension
2. Event development
3. Human interaction or emotional turn
4. First layer of realization
5. Broader interpretation
6. Personal choice or changed understanding

## Step 4: Draft For Mobile Reading

- Target 1800-2200 Chinese characters for the article body.
- Keep paragraphs short.
- Use two to four meaningful subheadings.
- Avoid list-heavy writing unless the subject requires it.
- Do not repeat one sentence merely to increase length.

## Step 5: Run A Source-Fidelity Check

Check every concrete claim against the parsed note or transcript. Remove or soften unsupported medical detail, invented dialogue, inferred intentions presented as fact, exaggerated sensory details, and unnecessary identifying information.

## Step 6: Add Publishing Metadata

Add three to five alternate titles, a one-sentence `核心观点`, and a 60-100
character cover summary. Do not add engagement bait unless explicitly requested.

## Feishu Creation

Create the article as a sibling of the video script under the daily parsed note:

```bash
lark-cli docs +create \
  --profile siyangyuan-tiantu \
  --as user \
  --title "YYYY-MM-DD 公众号文章" \
  --wiki-node "DAILY_NOTE_WIKI_NODE_TOKEN" \
  --markdown @entries/YYYY-MM-DD-daily-reflection/wechat-article.md
```

## Review Notification

After the document is created or revised:

1. Set `wechat_article.status=pending_review`.
2. Send a dedicated `公众号文章待审核` Feishu message with the document link and revision.
3. Do not treat video approval as article approval.
4. On a change request, update only the article and send a new reminder.

Use `workflows/wechat-article-review.md` for the review contract.

## Quality Checklist

- [ ] The body is approximately 1800-2200 Chinese characters.
- [ ] The article has one clear central viewpoint.
- [ ] The opening starts from a concrete scene.
- [ ] Every factual detail is supported by the source.
- [ ] The viewpoint advances beyond the event summary.
- [ ] The tone remains first-person and restrained.
- [ ] Privacy-sensitive details are minimized.
- [ ] Alternate titles and cover summary are included.
- [ ] One machine-readable `核心观点` is included for the cover branch.
- [ ] Article review reminder sent exactly once per revision.
- [ ] Article approval recorded independently.
