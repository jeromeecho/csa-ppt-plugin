# Local PPT Generate Workflow

Use this workflow to create a brand-new presentation locally.

The generation path is:

1. gather source material locally
2. convert local files or search notes into reference text
3. run `scripts/run_ppt_write.py` in `generate` mode
4. deliver the local `.pptx`

## 1. Gather source material

Any of the following can be used:

- the user's prompt itself
- notes already present in the conversation
- local files such as `.md`, `.txt`, `.docx`, `.csv`, `.json`, `.html`, `.pptx`
- notes gathered from the user's local web-search MCP server

If the user needs fresh information, use the local web-search MCP server first, then save the distilled notes into a local markdown or text file.

## 2. Prepare reference text

### Option A: pass local files directly

`run_ppt_write.py` can parse repeated local reference paths directly:

```bash
$PYTHON_CMD scripts/run_ppt_write.py "AI agent market overview" \
  --mode generate \
  --reference-path /absolute/path/notes.md \
  --reference-path /absolute/path/report.docx \
  -o /absolute/path/output.pptx
```

### Option B: pre-parse a file

```bash
$PYTHON_CMD scripts/parse_file.py /absolute/path/report.docx -o /tmp/report.txt
```

Then feed the parsed output back as a reference file:

```bash
$PYTHON_CMD scripts/run_ppt_write.py "AI agent market overview" \
  --mode generate \
  --reference-file /tmp/report.txt \
  -o /absolute/path/output.pptx
```

### Option C: merge multiple search-note files

If you collected several note files from MCP web search results, merge them into one markdown file:

```bash
$PYTHON_CMD scripts/web_search.py /tmp/search-1.md /tmp/search-2.md \
  --title "AI agent market reference" \
  --query "AI agent market 2026" \
  -o /tmp/ppt_reference.md
```

Then run generation with that merged reference file.

## 3. Run local generation

Minimal command:

```bash
$PYTHON_CMD scripts/run_ppt_write.py "Topic or user request" \
  --mode generate \
  --language Chinese \
  -o /absolute/path/output.pptx
```

Recommended command with source material:

```bash
$PYTHON_CMD scripts/run_ppt_write.py "8-page investor update on AI agents" \
  --mode generate \
  --language English \
  --reference-file /tmp/ppt_reference.md \
  --reference-path /absolute/path/internal-notes.md \
  --max-slides 8 \
  -o /absolute/path/output.pptx
```

## 4. Output interpretation

On success the script prints:

- `RESULT: success`
- `MODE: generate`
- `OUTPUT_FILE: ...`
- `SLIDE_COUNT: ...`
- `SLIDE_TITLES: [...]`

## 5. Visual Validation (MANDATORY — do NOT skip)

**This step is required before delivering any output.**

Run validation:

```bash
$PYTHON_CMD "$CSA_SCRIPTS/validate_visual.py" /absolute/path/output.pptx --output /tmp/ppt_validation.json
```

If exit code is 1 (issues found), auto-fix:

```bash
$PYTHON_CMD "$CSA_SCRIPTS/fix_overflow.py" /absolute/path/output.pptx \
  --report /tmp/ppt_validation.json \
  -o /absolute/path/output.pptx
```

Re-validate:

```bash
$PYTHON_CMD "$CSA_SCRIPTS/validate_visual.py" /absolute/path/output.pptx --output /tmp/ppt_validation.json
```

- If PASS → proceed to deliver
- If FAIL on newly generated slides → go back to step 3, adjust the generation parameters (reduce content, increase text box sizes in ppt_core.py) and regenerate
- If FAIL only on pre-existing content with minor overflow (< 0.1") → acceptable, deliver with note

## 6. Deliver

1. the local absolute output path
2. slide count
3. slide titles or a brief content summary
4. validation status (PASS / number of remaining minor issues)

## Notes

- The local generator builds a structured outline from the prompt and reference text.
- If the user wants a very specific structure, provide an explicit outline JSON via `--outline` or `--outline-file` instead of relying on auto-outline generation.
- This workflow does not call any remote PPT generation service.
- **Validation is non-negotiable** — the task is NOT complete until validation passes.