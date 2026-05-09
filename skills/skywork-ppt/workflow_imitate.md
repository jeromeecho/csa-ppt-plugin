# Local PPT Template Workflow

Use this workflow when the user provides a local `.pptx` template and wants a new deck that follows its layouts or theme.

The template workflow is still local:

1. inspect the template locally
2. gather content reference material locally
3. render a new deck with `--template-file`

## 1. Confirm the template path

The template must be a local `.pptx` path.

Examples:

- `/absolute/path/template.pptx`
- a file inside the workspace
- a temporary local file provided by the editor

If the path is ambiguous, ask for the exact local path.

## 2. Analyze the template first

Inspect the available layouts and sample slide titles:

```bash
$PYTHON_CMD scripts/analyze_template.py /absolute/path/template.pptx --json
```

Use this to understand:

- slide count
- page size
- layout names
- whether the template is title-heavy, section-heavy, or body-heavy

## 3. Gather reference material

Use the same local reference preparation options as the generate workflow:

- `--reference-path` repeated for local files
- `--reference-file` for prebuilt notes
- `scripts/web_search.py` to merge MCP search notes

## 4. Run template-based generation

```bash
$PYTHON_CMD scripts/run_ppt_write.py "Quarterly business review" \
  --mode template \
  --language Chinese \
  --template-file /absolute/path/template.pptx \
  --reference-file /tmp/ppt_reference.md \
  --max-slides 10 \
  -o /absolute/path/output.pptx
```

You can also pass local source files directly:

```bash
$PYTHON_CMD scripts/run_ppt_write.py "Quarterly business review" \
  --mode template \
  --template-file /absolute/path/template.pptx \
  --reference-path /absolute/path/notes.md \
  --reference-path /absolute/path/source.pptx \
  -o /absolute/path/output.pptx
```

## 5. Output interpretation

On success the script prints:

- `RESULT: success`
- `MODE: template`
- `OUTPUT_FILE: ...`
- `SLIDE_COUNT: ...`
- `SLIDE_TITLES: [...]`

## 6. Visual Validation (MANDATORY — do NOT skip)

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

Re-validate. Repeat until pass or report remaining issues.

## 7. Deliver

1. the output path
2. the template file used
3. the generated slide summary
4. validation status (PASS / number of remaining minor issues)

## Notes

- The template file supplies theme, masters, and layout selection context.
- This is local template reuse, not remote template matching.
- If the user needs exact placeholder-by-placeholder remapping, inspect the template first and provide an explicit outline JSON to control slide structure more tightly.
- **Validation is non-negotiable** — the task is NOT complete until validation passes.