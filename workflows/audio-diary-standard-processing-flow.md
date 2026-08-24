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
standard-parsed-note.md
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

## Step 5: Generate Standard Parsed Note

Use:

```text
prompts/audio-diary-standard-parser.md
```

Input:

- `transcript-raw.txt`
- `transcript-raw.json` if timestamps are needed
- source metadata such as duration and speaker count

Output:

```text
standard-parsed-note.md
```

The result should match the ideal Feishu format:

- 智能总结
- 录音信息
- 录音总结
- thematic summary sections
- 章节概要
- 金句精选
- 待办事项
- 处理说明

## Step 6: Create Feishu Wiki Child Document

Create a child document under the target root or date node:

```bash
lark-cli docs +create \
  --profile siyangyuan-tiantu \
  --as user \
  --title "YYYY-MM-DD" \
  --wiki-node "YCRZwOZ8GibC7pkt9L1cHh8enXf" \
  --markdown @entries/YYYY-MM-DD-daily-reflection/standard-parsed-note.md
```

If creating a derivative such as a video script under the daily note, use the daily note's wiki node token as `--wiki-node`.

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

