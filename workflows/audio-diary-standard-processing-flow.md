# Audio Diary Standard Processing Flow

This is the standard v0.2 workflow for turning one daily reflection recording into a Feishu-ready parsed note.

## Target Output

The standard parsed note must contain:

```text
### 📑 智能总结
#### 录音信息
#### 录音总结
#### 主题一
#### 主题二
...

### 📅 章节概要

### ✨ 金句精选

### 📋 待办事项

### 🔍 处理说明
```

This format is different from the video script format. It is a structured reflection note for the `每日成长` knowledge base.

## Local Inputs

Recording folder:

```text
/Users/wuyanyu/Desktop/每日感想录音记录
```

Feishu destination root:

```text
https://jp09qsvu8c.feishu.cn/wiki/YCRZwOZ8GibC7pkt9L1cHh8enXf
```

Feishu profile:

```text
siyangyuan-tiantu
```

## Step 1: Select Recording

Choose the target recording from:

```text
/Users/wuyanyu/Desktop/每日感想录音记录
```

Use the recording date as the entry title.

Example:

```text
2026-08-24.m4a -> 2026-08-24
```

## Step 2: Create Local Private Workspace

Create a local entry folder under ignored `entries/`:

```text
entries/YYYY-MM-DD-daily-reflection/
```

Suggested files:

```text
source-notes.md
transcript-raw.txt
transcript-raw.json
current-content.md
audio-parse-unabridged.md
processing-status.md
```

Do not commit `entries/` to Git.

## Step 3: Convert Audio

Convert M4A to 16kHz mono WAV:

```bash
ffmpeg -y \
  -i "/Users/wuyanyu/Desktop/每日感想录音记录/YYYY:MM:DD.m4a" \
  -ar 16000 \
  -ac 1 \
  -c:a pcm_s16le \
  "entries/YYYY-MM-DD-daily-reflection/audio/source.wav"
```

## Step 4: Transcribe Audio

Use local `whisper-cpp` with the multilingual base model:

```bash
/opt/homebrew/Cellar/whisper-cpp/1.9.2/bin/whisper-cli \
  --no-gpu \
  -m .models/ggml-base.bin \
  -l zh \
  -otxt \
  -oj \
  -of "entries/YYYY-MM-DD-daily-reflection/transcript-raw" \
  "entries/YYYY-MM-DD-daily-reflection/audio/source.wav"
```

Current model:

```text
.models/ggml-base.bin
```

## Step 5: Generate Two Parsed Outputs

Use:

```text
prompts/audio-diary-standard-parser.md
```

Input:

- `transcript-raw.txt`
- `transcript-raw.json` if timestamps are needed
- source metadata such as duration and speaker count

Outputs:

```text
current-content.md
audio-parse-unabridged.md
```

`current-content.md` must match the ideal Feishu format:

- 智能总结
- 录音信息
- 录音总结
- thematic summary sections
- 章节概要
- 金句精选
- 待办事项
- 处理说明

## Step 6: Create Feishu Wiki Child Documents

Create the current-content document under the target root or date node:

```bash
lark-cli docs +create \
  --profile siyangyuan-tiantu \
  --as user \
  --title "YYYY-MM-DD" \
  --wiki-node "YCRZwOZ8GibC7pkt9L1cHh8enXf" \
  --markdown @entries/YYYY-MM-DD-daily-reflection/current-content.md
```

Create the unabridged archive as a separate, clearly marked child document. It
must not replace the current-content document and should inherit the same
privacy access policy:

```bash
lark-cli docs +create \
  --profile siyangyuan-tiantu \
  --as user \
  --title "YYYY-MM-DD 音频解析无删减" \
  --wiki-node "YCRZwOZ8GibC7pkt9L1cHh8enXf" \
  --markdown @entries/YYYY-MM-DD-daily-reflection/audio-parse-unabridged.md
```

If creating a derivative such as a video script under the daily note, use the current-content document's wiki node token as `--wiki-node`.

## Step 7: Verify Feishu Output

Verify the created child node:

```bash
lark-cli wiki nodes list \
  --profile siyangyuan-tiantu \
  --as user \
  --params '{"space_id":"7618037226496543945","parent_node_token":"PARENT_NODE_TOKEN"}'
```

Fetch the created document:

```bash
lark-cli docs +fetch \
  --profile siyangyuan-tiantu \
  --as user \
  --doc "CREATED_DOC_OR_WIKI_URL" \
  --format pretty
```

## Step 8: Enter Parsed-Note Review

Do not generate a video script or WeChat article immediately after archiving.

The Wiki scanner must detect the new `YYYY-MM-DD` node, create a review-state record, and send a `标准解析稿待审核` Feishu message. Continue only after:

```text
parsed_note.status = approved
```

Use `workflows/standard-parsed-note-review.md` and `workflows/review-gated-diary-orchestration.md` for the review contract.

## Quality Checklist

- [ ] Audio file found
- [ ] WAV conversion completed
- [ ] Whisper transcription completed
- [ ] Obvious ASR errors corrected
- [ ] No invented facts
- [ ] Standard format followed
- [ ] 金句 are real or lightly corrected original lines
- [ ] 待办事项 only includes explicit actions
- [ ] Feishu child document created
- [ ] Feishu output verified
- [ ] `current-content.md` and `audio-parse-unabridged.md` both exist
- [ ] Unabridged file is complete, source-linked, and not summarized
- [ ] Parsed-note review reminder sent exactly once
- [ ] Parsed note explicitly approved before downstream generation
