# Parrot Audio Pipeline

Parrot Audio Pipeline is a step-by-step workspace for turning text datasets into speech datasets for ASR experiments. The current pipeline builds a synthetic English radiology speech dataset from PARROT v1.0 reports, normalizes the text for speech, renders Kokoro TTS audio, chunks long reports, validates audio/metadata pairs, and packages the result as a Hugging Face `datasets` dataset.

This project lives at `ysdede/parrot-audio-pipeline`.

This repo should remain the PARROT-dedicated finished work: it shows the real decisions, fixes, data stages, and scripts used to create the dataset. A cleaner generic skeleton can be extracted from this repo after the PARROT workflow is documented.

## What this repo contains

- Source acquisition notes and scripts under `sources/` and `tools/`.
- PARROT-specific text preparation stages under `data/PARROT_v1.0/01_*` through `05_*`.
- LLM normalization helpers under `deepseek-processor/` and `genai_tts_normalizer/`.
- Kokoro rendering entry points such as `tts_renderer_kokoro_v3.py`.
- Dataset packaging scripts under `data/PARROT_v1.0/dataset_creation_scripts/`.
- Tiny publishable examples under `examples/parrot-mini/`.
- A publishing plan and reusable-project extraction notes under `docs/`.

The PARROT source data is CC licensed and can be shared with attribution. The practical GitHub rule is size and clarity: keep small source samples, scripts, documentation, and attribution in Git; keep huge generated intermediates, rendered audio, packaged datasets, local model files, caches, logs, and credentials out of normal Git history.

## Pipeline Overview

1. **Load source text**
   - Start from PARROT v1.0 JSONL source data.
   - Convert JSONL to CSV with escaped newlines.
   - Extract the English `translation` field for downstream processing.

2. **Normalize raw text**
   - Normalize Unicode line separators and escaped newline markers.
   - Analyze unusual characters, markup, repeated patterns, and encoding issues.
   - Apply deterministic cleanup for known corruption patterns.

3. **Create TTS-ready text**
   - Send cleaned reports through an LLM prompt that returns two aligned forms:
     - `standardized`: the intended ASR ground truth.
     - `tts`: a spoken-form rendering suitable for TTS.
   - Store `sentence_pairs` so the renderer can synthesize sentence-level audio and preserve aligned metadata.

4. **Render audio**
   - Use Kokoro 82M voices through `tts_renderer_kokoro_v3.py`.
   - Randomize speaker, gender, speaking speed, and volume.
   - Render full reports, then chunk them at sentence boundaries so clips stay under the target duration.
   - Write per-clip JSON metadata with hashes, transcription, speaker, speed, volume, and duration.

5. **Align vocabulary and metadata**
   - Compare text characters against the target ASR model vocabulary.
   - Apply explicit replacements for unsupported markup, symbols, measurements, and punctuation.
   - Regenerate and validate the final corpus after edits.

6. **Package dataset**
   - Convert WAV output to compressed MP3 when desired.
   - Pair audio files with JSON labels.
   - Build train/test/validation splits with Hugging Face `datasets`.
   - Validate audio duration with `ffprobe` and write a dataset card.

## Minimal Example

The `examples/parrot-mini/` folder shows the shape of the pipeline without publishing the full dataset:

- `source.jsonl`: tiny source records.
- `translations.txt`: extracted text.
- `sentence_pairs.csv`: aligned standardized/TTS text.
- `label.json`: example renderer metadata for one chunk.

These files are intentionally small and safe for GitHub. They document the contract between stages.

## Local Data Layout

The full local run uses this shape:

```text
data/PARROT_v1.0/
  01_convert_jsonl_to_csv/
  02_extract_translation_column/
  03_normalize_line_separators/
  04_analyze_patterns/
  05_fix_text_corruptions/
  06_llm_fix/              # generated LLM outputs, local
  07_audio/                # generated audio and labels, local
  08_vocab/                # generated vocabulary checks, local
  09_dataset_clean/        # packaged HF dataset, local except README
```

Only scripts, documentation, tiny examples, and deliberately selected small data files should be committed. Full generated datasets and audio belong in local storage, release artifacts, or Hugging Face Datasets. Licensed upstream data can be linked, credited, mirrored as a release asset, or included only when it stays small enough for normal Git use.

## Requirements

The full pipeline uses Python plus optional GPU audio dependencies:

- `pandas`
- `numpy`
- `torch`
- `torchaudio`
- `soundfile`
- `kokoro`
- `datasets`
- `rich`
- `python-dotenv`
- `transformers`
- `ffmpeg` / `ffprobe`

LLM normalization scripts expect API keys in environment variables or local `.env` files. Do not commit `.env` files.

## Typical Commands

Run each command from the repo root unless the script says otherwise.

```powershell
python data/PARROT_v1.0/01_convert_jsonl_to_csv/01_convert_jsonl_to_csv.py
python data/PARROT_v1.0/02_extract_translation_column/02_extract_translation_column.py
python data/PARROT_v1.0/03_normalize_line_separators/03_normalize_line_separators.py
python data/PARROT_v1.0/04_analyze_patterns/04_analyze_patterns.py
python data/PARROT_v1.0/05_fix_text_corruptions/05_fix_text_corruptions.py
python deepseek-processor/parrot_batch_v4.py --help
python tts_renderer_kokoro_v3.py --help
python data/PARROT_v1.0/dataset_creation_scripts/create_parrot_hf_dataset_v2.py
```

Some older scripts contain absolute local paths. Treat them as captured working scripts until they are parameterized.

## Publishing To GitHub

Before pushing:

1. Keep generated files ignored.
2. Remove already-tracked generated files from the index with `git rm --cached`, not by deleting local data.
3. Commit docs, scripts, and examples.
4. Put large final datasets on Hugging Face or GitHub Releases instead of normal Git history.

See `docs/PUBLISHING.md` for a concrete cleanup checklist.

See `docs/REUSE_STRATEGY.md` for the split between this PARROT-specific project and the reusable skeleton project.

See `docs/TEXT_TO_AUDIO_DATASET_METHOD.md` for the reusable method distilled from this project.

## Dataset Card

The generated dataset card currently lives at `data/PARROT_v1.0/09_dataset_clean/README.md`. It documents the synthetic PARROT radiology ASR dataset, source attribution, splits, limitations, license, and citation text.

## License And Attribution

This pipeline derives its current dataset from PARROT v1.0, which is licensed CC BY-NC-SA 4.0. Any published derivative dataset should preserve the source attribution and compatible license terms.
