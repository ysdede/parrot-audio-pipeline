# Publishing Checklist

Use this checklist before updating GitHub.

## Recommended Repository Name

The current remote is `ysdede/scribe-ds`. The project reads more clearly as one of:

- `parrot-audio-pipeline`
- `parrot-audio`
- `text-to-audio-dataset-pipeline`

`parrot-audio-pipeline` is the most explicit name because this repo is not only the final dataset. It is the process for creating the dataset.

## What To Commit

Commit:

- Pipeline scripts.
- Prompt templates and non-secret configuration templates.
- Root documentation.
- Dataset card documentation.
- Tiny examples under `examples/`.
- Empty directory markers such as `.gitkeep` when useful.

Do not commit:

- Very large source corpora copied from external datasets, even when the license allows redistribution.
- Generated intermediate CSV/TXT/JSON corpora unless they are intentionally small examples or useful audit artifacts.
- WAV/MP3/FLAC audio.
- Parquet/Arrow Hugging Face dataset builds.
- Local model checkouts, voice binaries, tokenizer folders, caches, logs, or `.env` files.

The issue is repository weight, not the PARROT license. CC-licensed source data may be shared with attribution, but large files are better handled through Hugging Face Datasets, GitHub Releases, or documented download steps.

## Safe Cleanup For Already-Tracked Generated Files

`.gitignore` only affects new files. This repository already has some generated files tracked, so use `git rm --cached` to remove them from future commits while keeping local copies on disk.

Review first:

```powershell
git ls-files data sources notebooks tmp | sort
```

Then untrack generated outputs:

```powershell
git rm --cached data/PARROT_v1.0/01_convert_jsonl_to_csv/PARROT_v1_0_escaped.csv
git rm --cached data/PARROT_v1.0/02_extract_translation_column/PARROT_v1_0_translations.txt
git rm --cached data/PARROT_v1.0/03_normalize_line_separators/PARROT_v1_0_translations_normalized.txt
git rm --cached data/PARROT_v1.0/04_analyze_patterns/character_set_analysis_report.txt
git rm --cached data/PARROT_v1.0/04_analyze_patterns/exact_pattern_counts.txt
git rm --cached data/PARROT_v1.0/04_analyze_patterns/pattern_analysis.json
git rm --cached data/PARROT_v1.0/04_analyze_patterns/pattern_analysis_report.txt
git rm --cached data/PARROT_v1.0/05_fix_text_corruptions/PARROT_v1_0_050_cleaned.txt
git rm --cached data/PARROT_v1.0/05_fix_text_corruptions/PARROT_v1_0_051_english_only.txt
git rm --cached data/PARROT_v1.0/05_fix_text_corruptions/PARROT_v1_0_051_polish_reports.txt
git rm --cached data/PARROT_v1.0/05_fix_text_corruptions/PARROT_v1_0_052_transcription_fixed.txt
git rm --cached data/PARROT_v1.0/05_fix_text_corruptions/PARROT_v1_0_053.txt
git rm --cached data/PARROT_v1.0/05_fix_text_corruptions/analysis_patterns/pattern_analysis.txt
git rm --cached data/PARROT_v1.0/05_fix_text_corruptions/analysis_patterns/pattern_analysis_report.txt
git rm --cached data/PARROT_v1.0/05_fix_text_corruptions/exact_pattern_counts.txt
git rm --cached data/PARROT_v1.0/05_fix_text_corruptions/polish_removal_summary.txt
git rm --cached data/PARROT_v1.0/05_fix_text_corruptions/search_patterns.txt
git rm --cached data/PARROT_v1.0/05_fix_text_corruptions/text_cleaning_summary.txt
git rm --cached data/PARROT_v1.0/05_fix_text_corruptions/wordset2.txt
```

Consider whether these source snapshots should stay tracked. If they are small enough and useful for reproducibility, keep them with clear attribution. If they make the repository heavy, move them to a release artifact or keep only source instructions:

```powershell
git rm --cached sources/PARROT_v1.0/data/PARROT_v1_0.jsonl
git rm --cached sources/raddar-chest-xrays-indiana-university/indiana_reports.csv.zip
git rm --cached sources/tboyle10-medicaltranscriptions/archive.zip
```

After cleanup:

```powershell
git status --short
git add README.md docs/PUBLISHING.md .gitignore examples/parrot-mini
git commit -m "docs: describe parrot audio pipeline"
git push origin main
```

## GitHub Rename Steps

1. Rename the repository on GitHub: `Settings -> General -> Repository name`.
2. Pick `parrot-audio-pipeline` unless you want a shorter brand name.
3. Update the local remote:

```powershell
git remote set-url origin git@github.com:ysdede/parrot-audio-pipeline.git
git remote -v
```

GitHub usually redirects old clone URLs, but updating the remote keeps local scripts and notes clear.
