# Reuse Strategy

This repository can go in two useful directions:

1. Finish it as a PARROT-specific project.
2. Extract a generic text-to-audio dataset skeleton from the lessons learned here.

The best order is to finish the PARROT project first, then extract the skeleton. The current folder structure, scripts, bug fixes, cleanup reports, and trial outputs are useful because they show how the dataset was actually made.

## Recommended Split

### Keep This Repo PARROT-Specific

Use this repo as the complete, reproducible story for the PARROT radiology ASR dataset:

- Source attribution and licensing for PARROT v1.0.
- Step-by-step data folders.
- Scripts that performed each transformation.
- Notes about text corruptions, line separators, LLM normalization, TTS rendering, chunking, metadata, vocabulary fixes, and Hugging Face packaging.
- Small examples that show data contracts between stages.
- Links to large outputs stored outside normal Git history.

This makes the repo a finished case study and a defensible dataset creation record.

### Extract A Generic Skeleton Later

Create a separate repo such as `text-to-audio-dataset-pipeline` or `audio-dataset-pipeline-template` after this one is cleaned up.

The skeleton should contain:

- Generic stage folders:
  - `01_load_source/`
  - `02_extract_text/`
  - `03_clean_text/`
  - `04_llm_normalize/`
  - `05_render_tts/`
  - `06_validate_audio/`
  - `07_package_dataset/`
- Config files instead of hard-coded dataset names.
- CLI arguments instead of local absolute paths.
- A small fake example dataset.
- A generic dataset card template.
- Clear extension points for different TTS engines, LLM providers, and packaging targets.

## What To Generalize

Good skeleton candidates from this repo:

- `sentence_pairs` as the contract between LLM normalization and TTS rendering.
- Per-chunk JSON metadata.
- Hash-based skip/resume behavior.
- Graceful shutdown during long rendering jobs.
- Audio validation before packaging.
- Vocabulary compatibility checks for the target ASR model.
- Split creation and Hugging Face dataset card generation.

## What To Leave PARROT-Specific

Keep these details in this repo:

- PARROT source attribution and domain description.
- Radiology-specific prompts.
- Medical terminology cleanup notes.
- PARROT folder names and versioned local artifacts.
- The actual dataset card for the generated PARROT ASR dataset.

## Publishing Principle

The source data license can allow sharing, but normal Git history should stay light. Commit enough to explain and reproduce the process; store large generated results somewhere designed for datasets.
