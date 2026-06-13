# Text-To-Audio Dataset Method

This document distills the reusable method learned from building the PARROT audio dataset. The important lesson is not only which scripts ran, but which contracts made the pipeline recoverable, auditable, and useful for ASR.

## Central Lesson

Do not treat "clean text" and "spoken text" as the same artifact.

For ASR, the dataset needs:

- `transcription`: the label the ASR model should learn.
- `normalized`: the text actually sent to TTS.
- `sentence_pairs`: the mapping between those two forms.

That split preserves truth while still letting TTS pronounce dates, units, acronyms, symbols, and line breaks naturally.

## Pipeline Pattern

1. **Load source data**
   - Preserve upstream attribution and license.
   - Convert the source to a stable JSONL/CSV shape.
   - Keep stable IDs and hashes for every source row.

2. **Extract the target text**
   - Pick the field that should become audio.
   - Keep one record per report/document.
   - Preserve line markers in a controlled way.

3. **Normalize deterministic problems**
   - Fix encoding and Unicode line separators.
   - Analyze unusual characters and repeated patterns.
   - Remove or isolate wrong-language records.
   - Keep summaries of what changed.

4. **Use LLM normalization for judgment-heavy work**
   - Produce `standardized` text for labels.
   - Produce `tts` text for speech.
   - Require sentence-level pairing.
   - Cache results by source hash.
   - Validate JSON shape before rendering.

5. **Render TTS audio**
   - Render from `tts`, not from `standardized`.
   - Keep speaker/speed/volume consistent within a report.
   - Use multiple voices when useful for robustness.
   - Support graceful shutdown and resume.

6. **Chunk and label**
   - Chunk at sentence boundaries.
   - Keep chunks below the target duration.
   - Write per-chunk JSON metadata with hashes, speaker, speed, volume, duration, and source IDs.

7. **Validate and repair**
   - Validate audio readability, sample rate, duration, and metadata.
   - Reprocess incomplete parent items instead of patching random chunks by hand.
   - Extract a final corpus and check target ASR vocabulary compatibility.
   - Apply explicit tracked text edits.

8. **Package and publish**
   - Build deterministic train/test/validation splits.
   - Use `transcription` as the ASR label field.
   - Save metrics and a dataset card.
   - Keep huge generated artifacts outside normal Git history.

## PARROT-Specific Discoveries

- The LLM output became much more useful after moving from whole-report `standardized_report` and `tts_script` fields to `sentence_pairs`.
- Structure markers such as `<NL>` and `<PARA>` belong in `standardized`/`transcription`, but not in `tts`.
- Long medical sentences must be split before rendering; otherwise natural chunking fails and clips exceed ASR-friendly duration.
- Hash-based skip logic needs validation. A file name alone does not prove a report rendered correctly.
- Keeping `normalized_hash` and `transcription_hash` separately matters because TTS text and ASR truth intentionally diverge.
- Vocabulary checks should happen after rendering metadata is created, because final labels may contain symbols that the target ASR tokenizer cannot represent.

## Reusable Folder Skeleton

```text
data/<dataset_name>/
  01_load_source/
  02_extract_text/
  03_clean_text/
  04_analyze_patterns/
  05_llm_normalize/
  06_render_tts/
  07_chunk_and_label/
  08_vocab_check/
  09_package_dataset/
```

Each stage should contain the script that produced the next artifact plus a small README or summary when a decision was made.

## Minimum Example Files

A reusable skeleton should include tiny examples for:

- `source.jsonl`
- extracted `texts.csv`
- LLM `sentence_pairs.csv`
- chunk `label.json`
- packaged dataset card template

These examples teach the contracts without putting large corpora or audio in Git.

## Publishing Policy

The PARROT source license allows sharing with attribution. The GitHub constraint is size, not permission.

Use GitHub for:

- source instructions and attribution
- scripts
- prompts without secrets
- tiny example data
- documentation and dataset cards

Use Hugging Face Datasets, releases, or external storage for:

- rendered audio
- Parquet/Arrow datasets
- huge intermediate corpora
- caches and logs
- local model files
