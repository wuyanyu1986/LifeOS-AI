# Architecture Decisions

This file records important product and technical decisions for LifeOS AI.

## ADR-001: Start With Documentation First

Status: Accepted

Decision:

Start the project with product documents, prompts, roadmap, and architecture notes before implementation.

Reason:

The problem involves personal memory, privacy, Agent behavior, and knowledge structure. A clear product foundation reduces rework before code is added.

## ADR-002: Use Multi-Agent Workflow

Status: Accepted

Decision:

Use separate Agents for diary analysis, cognitive challenge, memory extraction, and content generation.

Reason:

Each task has different success criteria and risk boundaries. Separating them makes prompts easier to test and improve.

## ADR-003: Use Feishu Knowledge Base as Early Storage Surface

Status: Proposed

Decision:

Use Feishu documents and knowledge base pages as the first user-facing storage surface.

Reason:

Feishu already supports structured documents, folders, permissions, and collaboration. It allows early validation without building a full app.

## ADR-004: Keep Original Source Traceability

Status: Accepted

Decision:

Every structured diary, memory card, and content draft should preserve a link or reference to the original diary source.

Reason:

AI summaries can lose nuance or introduce errors. Traceability lets the user verify important claims and correct memory.

