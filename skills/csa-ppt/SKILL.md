---
name: csa-ppt
description: >
  Unified presentation skill for Cloud Solution Architects. Orchestrates multiple
  specialized tools to create professional presentations, architecture diagrams, and
  technical content. Use this skill whenever the user mentions: creating slides, PPT,
  presentations, deck, 演示文稿, 幻灯片, architecture diagrams for slides, filling
  templates, customer demos, tech sharing, workshops, or any combination of diagrams +
  slides. Also trigger when the user provides a .pptx template to fill, asks to visualize
  cloud architectures (Azure, AWS, GCP, multi-cloud) in a presentation context, or needs
  Chinese-language slide content. This skill covers ALL presentation-related work — from
  a quick internal deck to a polished customer-facing solution demo with architecture
  diagrams.
metadata:
  author: huqianghui
  version: "1.4.0"
  license: MIT
---

# CSA Presentation Skill

You are helping a Cloud Solution Architect create presentations. This person
regularly delivers customer solution demos, internal tech deep-dives, workshop materials,
and architecture reviews. Content may cover Azure, AWS, GCP, multi-cloud, or hybrid
scenarios. They work across Chinese and English content and often receive templates from
event organizers or HR that need to be filled with content.

## ⛔ THREE INVIOLABLE RULES

**These are HARD CONSTRAINTS, not suggestions. Violation = broken output.**

### Rule 1: CLARIFY-BEFORE-PLAN — Ask questions when requirements are unclear

**Before creating ANY plan or workspace, check if the user's request is complete enough.**

If ANY of these are unknown, call the **AskUserQuestion** tool with 1–4 questions:

| Must Know | Example Question |
|-----------|-----------------|
| Slide count | "大约需要多少页幻灯片？(5-8页 / 8-12页 / 12-20页)" |
| Target audience | "面向的观众是？(客户决策者 / 技术团队 / 内部同事)" |
| Language | "使用什么语言？(中文 / English / 中英混合)" |
| Output format | "输出格式？(.pptx / HTML网页 / 两者都要)" |

**Optional** (ask only if not obvious from context):
- Visual style preference (professional / technical / workshop)
- Whether to include architecture diagrams
- Whether a template is provided
- Key messages or must-include content

**Rules for asking:**
- Do NOT ask if the user already specified it (e.g., "做一个10页的PPT" → slide count is known)
- Do NOT ask more than 4 questions — infer the rest from context
- Do NOT start `mkdir` or any work before questions are answered
- Ask ALL questions in ONE AskUserQuestion call, not multiple rounds
- If the request is very detailed, skip directly to Step 0

### Rule 2: FILE-FIRST — All work must be written to files

The workspace markdown files (task_plan.md, style_contract.md, findings.md) are the
**single source of truth**. Sub-agents READ these files. If they don't exist, sub-agents
have no input and produce garbage.

- Running `python3` (diagrams) before task_plan.md exists = FORBIDDEN
- Generating HTML/PPTX slides before style_contract.md exists = FORBIDDEN
- Creating ANY content before the workspace directory exists = FORBIDDEN
- The ONLY correct first action is: `mkdir -p outputs/{project}/...`

### Rule 3: UPDATE-AFTER-EVERY-TASK — Enable resume from interruption

**After completing ANY task (research, diagram, slide, assembly, review), IMMEDIATELY
update `task_plan.md` to mark that task `[x]`.**

This is critical because:
- Sessions can be interrupted at any time (`/clear`, timeout, crash)
- On resume, the FIRST thing to do is `Read task_plan.md` to see what's done
- If task_plan.md is not updated, resume starts from scratch = wasted work

**Resume protocol** (when starting a new session in an existing workspace):
1. Call `ls outputs/` to find existing project directories
2. Call Read tool → `outputs/{project}/task_plan.md`
3. Find the first unchecked `[ ]` task → continue from there
4. Do NOT redo tasks already marked `[x]`

---

## How This Skill Works

This skill orchestrates 5 specialized sub-skills and MCP integrations.
Every presentation follows a **Plan-first, slide-by-slide execution** workflow:

1. **Plan** — Break the presentation into a task plan where each slide/chapter = one task
2. **Define Style** — Lock down colors, fonts, layout rules BEFORE any slide is created
3. **Execute** — Complete slides one by one (or in parallel via sub-agents), checking off
   each task as it's done
4. **Assemble** — Combine all slides into the final deck
5. **Review** — Spawn the review sub-agent to check quality and style consistency (max 2
   rounds). Read `agents/review-agent.md` for the full review protocol.

### Scaling by Complexity

| Request Size | Planning | Workspace | Review |
|-------------|---------|-----------|--------|
| Simple (< 5 slides) | Single `task_plan.md` that includes style rules inline | Flat `outputs/{project}/` dir, no subdirs required | Quick self-check, no formal review agent |
| Standard (5-10 slides) | Full workspace with `task_plan.md` + `style_contract.md` + `progress.md` | Full directory structure with `diagrams/`, `slides/`, `final/` | Formal review agent, 1 round |
| Large (10+ slides) | Full workspace + parallel sub-agent dispatch | Full directory structure | Formal review agent, up to 2 rounds |

---

## CRITICAL: File-Based Workflow

**All work MUST be persisted to files.** Agents communicate through files, not through
conversation context. If it's not written to a file, it doesn't exist for the next phase.

**THEREFORE: Execute the steps below in EXACT ORDER. No reordering. No skipping.**

### Step 0: Initialize Workspace (ONLY after Rule 1 questions are answered)

Derive a short, descriptive project name from the user's request content:
- "帮我做Azure RAG方案的PPT" → `rag-demo`
- "AKS迁移到ACA的技术分享" → `aks-to-aca`
- "季度工作汇报" → `quarterly-report`

**For standard/large requests (5+ slides):**

```bash
mkdir -p outputs/{project-name}/{diagrams,slides,final}
```

Then write these 3 files using the Write tool:

1. **`task_plan.md`** — The master plan (see `references/templates.md` for template)
2. **`progress.md`** — Session log, updated after each step
3. **`style_contract.md`** — Standalone style rules for sub-agents to read

**For simple requests (< 5 slides):**

```bash
mkdir -p outputs/{project-name}
```

Write a single **`task_plan.md`** with style rules included inline (see the lightweight
variant in `references/templates.md`). No separate `style_contract.md` or `progress.md`
needed — the orchestrator tracks progress directly.

### Step 0.5: CHECKPOINT — Verify files exist

**For standard/large requests (5+ slides):**
```bash
ls -la outputs/{project}/task_plan.md outputs/{project}/style_contract.md outputs/{project}/progress.md
```
If ANY file is missing, go back to Step 0.

**For simple requests (< 5 slides):**
```bash
ls -la outputs/{project}/task_plan.md
```
Only `task_plan.md` is required (style rules are inline). **Do NOT proceed until confirmed.**

### Workspace Directory Structure

```
outputs/{project-name}/
├── task_plan.md              ← Master plan with checkboxes
├── progress.md               ← Session log (5+ slides only)
├── style_contract.md         ← Colors, fonts, layout rules (5+ slides only)
├── findings.md               ← Research results (Phase 1 output)
├── diagrams/
│   ├── manifest.md           ← List of diagrams generated
│   └── *.png                 ← Diagram images
├── slides/
│   ├── manifest.md           ← List of slides built (format per slide)
│   ├── slide-{N}.{pptx|html} ← Individual slide files
│   └── slide-{N}-notes.md    ← Speaker notes per slide
└── final/
    ├── final-deck.{pptx|html}← Assembled deck
    ├── assembly-report.md    ← What was assembled
    ├── review_report.md      ← Review agent output
    └── fix_summary.md        ← Fix agent output
```

**After completing EACH phase:**
1. Update `task_plan.md` — mark completed items `[x]`, update phase status
2. Append to `progress.md` — what was done, files created, any issues

---

## Execution Steps (1–8)

> See `references/templates.md` for full task_plan and style_contract templates.

### Step 1: Create the Slide Plan

After understanding the user's request, **write** `task_plan.md` to disk with one task
per slide or logical chapter. The plan must include:

- **Goal**: One-sentence summary of the presentation
- **Style Contract**: Color palette, fonts, language, density rules, output format
- **Phases**: Research → Diagrams → Slides → Assembly → Review, each with checkboxes

For simple requests (< 5 slides), use the lightweight variant from `references/templates.md`
with style rules inline in `task_plan.md`.

### Step 2: Lock the Style Contract (5+ slides only)

For 5+ slide decks, **write `style_contract.md`** as a standalone file so every sub-agent
can read it directly without parsing task_plan.md. See `references/templates.md` for the
template.

**Every sub-agent prompt must include**: "Read `style_contract.md` at
`outputs/{project-name}/style_contract.md` for all styling rules."

For simple requests (< 5 slides): skip this step — style rules are inline in `task_plan.md`.

### Step 3: Research (if needed) → Write findings to file

If the topic needs research (web search, cloud docs), do the research, then:

**Call Write tool** → file_path: `outputs/{project}/findings.md`

**Then immediately update task_plan.md** (Rule 3):
- Mark Phase 1 research tasks as `[x]`
- Append to `progress.md`: "Phase 1 complete. findings.md written." (5+ slides only)

### Step 4: PRE-CHECK before EVERY phase

**Before starting ANY phase (diagrams, slides, assembly, review), run this check:**

**For standard/large requests (5+ slides):**
```bash
ls outputs/{project}/task_plan.md outputs/{project}/style_contract.md
```
If either file is missing → STOP → go back to Step 0 and create them.

**For simple requests (< 5 slides):**
```bash
ls outputs/{project}/task_plan.md
```
Only `task_plan.md` is required.

Additionally, each phase must READ the outputs of previous phases:
- Before diagrams → READ `task_plan.md` + `style_contract.md` (or inline style in task_plan.md)
- Before slides → READ `task_plan.md` + `style_contract.md` (if exists) + `findings.md` (if exists) + check `diagrams/`
- Before assembly → READ `task_plan.md` + check `slides/` directory
- Before review → READ `style_contract.md` (or task_plan.md for simple) + check `final/` directory

**If a required input file does not exist, do NOT proceed. Create it first.**

### Step 5: Create diagrams and slides

Only NOW may you call sub-skills (azure-diagrams, frontend-slides, pptx, etc.).

**⛔ CRITICAL: Each slide MUST be saved as an INDIVIDUAL file in `slides/`.** Do NOT build
all slides in a single Presentation object and save directly to `final/`. The correct
pattern is:

```python
# CORRECT: One file per slide
for n in range(1, slide_count + 1):
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    # ... build slide content ...
    prs.save(f'outputs/{project}/slides/slide-{n}.pptx')

# WRONG: All slides in one file saved to final/
# prs = Presentation()
# for n in range(...): prs.slides.add_slide(...)
# prs.save('outputs/{project}/final/final-deck.pptx')  # FORBIDDEN
```

**AFTER EVERY artifact, update task_plan.md immediately** (Rule 3).

### Step 6: ⛔ MANDATORY GATE — Verify slides/ before assembly

**This gate is a HARD CONSTRAINT. Assembly CANNOT begin until it passes.**

```bash
SLIDE_COUNT=$(ls outputs/{project}/slides/slide-*.pptx outputs/{project}/slides/slide-*.html 2>/dev/null | wc -l)
echo "Found $SLIDE_COUNT individual slide files in slides/"
ls -la outputs/{project}/slides/
```

**Gate rules:**
- If `slides/` is EMPTY (0 files) → **STOP.** Go back to Step 5 and build individual slides.
- If `slides/` has fewer files than expected by `task_plan.md` → **STOP.** Build the missing slides first.
- If `slides/manifest.md` does not exist → **STOP.** Write the manifest first.
- Only proceed when: (a) `slides/` contains one file per planned slide, (b) `slides/manifest.md` exists, and (c) the file count matches `task_plan.md`.

**If you find yourself about to create a single Presentation() object and save it directly
to `final/`, you are violating this gate. STOP and restructure.**

### Step 7: Assembly (Phase 4) — ONLY after Step 6 gate passes

Spawn the **Assembly Agent** to merge individual slides into the final deck.
Read `agents/assembly-agent.md` for the full assembly protocol.

**After assembly:**
- Mark Phase 4 tasks as `[x]` in task_plan.md
- Append to `progress.md`: "Phase 4 complete. Final deck assembled."

### Step 8: Review & Fix (Phase 5) — ONLY after assembly is complete

Read `agents/review-agent.md` for the full review protocol. Max 2 rounds.

- **Round 1 — Full Review**: Spawn Review Agent → writes `review_report.md`
- **Apply Fixes (if NEEDS_FIX)**: Spawn Fix Agent → writes `fix_summary.md`
- **Round 2 — Verify Fixes**: Spawn Review Agent again (Round 2 mode)
- After Round 2: PASS → deliver; NEEDS_FIX → mark as KNOWN_ISSUES, deliver with report
- Do NOT loop a third time

**For simple requests (< 5 slides):** Skip the formal Review Agent. Do a quick self-check
instead (see Scaling by Complexity table above).

### Parallel Execution (10+ slides, optional)

For large presentations, use multiple sub-agents to build different chapters simultaneously.

**Can parallelize:** Independent content chapters, diagram generation, research tasks.
**Must be sequential:** Title/agenda (first), final assembly (last).

Each sub-agent MUST receive in its prompt:
1. The **workspace_path** — absolute path (e.g., `/full/path/to/outputs/rag-demo/`)
2. The **skill_root_path** — absolute path to the skills directory so agents can find sub-skill SKILL.md files (e.g., `/full/path/to/csa-ppt-plugin/skills/`)
3. Instruction to **read `style_contract.md`** from the workspace (or `task_plan.md` for simple requests)
4. The **sub-skill path** to read (e.g., `{skill_root_path}/pptx/SKILL.md`)
5. The **agent instructions** to read (e.g., `agents/slide-builder-agent.md`)

---

## Incremental Update Workflow

When the user wants to modify an existing presentation (e.g., "改一下第5页"):

1. **Read** the existing workspace files (`task_plan.md`, `style_contract.md`)
2. **Identify** which slides/phases are affected
3. **Re-execute** only the affected phases:
   - Content change on one slide → re-run Phase 3 for that slide only
   - New diagram needed → re-run Phase 2 for that diagram, then Phase 3 for embedding
   - Style change → update `style_contract.md`, re-run Phase 3 for all slides
4. **Re-assemble** (Phase 4) — always needed after any slide change
5. **Quick self-check** instead of formal review (unless the change is large)
6. Update `progress.md` with what was changed

Do NOT re-run the full 5-phase pipeline for incremental changes.

---

## Decision Framework

> ⛔ **PREREQUISITE**: Before using this framework, `task_plan.md` MUST already exist on
> disk. For 5+ slide decks, `style_contract.md` must also exist. If not, go back to Step 0.

Analyze the request along these dimensions, then route accordingly:

### 0. Combined Routing Rules (优先级最高)

> **云架构 PPT 强制规则**: 当 PPT 内容包含云架构（Azure/AWS/GCP 服务拓扑、网络架构、
> 数据流水线等），**必须**先调用 `azure-diagrams` 生成专业架构图 PNG，再将 PNG 嵌入
> `pptx`(html2pptx) 幻灯片。禁止用 inline SVG/matplotlib 替代 azure-diagrams 画云架构图。

| 场景 | 组合流程 | 说明 |
|------|---------|------|
| PPT 含云架构图 | **azure-diagrams** → **pptx** | 先生成 PNG，再嵌入 html2pptx 幻灯片 |
| PPT 含流程图/泳道图 | **azure-diagrams** → **pptx** | graphviz 泳道图比 inline SVG 更专业 |
| PPT 含手绘概念图 | **excalidraw-diagram** → **pptx** | 先生成 .excalidraw + PNG，再嵌入幻灯片 |
| 纯文字/数据图表 PPT | **pptx** 单独完成 | 柱状图/饼图等用 PptxGenJS 内置即可 |

**判断方法**:
- 运行 `azure-diagrams/scripts/detect_cloud_arch.py` 分析幻灯片大纲，自动识别需要 azure-diagrams 的 slides。
- 运行 `excalidraw-diagram/scripts/detect_excalidraw.py detect` 识别需要手绘风格图的 slides。
- 图生成完成后，运行 `excalidraw-diagram/scripts/detect_excalidraw.py validate` 验证输出确实来自 excalidraw-diagram skill（必须有 .excalidraw JSON 源文件 + 渲染 PNG）。

### 1. What's the primary content type?

| Content | Best Tool | Why |
|---------|-----------|-----|
| Cloud architecture diagram (Azure, AWS, GCP) | **azure-diagrams** | 700+ official cloud icons, professional layout |
| Hand-drawn / conceptual diagram | **excalidraw-diagram** | Whiteboard aesthetic, great for brainstorming visuals |
| Swimlane / business process flow | **azure-diagrams** (matplotlib) | Built-in swimlane support |
| Sequence / auth flow | **azure-diagrams** | Dedicated sequence diagram patterns |
| Design mockup / wireframe | **Figma** or **Pencil** MCP | Interactive design tools |

### 2. What's the delivery format?

| Scenario | Format | Tool Chain |
|----------|--------|------------|
| Given a .pptx template to fill | .pptx | **skywork-ppt** (template workflow) or **pptx** (OOXML for complex templates) |
| Customer-facing formal deck | .pptx | **pptx** (html2pptx for rich layouts) |
| Internal sharing / demo | HTML or .pptx | **frontend-slides** if animation/中文 heavy; otherwise **pptx** |
| Architecture review document | Images + .pptx | **azure-diagrams** → embed in **pptx** |
| Workshop hands-on guide | HTML | **frontend-slides** (step-by-step with code blocks renders best in HTML) |
| Slide manipulation (delete/merge/reorder) | .pptx | **skywork-ppt** (local_pptx_ops.py) |

### 3. Language & encoding considerations

- **Chinese-heavy content (中文为主)**: Prefer **frontend-slides** (HTML) — it avoids
  font embedding issues that plague .pptx generation. If .pptx is required, use
  **pptx** (html2pptx.js) which handles CJK better than python-pptx.
- **English or mixed**: Any tool works fine.
- **Code snippets**: **frontend-slides** renders code beautifully with syntax highlighting.
  For .pptx, use **pptx** with monospace font blocks.

### 4. Template handling

When the user provides a template:

1. **Inspect first**: Read the template to understand its layouts, color scheme, and
   placeholder structure
2. **Choose the right tool**:
   - Simple content fill (text + images) → **skywork-ppt** `workflow_imitate.md`
   - Complex layout changes or strict formatting → **pptx** OOXML workflow
3. **Preserve template integrity**: Never change the template's master slides, color
   scheme, or font theme unless explicitly asked

## Common CSA Workflows

Read the appropriate reference file for the scenario at hand:

| Scenario | Reference | Typical Flow |
|----------|-----------|-------------|
| Customer Demo | `references/workflow-customer-demo.md` | Research → Diagrams → Narrative deck |
| Tech Sharing | `references/workflow-tech-sharing.md` | Outline → Code visuals → HTML/PPTX |
| Workshop | `references/workflow-workshop.md` | Steps → Code + diagrams → HTML slides |
| Architecture Review | `references/workflow-architecture-review.md` | As-is diagram → Gap analysis → Deck |
| Template Fill | `references/workflow-template-fill.md` | Analyze template → Map → Fill → Verify |

For orchestration patterns and MCP integration details, read `references/orchestration-and-mcp.md`.
For task plan and style contract templates, read `references/templates.md`.

## Slide Design System (Modular Templates)

The slide design system defines a **light/elegant multi-template approach** (淡雅清新多模版体系).

**MANDATORY**: When creating slides via html2pptx, follow the design system and choose the appropriate template per slide based on content semantics.

| Resource | Path | Purpose |
|----------|------|---------|
| **Design System** (global rules) | `references/slide-design-system.md` | Page basics, colors, fonts, prohibited styles, chart specs, html2pptx height rules |
| **Template Index** | `references/slide-templates/README.md` | Decision table for selecting templates, how to add new templates |
| **Shared Components** | `references/slide-templates/_shared.md` | Common elements: title area, cards, badges, bottom bar, extension area |
| **Template A** (Comparison) | `references/slide-templates/template-A-comparison.md` | Before/After, paradigm shifts |
| **Template B** (Architecture) | `references/slide-templates/template-B-architecture.md` | System architecture, feature modules |
| **Template C** (Timeline) | `references/slide-templates/template-C-timeline.md` | Milestones, evolution |
| **Template D** (Numbered Grid) | `references/slide-templates/template-D-numbered-grid.md` | Best practices, 3-6 key points |
| **Template E** (Text + Diagram) | `references/slide-templates/template-E-text-diagram.md` | Concept explanation with chart/diagram |
| **Template F** (Multi-Column) | `references/slide-templates/template-F-multi-column.md` | Feature showcase, equal-weight categories |

**Key design rules** (enforced by `scripts/check-slide-html.sh` hook):
- Page background: pure white `#ffffff`
- Title: left-aligned, dark `#1a1a2e`, no colored background bar
- Card backgrounds: `#f0f2f5` (light gray)
- **Prohibited**: full-width dark bars (`#4472C4`/`#2F5496` at `width:960pt`)
- Accent color (orange `#E8913A`) for badges, icons, borders only — area < 15%
- Every slide must include at least one visualization (chart/diagram/flow)
- Content coverage >= 95% of page area

**Hook enforcement**: Copy `hooks-settings.json` to `.claude/settings.json` in the project to enable automatic HTML rule checking on Write/Edit.

**Memory files**: `memory/` contains persistent design preferences — copy relevant files to the project's memory directory.

## Sub-Skill Locations

> ⛔ **PREREQUISITE**: Do NOT read or invoke any sub-skill until Steps 0–3 of the
> workflow are complete and workspace files exist on disk.

These paths are relative to the skill directory (where this SKILL.md lives):

| Skill | Path | When to Read |
|-------|------|-------------|
| azure-diagrams | `../azure-diagrams/SKILL.md` | Need any cloud/architecture diagram (supports Azure, AWS, GCP icons) |
| excalidraw-diagram | `../excalidraw-diagram/SKILL.md` | Need hand-drawn style diagrams |
| frontend-slides | `../frontend-slides/SKILL.md` | Creating HTML presentations |
| pptx | `../pptx/SKILL.md` | Complex .pptx creation/editing |
| skywork-ppt | `../skywork-ppt/SKILL.md` | Slide local operations (info/delete/reorder/extract/merge) or template fill |

**Read the relevant sub-skill's SKILL.md before using it.** Each has specific patterns,
scripts, and constraints that matter for quality output.

## Sub-Agents

> ⛔ **PREREQUISITE**: Do NOT spawn any sub-agent until workspace files (task_plan.md,
> style_contract.md, findings.md) exist on disk. Agents READ these files as input.

The `agents/` directory contains instructions for specialized sub-agents. Read the
relevant agent file before spawning it. All agents use `workspace_path` as their
primary input parameter pointing to `outputs/{project-name}/`.

| Agent | File | When to Spawn |
|-------|------|--------------|
| **Research Agent** | `agents/research-agent.md` | Phase 1 — gather cloud service docs, features, case studies |
| **Diagram Agent** | `agents/diagram-agent.md` | Phase 2 — generate architecture diagrams and visuals |
| **Slide Builder Agent** | `agents/slide-builder-agent.md` | Phase 3 — build individual slides (parallelizable) |
| **Assembly Agent** | `agents/assembly-agent.md` | Phase 4 — merge slides + diagrams into final deck |
| **Review Agent** | `agents/review-agent.md` | Phase 5 — quality review (max 2 rounds; skipped for <5 slides where orchestrator self-checks) |
| **Fix Agent** | `agents/fix-agent.md` | Phase 5 — apply fixes from review report |

**Agent interaction flow (file-based):**
```
Phase 0: Orchestrator
  WRITES → task_plan.md, style_contract.md, progress.md

Phase 1: Research Agent
  READS  ← task_plan.md
  WRITES → findings.md

Phase 2: Diagram Agent
  READS  ← task_plan.md, style_contract.md
  WRITES → diagrams/*.png, diagrams/manifest.md

Phase 3: Slide Builder Agent(s)  [parallelizable]
  READS  ← style_contract.md, findings.md, diagrams/
  WRITES → slides/slide-{N}.{pptx|html}, slides/slide-{N}-notes.md, slides/manifest.md
  FORMAT CHOICE: .pptx (simple/English) or .html (complex/Chinese/code) per slide

Phase 4: Assembly Agent
  READS  ← task_plan.md, slides/, diagrams/
  WRITES → final/final-deck.{pptx|html}, final/assembly-report.md

Phase 5: Review Agent (Round 1)
  READS  ← style_contract.md, final/final-deck.*
  WRITES → final/review_report.md

Phase 5: Fix Agent
  READS  ← final/review_report.md, style_contract.md, final/final-deck.*
  WRITES → final/final-deck.* (updated), final/fix_summary.md

Phase 5: Review Agent (Round 2)
  READS  ← style_contract.md, final/final-deck.*, final/review_report.md
  WRITES → final/review_report.md (updated)
```

## ⚠️ MANDATORY: Visual Validation (最终交付门禁)

**最高优先级规则：内容完整显示 + 合理布局 > 字体大小**

- 所有文本必须完整可见，不允许截断或溢出（**硬约束**）
- 文本尽量不换行；如果换行后最后一行内容 < 20%（widow line），必须修复（**硬约束**）
- 字体大小尽量 >= 10pt，但为满足上述两条可缩至任意合理大小（**软约束**）
- **完整可见 > 合理布局 > 字体大小** — 字体大小永远让步于内容完整显示

**Every .pptx output MUST pass visual validation before delivery — no exceptions.**

After ANY generation, editing, or structural modification that produces a `.pptx`:

```bash
$PYTHON_CMD -m pip install -q python-pptx Pillow

# 验证脚本位于 csa-skills 插件根目录:
CSA_SCRIPTS="$HOME/.claude/plugins/marketplaces/csa-skills/scripts"

$PYTHON_CMD "$CSA_SCRIPTS/validate_visual.py" /path/to/output.pptx --output /tmp/ppt_validation.json
```

If validation FAILS (exit code 1):

```bash
$PYTHON_CMD "$CSA_SCRIPTS/fix_overflow.py" /path/to/output.pptx --report /tmp/ppt_validation.json -o /path/to/output.pptx
$PYTHON_CMD "$CSA_SCRIPTS/validate_visual.py" /path/to/output.pptx --output /tmp/ppt_validation.json
```

> **脚本位置**: `~/.claude/plugins/marketplaces/csa-skills/scripts/validate_visual.py`
> 这是插件根目录下的独立脚本，不依赖任何子 skill，任何触发 csa-skills 的场景都能调用。

**Do NOT deliver until validation passes.**

### 双重校验机制（算法 + LLM 视觉）

1. **算法校验**：`validate_visual.py` 检测溢出、widow line（自动化，速度快）
2. **LLM 视觉校验**：Agent 自身读取渲染后的 PNG 截图，确认内容完整可见、布局合理

**两者都通过才算通过。** 算法有盲区（PIL 与 PowerPoint 渲染差异），LLM 看截图能发现算法遗漏的问题。

**LLM 视觉校验流程（模型无关）**：

```bash
# 渲染新建/修改的页面为 PNG
$PYTHON_CMD "$CSA_SCRIPTS/render_slides.py" /path/to/output.pptx \
  --output-dir /tmp/slide_renders/ \
  --slides <页码>
```

然后 Agent 直接使用 Read 工具读取 `/tmp/slide_renders/slide-*.png` 图片，验证：
- 所有文本完整可见（无裁切截断）
- 无 widow line
- 布局合理（无重叠、无异常空白）

> **不绑定特定模型** — coding agent 本身就是多模态 LLM，直接用内置能力读图即可。
> 不需要额外 API 调用或硬编码模型名称。

Read `../skywork-ppt/workflow_validate.md` for the full loop.

Fix priority (applied in order):
1. Expand container（不影响字体，避免换行）
2. Widen shape（消除 widow line）
3. Reduce font size（无硬性下限，完整可见是硬约束）
4. Reduce spacing
5. Truncate（最后手段）

---

## Quality Checklist

Before delivering any presentation, verify:

- [ ] **Visual validation PASSED**: `validate_visual.py` exit code 0 (no text overflow, no widow lines)
- [ ] **Content accuracy**: Cloud service names, pricing tiers, and features are current (Azure, AWS, GCP — whichever the deck covers)
- [ ] **Visual consistency**: Diagrams use consistent colors and icon styles throughout
- [ ] **Language**: No mixed-language issues (don't accidentally leave English labels in a
      Chinese deck or vice versa)
- [ ] **Font rendering**: For .pptx with Chinese text, verify characters render correctly
- [ ] **Image resolution**: All embedded diagrams are crisp, not pixelated
- [ ] **Template compliance**: If using a provided template, verify master slides are intact
- [ ] **Narrative flow**: Slides tell a story, not just list features

## Tips for CSA Presentations

> For detailed tips, read `references/orchestration-and-mcp.md`

Key principles:
- Lead with the customer's problem, not cloud service features
- Use progressive disclosure in architecture diagrams
- Include decision rationale (why CosmosDB over SQL? why DynamoDB over RDS?)
- Reference Well-Architected Framework pillars when relevant (Azure WAF, AWS WAF, GCP Architecture Framework)
