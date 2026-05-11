# Caption cleaner

A small Python utility that cleans **WebVTT** (`.vtt`) subtitle files: it edits the caption text while leaving structure and timing cues intact.

## What it does

- **Removes filler words** — Standalone `um` and `uh` (case-insensitive, whole words only so words like `humor` are not changed).
- **Capitalizes “I”** — Standalone `i` and contractions such as `i'm` become `I` / `I'm`.
- **Normalizes spacing** — Collapses extra spaces and removes spaces before punctuation (`,.;:!?`).

The `WEBVTT` header, cue timestamps (`-->` lines), and overall cue layout are preserved. By default the input file is **overwritten**; use `-o` to write a different file.

After a run, the script prints counts for `um` removals, `uh` removals, and `I` capitalizations.

## Requirements

Python 3 (standard library only: `argparse`, `pathlib`, `re`).

## Usage

```bash
python script/caption_cleaner.py path/to/captions.vtt
```

Write to another file instead of overwriting:

```bash
python script/caption_cleaner.py path/to/captions.vtt -o path/to/captions.cleaned.vtt
```

## Credits

Concept: Lisa Raposa Millar  
Code generation and implementation: Cursor AI ([cursor.com](https://cursor.com)).

## License

MIT License (provided by the `caption-cleaner` contributors to the extent of rights they can grant). See `LICENSE` for details.
