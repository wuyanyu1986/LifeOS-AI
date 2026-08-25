# Workflow Registry

## By Workflow

| Workflow | Spec | Status | Trigger |
| --- | --- | --- | --- |
| Audio to parsed note | `audio-diary-standard-processing-flow.md` | Review | New local recording |
| Parsed-note review | `standard-parsed-note-review.md` | Draft | New Wiki date node detected |
| Review-gated orchestration | `review-gated-diary-orchestration.md` | Draft | Parsed-note review state created |
| Video generation | `video-diary-script-copy-generation-flow.md` | Review | Parsed note approved |
| Video review | `video-script-review.md` | Draft | Video document created or revised |
| WeChat article generation | `wechat-article-generation-flow.md` | Review | Parsed note approved |
| WeChat article review | `wechat-article-review.md` | Draft | Article document created or revised |

## By State

| State | Entered by | Exit condition |
| --- | --- | --- |
| `parsed_pending_review` | New date node detection | Approve or request changes |
| `parsed_changes_requested` | Parsed-note review | Revised note is resubmitted |
| `generating_derivatives` | Parsed-note approval | Both generation jobs settle |
| `derivatives_pending_review` | A derivative is created | Both derivatives approved |
| `ready_for_manual_publish` | Video and article approvals | Owner manually handles publishing |
| `completed` | Legacy entries only | Terminal |
| `failed` | Permanent processing failure | Manual retry or repair |
