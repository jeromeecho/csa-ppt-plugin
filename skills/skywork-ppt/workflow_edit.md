# Local PPT Edit Workflow

Use this workflow to modify an existing local `.pptx`.

The edit path is deterministic and local:

1. inspect the presentation
2. build an edit plan JSON
3. apply the plan with `run_ppt_write.py --mode edit`

## 1. Inspect the current deck

Get slide count and titles:

```bash
$PYTHON_CMD scripts/local_pptx_ops.py info --file /absolute/path/input.pptx
```

If you need more text context, extract slide text:

```bash
$PYTHON_CMD scripts/parse_file.py /absolute/path/input.pptx -o /tmp/input.txt
```

## 2. Build a local edit plan

Supported actions in the JSON plan:

- `update_text`
- `append_slide`
- `delete_slide`
- `reorder_slides`

Example edit plan:

```json
{
  "edits": [
    {
      "action": "update_text",
      "slide": 2,
      "title": "Updated Overview",
      "bullets": [
        "Current position",
        "Key risks",
        "Recommended action"
      ]
    },
    {
      "action": "append_slide",
      "type": "bullets",
      "title": "Next Steps",
      "bullets": [
        "Finalize scope",
        "Assign owners",
        "Track delivery milestones"
      ]
    }
  ]
}
```

Save the plan to a local file such as `/tmp/edit-plan.json`.

## 3. Apply the edit plan

```bash
$PYTHON_CMD scripts/run_ppt_write.py \
  --mode edit \
  --pptx-file /absolute/path/input.pptx \
  --edit-plan-file /tmp/edit-plan.json \
  -o /absolute/path/output.pptx
```

If you already have the edit JSON inline, you can pass it directly:

```bash
$PYTHON_CMD scripts/run_ppt_write.py \
  --mode edit \
  --pptx-file /absolute/path/input.pptx \
  --edit-plan '{"edits":[{"action":"delete_slide","slide":3}]}' \
  -o /absolute/path/output.pptx
```

## 4. Output interpretation

On success the script prints:

- `RESULT: success`
- `MODE: edit`
- `OUTPUT_FILE: ...`
- `SLIDE_COUNT: ...`
- `SUMMARY: [...]`

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
- If FAIL on edited slides → revise the edit plan (reduce text, adjust layout) and re-apply
- If FAIL only on untouched slides with minor overflow (< 0.1") → acceptable, deliver with note

## 6. Deliver

1. the output path
2. the applied change summary
3. any follow-up edits still needed
4. validation status (PASS / number of remaining minor issues)

## Notes

- The edit flow is local-file based only.
- There is no URL upload step.
- Slide references are 1-based in the edit plan.
- Reorder plans must include every slide exactly once.
- **Validation is non-negotiable** — the task is NOT complete until validation passes.