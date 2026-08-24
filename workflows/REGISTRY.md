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
| WeChat MP draft publishing | `wechat-mp-draft-publishing-flow.md` | Review | WeChat article approved |

## By State

| State | Entered by | Exit condition |
| --- | --- | --- |
| `parsed_pending_review` | New date node detection | Approve or request changes |
| `parsed_changes_requested` | Parsed-note review | Revised note is resubmitted |
| `generating_derivatives` | Parsed-note approval | Both generation jobs settle |
| `derivatives_pending_review` | A derivative is created | Both derivatives approved |
| `preparing_wechat_draft` | WeChat article approval | Draft created or configuration blocked |
| `wechat_draft_configuration_required` | Missing local WeChat credentials | Configuration supplied and retried |
| `wechat_draft_pending_review` | WeChat draft created | Manual review and publication in WeChat |
| `completed` | Legacy entries only | Terminal |
| `failed` | Permanent processing failure | Manual retry or repair |
