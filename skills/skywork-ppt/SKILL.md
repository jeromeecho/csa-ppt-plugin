---
name: skywork-ppt
description: "Use this skill for local PPTX slide operations: inspect slide count and titles, delete specific slides, reorder slides, extract a subset of slides into a new file, and merge multiple PPTX files. Also supports editing existing PPTX via JSON edit plan and template-based generation. For creating new presentations from scratch, prefer the pptx skill (html2pptx) instead. Python 3.8+ is required."
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Local PPT Skill

This skill is fully local.

- No Skywork login
- No OSS/CDN upload
- No account membership checks
- No remote generation backend

All PPT generation, template-based generation, editing, and file operations run against local files in `skywork-ppt/scripts`.

## Supported workflows

| User intent | Workflow |
|-------------|----------|
| Generate a new PPT from a topic, notes, or local source files | `workflow_generate.md` |
| Use a local `.pptx` as a style/layout template | `workflow_imitate.md` |
| Edit an existing local `.pptx` | `workflow_edit.md` |
| View / delete / reorder / extract / merge slides | `workflow_local.md` |

## Environment check

Run this before invoking any script:

```bash
PYTHON_CMD=""
for cmd in python3 python python3.13 python3.12 python3.11 python3.10 python3.9 python3.8; do
  if command -v "$cmd" >/dev/null 2>&1 && "$cmd" -c "import sys; raise SystemExit(0 if sys.version_info >= (3,8) else 1)" 2>/dev/null; then
    PYTHON_CMD="$cmd"
    break
  fi
done

if [ -z "$PYTHON_CMD" ]; then
  echo "ERROR: Python 3.8+ not found."
  exit 1
fi

echo "Found Python: $PYTHON_CMD ($($PYTHON_CMD --version))"
$PYTHON_CMD -m pip install -q python-pptx
```

Use the resolved `$PYTHON_CMD` in every subsequent command.

## Routing rules

### 1. Generate a new PPT

Read `workflow_generate.md` before acting.

Use this when the user wants a brand-new presentation from:

- a topic
- reference notes already in the conversation
- local source files such as `.md`, `.txt`, `.docx`, `.csv`, `.json`, `.html`, or `.pptx`
- notes collected from the user's local web-search MCP server

Primary script:

```bash
$PYTHON_CMD scripts/run_ppt_write.py "topic or request" --mode generate -o /absolute/path/output.pptx
```

### 2. Generate from a local template

Read `workflow_imitate.md` before acting.

Use this when the user provides a local `.pptx` and wants the new deck to follow its layouts, theme, or visual rhythm.

Primary script:

```bash
$PYTHON_CMD scripts/run_ppt_write.py "topic or request" --mode template --template-file /absolute/path/template.pptx -o /absolute/path/output.pptx
```

### 3. Edit an existing PPT locally

Read `workflow_edit.md` before acting.

Use this when the user wants to modify an existing local `.pptx`. The edit flow is local and deterministic:

1. inspect the file
2. build a local edit plan JSON
3. apply it with `run_ppt_write.py`

Primary script:

```bash
$PYTHON_CMD scripts/run_ppt_write.py --mode edit --pptx-file /absolute/path/input.pptx --edit-plan-file /absolute/path/edit-plan.json -o /absolute/path/output.pptx
```

### 4. Direct local slide operations

Read `workflow_local.md` before acting.

Use `scripts/local_pptx_ops.py` for direct structural operations:

- `info`
- `delete`
- `reorder`
- `extract`
- `merge`

## Reference material handling

This skill expects web research to happen through the user's configured local MCP web search tools.

Recommended pattern:

1. run web searches with the local MCP server
2. save the distilled notes to one or more local `.md` or `.txt` files
3. optionally merge them with `scripts/web_search.py`
4. pass the result to `run_ppt_write.py` via `--reference-file` or pass source files directly with repeated `--reference-path`

## Local helper scripts

| Script | Purpose |
|--------|---------|
| `scripts/run_ppt_write.py` | Local generation, template generation, and edit entrypoint |
| `scripts/ppt_core.py` | Core rendering, template analysis, text extraction, edit application |
| `scripts/analyze_template.py` | Inspect a local template's layouts and sample titles |
| `scripts/parse_file.py` | Parse local source files into plain text |
| `scripts/web_search.py` | Merge locally saved search notes into one reference markdown file |
| `scripts/local_pptx_ops.py` | Direct local slide operations |

## Dependency summary

- Python 3.8+
- `python-pptx`

No other service is required for the base workflow.