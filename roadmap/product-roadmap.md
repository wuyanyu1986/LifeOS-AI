# Product Roadmap

## v0.1 Product Definition

Status: Done

- Initialize repository and documentation.
- Define product vision, PRD, user journey, Agent roles, Feishu knowledge structure, and architecture.
- Establish prompt files and decision log.

## v0.2 Manual Workflow Prototype

Status: In progress

- Use existing video or audio files as input.
- Manually run transcription.
- Run Agent prompts with copied transcript.
- Export structured Markdown.
- Manually write results to Feishu.

Current local assets:

- `workflows/manual-video-diary-workflow.md`
- `templates/source-notes-template.md`
- `templates/daily-journal-template.md`
- `templates/memory-card-template.md`
- `schemas/diary-entry.schema.json`
- `examples/sample-diary-entry.json`
- `examples/sample-final-journal.md`

Next validation:

- Process one real or simulated 3 to 5 minute diary transcript.
- Check whether the final journal is useful enough for weekly reuse.
- Confirm which fields should be mandatory before automation.

## v0.3 Local Automation

Status: Planned

- Add local script for transcript ingestion.
- Generate a structured diary JSON file.
- Chain Agent prompts in a repeatable workflow.
- Save outputs to local folders.

## v0.4 Feishu Integration

Status: Planned

- Create Feishu document templates.
- Add sync workflow for diary entries and memory cards.
- Handle authorization, folder selection, and duplicate prevention.

## v0.5 Memory System

Status: Planned

- Add memory candidate review.
- Support confirmed, rejected, and updated memory states.
- Add search by person, project, goal, and theme.

## v1.0 Usable Product

Status: Planned

- Provide a simple interface for upload, review, edit, and sync.
- Support recurring diary workflow.
- Maintain a persistent personal memory store.
- Generate content drafts from selected diary entries.
