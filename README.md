# CSA PPT Plugin

All-in-one presentation toolkit for **Cloud Solution Architects** (Azure / AWS / GCP).

Works with **Claude Code**, **Cursor**, **GitHub Copilot CLI**, **OpenAI Codex CLI**, **Windsurf**, and **OpenCode**.

## What's Inside

### Skills (1 orchestrator + 6 sub-skills + 1 utility)

| Skill | Description |
|-------|-------------|
| **csa-ppt** | Smart orchestrator — analyzes your request and routes to the best tool chain |
| **azure-diagrams** | 700+ cloud icons (Azure/AWS/GCP), architecture diagrams, swimlane flows, ERDs, timelines |
| **excalidraw-diagram** | Hand-drawn style diagrams for brainstorming and conceptual visuals |
| **gpt-image** | AI image generation (Azure OpenAI GPT-image-2) — photorealistic illustrations, concept art, hero backgrounds |
| **frontend-slides** | Zero-dependency HTML presentations, great for Chinese content and code |
| **pptx** | Full OOXML-level PowerPoint creation and editing |
| **skywork-ppt** | Quick PowerPoint generation, template-based creation, and slide operations |
| **planning-with-files** | Task planning with file-based progress tracking for multi-slide decks |

### Sub-Agents (6 agents)

The orchestrator **按需调度** sub-agents — not every agent is used every time. The orchestrator
decides based on deck size and complexity:

| Agent | Phase | Role | When Dispatched |
|-------|-------|------|-----------------|
| **Research Agent** | Phase 1 | Gathers cloud docs (Azure/AWS/GCP), features, case studies, industry context | Topics need web research |
| **Diagram Agent** | Phase 2 | Generates architecture diagrams and technical visuals | Deck includes architecture diagrams |
| **Slide Builder Agent** | Phase 3 | Builds individual slides, smart format selection per slide (parallelizable) | Large decks (10+ slides) |
| **Assembly Agent** | Phase 4 | Normalizes mixed formats + merges slides + diagrams into final deck | Multiple builders produced separate files |
| **Review Agent** | Phase 5 | Quality review across 7 dimensions, max 2 rounds | Always for 5+ slide decks |
| **Fix Agent** | Phase 5 | Applies targeted fixes from the review report | Review found issues |

**Dispatch strategy by deck size:**

| Deck Size | Orchestrator Does | Sub-Agents Handle |
|-----------|-------------------|-------------------|
| Small (< 5 slides) | Everything directly, quick self-check | — |
| Medium (5–10 slides) | Phase 1, 2, 4 | Slide Builder (Phase 3), Review + Fix (Phase 5) |
| Large (10+ slides) | Coordination only | All 6 agents, Slide Builders run in parallel |

### Workflow

```
Plan → Style Contract → Research → Diagrams → Slides → Assembly → Review → Fix → Deliver
                         Phase 1    Phase 2    Phase 3   Phase 4    Phase 5
```

Each presentation follows a **5-phase workflow**:

1. **Plan** — Break the deck into tasks (one per slide/chapter)
2. **Define Style** — Lock colors, fonts, layout rules into a Style Contract
3. **Execute** — Research + diagrams + slides (parallel where possible)
4. **Assemble** — Normalize mixed intermediate formats + combine into final .pptx or HTML
5. **Review & Fix** — Independent quality check + fix loop (max 2 rounds)

---

## Diagram & Image Skill Routing (图表/图片技能路由规则)

本插件包含 **4 种可视化生成能力**，按「结构化 → 写实/艺术」光谱排列，各司其职、互不重叠：

```
        结构化 ◄─────────────────────────────────► 写实/艺术

  PptxGenJS        azure-diagrams      excalidraw-diagram      gpt-image
  (数据图表)         (架构图)             (概念手绘)            (写实插画/场景)
      ▲                  ▲                   ▲                      ▲
   纯数据             技术架构            思维概念              视觉表达/氛围
```

### 快速决策树

```
需要什么类型的图？
├── 数值对比 / 趋势 / 占比  ──────► pptx（PptxGenJS 内置柱状图/饼图/折线图）
├── 云服务架构 (Azure/AWS/GCP) ──► azure-diagrams（700+ 官方图标）
├── 泳道流程 / 业务流程 ─────────► azure-diagrams（Graphviz 泳道）
├── 序列图 / 认证流程 ──────────► azure-diagrams（序列图模式）
├── ERD / 数据模型 ─────────────► azure-diagrams（ER 图）
├── 时间线 / 里程碑 ────────────► azure-diagrams（Timeline/Gantt）
├── 手绘 / 白板 / 概念草图 ────► excalidraw-diagram（手绘美学）
└── 以下场景用 gpt-image ──────►
    ├── 封面/标题页概念插画
    ├── 行业场景写实图（零售、工厂、医院、智慧城市）
    ├── 抽象概念可视化（零信任、云原生隐喻）
    ├── 产品 UI 概念图
    ├── 幻灯片背景/Hero 图
    └── 多语言信息图
```

### 能力对比矩阵

| 能力 | PptxGenJS | azure-diagrams | excalidraw-diagram | gpt-image |
|------|:---------:|:--------------:|:------------------:|:---------:|
| 柱状图/饼图/折线图 | **最佳** | — | — | — |
| 云架构图 (Azure/AWS/GCP) | — | **最佳** (700+ 图标) | — | — |
| 泳道/流程图 | — | **最佳** | 可用 | — |
| 手绘/白板风格 | — | — | **最佳** | — |
| ERD / 数据模型 | — | **最佳** | — | — |
| 时间线 / 甘特图 | — | **最佳** | 可用 | — |
| 写实场景插画 | — | — | — | **独有** |
| 概念艺术/封面图 | — | — | — | **独有** |
| 行业场景图像 | — | — | — | **独有** |
| 多语言嵌入文字图 | — | — | — | **独有** |
| 产品 UI 概念图 | — | — | — | **独有** |
| 幻灯片背景/Hero | CSS only | — | — | **独有** |

### 各 Skill 详细说明

#### azure-diagrams — 技术架构图

| 图表类型 | 参考文件 | 示例调用 |
|----------|----------|----------|
| Azure 架构图 | `references/azure-components.md` | "Design a microservices architecture with AKS and Cosmos DB" |
| 业务流程图 (泳道) | `references/business-process-flows.md` | "Create a swimlane for invoice approval workflow" |
| ER 图 (数据模型) | `references/entity-relationship-diagrams.md` | "Generate an ERD for customer and order entities" |
| 时间线 / 甘特图 | `references/timeline-gantt-diagrams.md` | "Create a 6-month migration roadmap" |
| UI 线框图 | `references/ui-wireframe-diagrams.md` | "Design a KPI dashboard layout" |
| 通用模式 (Hub-Spoke 等) | `references/common-patterns.md` | "Show a hub-spoke network topology" |

**支持 IaC 逆向生成**：读取 Bicep / Terraform / ARM Template / Azure Pipelines YAML / GitHub Actions 文件，自动生成架构图。

**强制规则**：PPT 中包含云架构内容（Azure/AWS/GCP 服务拓扑、网络架构、数据管线等）时，**必须**使用 azure-diagrams 生成 PNG，禁止用内联 SVG/matplotlib 替代。

#### excalidraw-diagram — 手绘概念图

适用于需要白板/手绘美学的场景。输出 `.excalidraw` JSON + 渲染 PNG，可嵌入 PPT。

| 视觉模式 | 适用场景 |
|----------|----------|
| Fan-Out (一对多) | 来源、PRD、根因分析、中心枢纽 |
| Convergence (多对一) | 聚合、漏斗、综合 |
| Tree (层级) | 文件系统、组织架构、分类 |
| Spiral/Cycle (循环) | 反馈闭环、迭代过程、演进 |
| Assembly Line (转换) | 输入→处理→输出的转换链 |
| Side-by-Side (对比) | Before/After、方案对比 |
| Timeline (时间线) | 线 + 点 + 标签的时间序列 |

**强制规则**：用户明确要求手绘（手绘/草图/whiteboard/sketch）风格时，**必须**使用 excalidraw-diagram。

#### gpt-image — AI 写实插画

基于 Azure OpenAI GPT-image-2 模型，生成照片级插画、概念艺术、场景图像。

| 用途 | 示例 | 为什么用 gpt-image |
|------|------|-------------------|
| 封面/标题页 | "AI赋能数字化转型" 概念插画 | 其他工具无法创建写实概念图 |
| 行业场景 | 零售店、工厂车间、医院、智慧城市 | 方案演示需要场景化视觉 |
| 抽象概念 | "零信任安全" 隐喻图、"云原生" 插画 | 超越方框箭头的视觉叙事 |
| 产品 UI 概念 | 仪表盘预览、App 概念图 | 比 excalidraw 手绘更写实 |
| Hero 背景 | 带科技元素的渐变网格背景 | CSS 渐变太平，AI 创造景深 |
| 自定义图标 | 品牌概念图标（Azure 图标库没有的） | 填补标准图标库空白 |
| 多语言信息图 | 嵌入中英文文字的图像 | 原生 CJK 文字渲染支持 |

**不要用 gpt-image 的场景**：云架构图 → azure-diagrams | 手绘风格 → excalidraw-diagram | 数据图表 → pptx

### 编排器路由优先级

csa-ppt 编排器按以下优先级自动路由：

| 优先级 | 规则 | 说明 |
|--------|------|------|
| **P0** | 强制组合路由 | 云架构 PPT → azure-diagrams → pptx；手绘概念 PPT → excalidraw → pptx；写实插画 → gpt-image → pptx |
| **P1** | 内容类型 | 架构图 → azure-diagrams；手绘 → excalidraw；写实 → gpt-image；数据图表 → pptx |
| **P2** | 交付格式 | 客户正式 → pptx(html2pptx)；内部/Demo → frontend-slides 或 pptx；模板填充 → skywork-ppt |
| **P3** | 语言 | 中文为主 → 偏好 HTML 中间格式；英文/混合 → 任意 |
| **P4** | 模板处理 | 简单填充 → skywork-ppt；复杂排版 → pptx OOXML |

**自动检测脚本**：
- `azure-diagrams/scripts/detect_cloud_arch.py` — 分析幻灯片大纲，自动识别需要架构图的页面
- `excalidraw-diagram/scripts/detect_excalidraw.py` — 检测需要手绘风格的页面 + 验证输出

---

## Slide Design System (淡雅清新多模版体系)

Plugin 内置一套**淡雅清新多模版设计体系**，作为所有 PPT 生成的默认样式。

### 设计理念

> 白色背景、左上角深色标题、浅灰卡片、橙色点缀，禁止全幅深色横条。

### 6 套模版

每个模版是独立文件，新增模版只需添加一个文件：

| 模版 | 名称 | 适用场景 | 文件 |
|------|------|----------|------|
| **A** | 对比/Before-After | 新旧对比、范式迁移 | [`template-A-comparison.md`](skills/csa-ppt/references/slide-templates/template-A-comparison.md) |
| **B** | 架构/特性展示 | 系统架构、功能模块 | [`template-B-architecture.md`](skills/csa-ppt/references/slide-templates/template-B-architecture.md) |
| **C** | 时间线/里程碑 | 时间演进、发展阶段 | [`template-C-timeline.md`](skills/csa-ppt/references/slide-templates/template-C-timeline.md) |
| **D** | 编号网格 | 最佳实践、3-6 个要点 | [`template-D-numbered-grid.md`](skills/csa-ppt/references/slide-templates/template-D-numbered-grid.md) |
| **E** | 左文右图 | 概念说明+图表配合 | [`template-E-text-diagram.md`](skills/csa-ppt/references/slide-templates/template-E-text-diagram.md) |
| **F** | 多列等宽卡片 | 功能展示、等权分类 | [`template-F-multi-column.md`](skills/csa-ppt/references/slide-templates/template-F-multi-column.md) |

辅助文件：
- [`_shared.md`](skills/csa-ppt/references/slide-templates/_shared.md) — 通用组件规范（标题区、卡片、徽章、底部栏等）
- [`README.md`](skills/csa-ppt/references/slide-templates/README.md) — 模版索引 + 选择决策表 + 扩展说明
- [`slide-design-system.md`](skills/csa-ppt/references/slide-design-system.md) — 全局设计规范（配色、字体、禁止样式、html2pptx 规则）

### 配色方案

| 用途 | 色值 | 示例 |
|------|------|------|
| 主强调色（橙） | `#E8913A` | 序号徽章、图标、左竖线 |
| 辅助色（蓝） | `#4472C4` | 图表系列、链接 |
| 成功/绿 | `#70AD47` | 正面指标 |
| 标题色 | `#1a1a2e` | 页面主标题 |
| 卡片背景 | `#f0f2f5` | 内容卡片底色 |
| 底部栏 | `#f5f5f7` | 洞察/摘要栏 |

### 禁止样式

- 全幅深色标题栏（`#4472C4` / `#2F5496` 全宽）
- 全幅深色底部栏
- 大面积深色色块 > 15%
- 标题居中在蓝色背景内

### 添加新模版

1. 在 `skills/csa-ppt/references/slide-templates/` 下新建 `template-G-xxx.md`
2. 按统一格式编写：适用场景 → 布局骨架(ASCII) → 区域说明 → 高度预算 → HTML 参考
3. 在 `README.md` 决策表中新增一行
4. 在 `slide-design-system.md` §4 模版选择表中新增一行

---

## Hook 强制规则

Plugin 提供 `scripts/check-slide-html.sh` 脚本，可作为 **PostToolUse hook** 自动检查 slide HTML 违规：

### 检查规则

| 规则 | 说明 |
|------|------|
| 禁止全幅深色横条 | `width:960pt` 元素不得使用 `background:#4472C4` 或 `#2F5496` |
| 尺寸匹配 | 有 `width:960pt` 时必须同时有 `height:540pt` |
| 禁止蓝色标题栏 | `.title-bar` 类不得同时使用全幅 + 深色背景 |

### 启用方式

将 [`hooks-settings.json`](skills/csa-ppt/hooks-settings.json) 的内容复制到项目的 `.claude/settings.json`，并替换 `PLUGIN_PATH` 为实际路径：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [{
          "type": "command",
          "command": "bash /path/to/scripts/check-slide-html.sh \"$CLAUDE_FILE_PATH\""
        }]
      },
      {
        "matcher": "Edit",
        "hooks": [{
          "type": "command",
          "command": "bash /path/to/scripts/check-slide-html.sh \"$CLAUDE_FILE_PATH\""
        }]
      }
    ]
  }
}
```

Hook 仅对 `slide*.html` 文件生效，其他文件自动跳过。

---

## Memory（设计偏好记忆）

`skills/csa-ppt/memory/` 包含持久化的设计偏好文件，可复制到项目的 memory 目录：

| 文件 | 内容 |
|------|------|
| `feedback_ppt_light_theme.md` | 淡雅多模版体系规则，禁止深色横条 |
| `feedback_ppt_charts_required.md` | 每页必须含图表，左文右图布局 |
| `feedback_ppt_sizing.md` | 95%+ 覆盖率规则，高度预算方法 |

---

## Multi-Platform Instructions

每个 AI 编码工具会自动读取对应的指令文件，获得默认的 PPT 设计规范：

| 平台 | 指令文件 | 自动加载 |
|------|----------|----------|
| Claude Code | `CLAUDE.md` | Yes |
| GitHub Copilot | `.github/copilot-instructions.md` | Yes |
| Cursor | `.cursorrules` | Yes |
| OpenAI Codex | `AGENTS.md` | Yes |
| Windsurf | `.windsurfrules` | Yes |
| OpenCode | `opencode.json` | Yes |

---

## Smart Intermediate Format Selection

Slide Builder Agents **choose the best intermediate format per-slide** based on content — not
forced to match the final output format:

| Content | Intermediate Format | Why |
|---------|-------------------|-----|
| Simple bullets, English content | `.pptx` (python-pptx) | Direct, no conversion overhead |
| Diagram-only slides | `.pptx` (python-pptx) | Simple image embed |
| Chinese-heavy (中文为主) | `.html` | Better CJK font rendering |
| Code blocks with syntax highlighting | `.html` | Native code rendering |
| Complex multi-column layouts | `.html` | CSS flexbox/grid flexibility |

The Assembly Agent handles the format mix — normalizing all slides to the target format
before merging into the final deck.

## Supported Scenarios

- **Customer Solution Demos** — Architecture diagrams + polished .pptx decks
- **Internal Tech Sharing** — HTML slides with code syntax highlighting
- **Workshops / Hands-on Labs** — Step-by-step interactive presentations
- **Architecture Reviews (CAF/WAF/Well-Architected)** — Assessment decks with as-is/to-be diagrams
- **Template Filling** — Fill company/event templates while preserving branding

## Installation

### Claude Code (Primary)

```bash
# Via marketplace (recommended)
/plugin marketplace add huqianghui/csa-ppt-plugin
/plugin install csa-ppt@csa-skills

# Or load directly for testing
claude --plugin-dir /path/to/csa-ppt-plugin
```

### Cursor

Clone to your project and Cursor auto-discovers `.cursor-plugin/plugin.json`:
```bash
git clone https://github.com/huqianghui/csa-ppt-plugin.git .cursor-plugins/csa-ppt
```
Or add individual skill paths in **Cursor Settings > Skills**.

### GitHub Copilot CLI

```bash
# Install from GitHub
copilot plugin install huqianghui/csa-ppt-plugin

# Or clone to project — Copilot reads .github/plugin/plugin.json
git clone https://github.com/huqianghui/csa-ppt-plugin.git
```

### OpenAI Codex CLI

```bash
# Symlink skills into Codex discovery path
ln -s /path/to/csa-ppt-plugin/skills ~/.codex/skills

# Or add to ~/.codex/config.toml
# [[skills.config]]
# path = "/path/to/csa-ppt-plugin/skills/csa-ppt"
```

### Windsurf

```bash
# Symlink to global skills
ln -s /path/to/csa-ppt-plugin/skills ~/.codeium/windsurf/skills

# Or clone to project — Windsurf reads .agents/skills/ automatically
```

### OpenCode

Clone to project root. OpenCode reads `opencode.json` automatically:
```bash
git clone https://github.com/huqianghui/csa-ppt-plugin.git
```

### Verify Installation (All Platforms)

```bash
bash scripts/install.sh
```

## Usage

Just describe what you need in natural language:

- "帮我做一个给客户演示Azure RAG方案的PPT"
- "Create an AWS to Azure migration comparison deck in English"
- "做一个内部AKS迁移到ACA的技术分享，中文，HTML格式"
- "用这个模板帮我填写季度工作汇报"
- "画一个Azure Landing Zone的架构图"

The **csa-ppt** skill will automatically:
1. Analyze your request (content type, language, format)
2. Initialize a file-based workspace (`outputs/{project}/`)
3. Choose the best tool chain and intermediate format per slide
4. Dispatch sub-agents as needed based on deck size
5. Assemble, normalizing any mixed intermediate formats
6. Review the assembled deck for quality and apply fixes

### Workspace — Intermediate Outputs You Can Inspect

Every presentation creates a workspace folder under `outputs/`. All intermediate files are
written to disk so you can **review, edit, or adjust** them at any point before the final
deck is assembled.

```
outputs/{project}/
├── task_plan.md              ← Slide plan with checkboxes — edit to reorder/add/remove slides
├── progress.md               ← Session log — see what's been done and what's next
├── style_contract.md         ← Colors, fonts, layout rules — edit to change the look
├── findings.md               ← Research results — review before slides are built
├── diagrams/
│   ├── manifest.md           ← List of generated diagrams
│   ├── rag-architecture.png  ← Architecture diagram — open to preview
│   └── data-pipeline.png     ← Flow diagram — replace with your own if needed
├── slides/
│   ├── manifest.md           ← Per-slide format (pptx/html) and status
│   ├── slide-1.pptx          ← Individual slide — open in PowerPoint to check
│   ├── slide-1-notes.md      ← Speaker notes — edit to refine talking points
│   ├── slide-2.html          ← HTML slide — open in browser to preview
│   └── ...
└── final/
    ├── final-deck.pptx       ← Assembled deck — the deliverable
    ├── assembly-report.md    ← What was merged, format conversions applied
    ├── review_report.md      ← Quality review results (per-slide PASS/FIX)
    └── fix_summary.md        ← What was fixed after review
```

**How to use this during creation:**

- **Adjust the plan** — Edit `task_plan.md` to add/remove/reorder slides before Phase 3
- **Change the style** — Edit `style_contract.md` to change colors or fonts before slides are built
- **Review research** — Read `findings.md` to verify the content before it goes into slides
- **Preview individual slides** — Open `.pptx` files in PowerPoint or `.html` files in a browser
- **Replace diagrams** — Drop your own `.png` files into `diagrams/` and update `manifest.md`
- **Edit speaker notes** — Modify any `slide-{N}-notes.md` before assembly
- **Check review results** — Read `review_report.md` to see what the Review Agent flagged

All changes you make to intermediate files will be picked up by the next phase.

## Project Structure

```
csa-ppt-plugin/
├── CLAUDE.md                        # Claude Code 默认设计规范
├── AGENTS.md                        # Codex 默认设计规范
├── .cursorrules                     # Cursor 默认设计规范
├── .windsurfrules                   # Windsurf 默认设计规范
├── .claude-plugin/                  # Claude Code manifest
│   ├── plugin.json
│   └── marketplace.json
├── .cursor-plugin/                  # Cursor manifest
│   └── plugin.json
├── .github/
│   ├── plugin/plugin.json           # GitHub Copilot CLI manifest
│   └── copilot-instructions.md      # Copilot 默认设计规范
├── .codex/skills -> skills          # Codex CLI symlink
├── .agents/skills -> skills         # Cross-platform symlink
├── .windsurf/skills -> skills       # Windsurf symlink
├── .opencode/agents -> skills       # OpenCode symlink
├── opencode.json                    # OpenCode config
├── scripts/
│   ├── install.sh                   # Multi-platform installer & verifier
│   └── check-slide-html.sh         # Hook: slide HTML 规则检查
├── skills/
│   ├── csa-ppt/                     # Main orchestrator
│   │   ├── SKILL.md                 # Routing logic, workflow, Style Contract
│   │   ├── hooks-settings.json      # Hook 配置模版（复制到项目 .claude/settings.json）
│   │   ├── memory/                  # 持久化设计偏好
│   │   │   ├── MEMORY.md
│   │   │   ├── feedback_ppt_light_theme.md
│   │   │   ├── feedback_ppt_charts_required.md
│   │   │   └── feedback_ppt_sizing.md
│   │   ├── agents/                  # 6 specialized sub-agents
│   │   │   ├── research-agent.md
│   │   │   ├── diagram-agent.md
│   │   │   ├── slide-builder-agent.md
│   │   │   ├── assembly-agent.md
│   │   │   ├── review-agent.md
│   │   │   └── fix-agent.md
│   │   ├── references/
│   │   │   ├── slide-design-system.md       # 全局设计规范
│   │   │   ├── slide-templates/             # 模版目录
│   │   │   │   ├── README.md                # 模版索引 + 选择决策表
│   │   │   │   ├── _shared.md               # 通用组件规范
│   │   │   │   ├── template-A-comparison.md
│   │   │   │   ├── template-B-architecture.md
│   │   │   │   ├── template-C-timeline.md
│   │   │   │   ├── template-D-numbered-grid.md
│   │   │   │   ├── template-E-text-diagram.md
│   │   │   │   └── template-F-multi-column.md
│   │   │   ├── templates.md                 # Task plan / style contract templates
│   │   │   ├── orchestration-and-mcp.md
│   │   │   ├── workflow-customer-demo.md
│   │   │   ├── workflow-tech-sharing.md
│   │   │   ├── workflow-workshop.md
│   │   │   ├── workflow-architecture-review.md
│   │   │   └── workflow-template-fill.md
│   │   └── evals/
│   │       └── evals.json
│   ├── azure-diagrams/              # 700+ Azure icons, diagram scripts
│   ├── excalidraw-diagram/          # Hand-drawn style diagrams
│   ├── gpt-image/                   # AI photorealistic image generation (GPT-image-2)
│   ├── frontend-slides/             # HTML presentations
│   ├── pptx/                        # OOXML PowerPoint creation
│   ├── skywork-ppt/                 # Quick PPT generation
│   └── planning-with-files/         # Task planning system
└── README.md
```

## Prerequisites

- Python 3.8+ with `python-pptx` (for skywork-ppt and azure-diagrams)
- Node.js (for pptx html2pptx conversion)
- `graphviz` system package (for azure-diagrams)
- `diagrams` and `matplotlib` Python libraries (for azure-diagrams)

## License

MIT
