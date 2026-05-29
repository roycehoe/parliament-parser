# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
poetry install          # install dependencies
python main.py          # run the parser (debug mode — prints raw lines)
python test.py          # parse 5 random data/ files, write results to sample_output/
```

There is no test framework or linter configured.

## What this project does

Parses Singapore Parliament Hansard records. Input is JSON files in `data/` (one per sitting, named `DD-MM-YYYY.json`), each containing an `htmlFullContent` field. Output is a list of dicts — one per line of the document — with structured tags added by a sequential pipeline.

## Pipeline architecture

`main.py` orchestrates a sequential tagging pipeline. Each stage reads the list of dicts from the previous stage and returns a new list with one additional field added per dict:

1. **`cleaining.py`** — pre-processes raw HTML: strips `&nbsp;`, removes column/page markers with regex
2. **`tagging/section.py`** → adds `section` (`meta` | `attendance` | `transcript` | `annex`) — detects section boundaries by scanning for sentinel strings (e.g. `"PRESENT:"`, `"ORAL ANSWERS TO QUESTIONS"`, `"Adjourned accordingly at"`)
3. **`tagging/transcript.py`** → adds `transcript_tag` (`title` | `subtitle` | `blank` | `speech` | `contd_text`) — classifies markdown-formatted lines by regex patterns on bold text; only set within `transcript` section
4. **`tagging/attendance.py`** → adds `attendance_tag` — classifies attendance section lines; only set within `attendance` section
5. **`tagging/speaker.py`** → adds `speaker` — tracks current speaker by detecting lines that start with a bold name followed by a colon; only set within `transcript` section
6. **`tagging/topic.py`** → adds `title` and `subtitle` — propagates the most recent `TITLE`/`SUBTITLE` line forward; TITLE/SUBTITLE lines themselves are consumed and not emitted into the result
7. **`tagging/speech_type.py`** → adds `speech_type` (`question` | `answer`) — the first speaker on a new topic becomes the questioner; all other speakers are `answer`; once someone else has answered, the original questioner's subsequent lines also become `answer`

## Output shape

Each dict in the output list has:
```
line, text, section, transcript_tag, attendance_tag, speaker, title, subtitle, speech_type
```
Tags outside their relevant section are `None` (e.g. `speaker` is `None` in the `attendance` section).

## Tagging module conventions

Each `tagging/` module follows the same pattern:
- `get_X_line_type(text: str) -> XLineType` — classifies a single line (used independently in tests/debugging)
- `get_X_tagged_handsard(handsard_lines_data: list[dict]) -> list[dict]` — processes the full document, adding the tag field

When adding a new tagging stage, follow this pattern and add it to the pipeline in `main.py`.
