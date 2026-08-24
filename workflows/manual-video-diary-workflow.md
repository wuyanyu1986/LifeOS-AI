# Manual Video Diary Workflow

This workflow describes the v0.2 manual prototype for turning a video diary into a structured LifeOS AI entry.

## Goal

Process one video, audio, or transcript into:

- A structured daily journal entry
- Cognitive challenge questions
- Memory card candidates
- Content draft candidates
- Feishu-ready Markdown

## Inputs

Required:

- Recording date
- Video, audio, or transcript
- User language

Optional:

- Title
- Tags
- Related project
- People mentioned
- Content goal

## Folder Convention

For local work, use this structure:

```text
entries/
└── YYYY-MM-DD-title/
    ├── source-notes.md
    ├── transcript.md
    ├── diary-analysis.md
    ├── cognitive-challenge.md
    ├── memory-candidates.json
    ├── content-draft.md
    └── final-journal.md
```

The `entries/` folder is intentionally not created by default because diary content may be private. Create it locally when you are ready to process real data.

## Step 1: Prepare Source Notes

Create `source-notes.md` from `templates/source-notes-template.md`.

Fill in:

- Date
- Title
- Source type
- File reference
- Privacy level
- Tags
- Short context

## Step 2: Transcribe

Create `transcript.md`.

If you already have transcript text, paste it directly. If not, use any speech-to-text tool and keep the raw transcript before cleanup.

Keep these sections:

```markdown
# Transcript

## Raw Transcript

## Cleaned Transcript

## Unclear Segments
```

## Step 3: Run Diary Analysis Agent

Use `prompts/diary-analysis-agent.md`.

Input:

- `source-notes.md`
- `transcript.md`

Save output as:

```text
diary-analysis.md
```

Review for:

- Invented facts
- Missing people or projects
- Incorrect event order
- Overly generic summary

## Step 4: Run Cognitive Challenge Agent

Use `prompts/cognition-challenge-agent.md`.

Input:

- `diary-analysis.md`
- `transcript.md`
- Any known user context that is safe to include

Save output as:

```text
cognitive-challenge.md
```

Review for:

- Whether questions are actually useful
- Whether the tone is respectful
- Whether suggested actions are small enough

## Step 5: Run Memory Agent

Use `prompts/memory-agent.md`.

Input:

- `diary-analysis.md`
- `cognitive-challenge.md`
- Existing memory notes, if available

Save output as:

```text
memory-candidates.json
```

Validate each candidate against:

- Is it stable enough to remember?
- Does it have a source date?
- Does it need user review?
- Is it too sensitive to store?

## Step 6: Run Content Generator Agent

Use `prompts/content-generator-agent.md`.

Input:

- `diary-analysis.md`
- `cognitive-challenge.md`
- `memory-candidates.json`
- Desired content format
- Privacy preference

Save output as:

```text
content-draft.md
```

## Step 7: Assemble Final Journal

Create `final-journal.md` from `templates/daily-journal-template.md`.

Copy reviewed sections from the previous outputs into the final template.

The final journal should be suitable for Feishu copy-paste without exposing raw private content by default.

## Step 8: Manual Feishu Archive

Create or update a Feishu document under:

```text
LifeOS AI / 01 Daily Journal / YYYY-MM-DD - Title
```

If memory candidates are confirmed, add them under:

```text
LifeOS AI / 02 Memory Cards
```

If a content draft is worth keeping, add it under:

```text
LifeOS AI / 06 Content Studio
```

## Completion Checklist

- [ ] Source notes completed
- [ ] Transcript saved
- [ ] Diary analysis reviewed
- [ ] Cognitive challenge reviewed
- [ ] Memory candidates reviewed
- [ ] Content draft reviewed
- [ ] Final journal assembled
- [ ] Feishu document created or updated
- [ ] Sensitive details removed from public content

