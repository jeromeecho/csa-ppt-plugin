# GPT-image Skill

AI image generation for CSA presentations, powered by Azure OpenAI GPT-image-2.

## Why GPT-image-2?

### Tool Ecosystem Positioning

```
                    结构化 ←————————————————→ 写实/艺术
                    
  PptxGenJS    azure-diagrams    excalidraw    GPT-image-2
  (数据图表)    (架构图)          (概念手绘)     (写实插画/场景)
      ↑              ↑               ↑              ↑
   纯数据         技术架构        思维概念      视觉表达/氛围
```

**不重叠、纯增量** — GPT-image-2 填补的是"视觉表达层"，现有工具覆盖的是"信息结构层"。

### Detailed Comparison

| Capability | PptxGenJS | azure-diagrams | excalidraw | **GPT-image-2** |
|-----------|-----------|----------------|------------|-----------------|
| 数据图表 (柱/饼/折线) | **Best** | - | - | - |
| 云架构图 (Azure/AWS/GCP) | - | **Best** (700+ icons) | - | - |
| 泳道/流程图 | - | **Best** | Good | - |
| 手绘/白板风格 | - | - | **Best** | - |
| **写实场景插画** | - | - | - | **Unique** |
| **概念艺术/封面图** | - | - | - | **Unique** |
| **行业场景图** | - | - | - | **Unique** |
| **多语言文字嵌入图片** | - | - | - | **Unique** |
| **产品UI概念图** | - | - | - | **Unique** |
| **背景/Hero图** | CSS only | - | - | **Unique** |
| ERD/数据模型 | - | **Best** | - | - |
| 时间线/甘特图 | - | **Best** | Good | - |

### GPT-image-2 Unique Advantages

1. **写实概念插画** — 封面/过渡页需要"AI赋能数字化转型"这类抽象概念的视觉表达时，现有工具只能画框线图
2. **场景化配图** — "零售行业智能推荐方案"需要商场/仓库场景图，现有工具做不到
3. **多语言文字渲染** — 支持中/日/韩/英文字直接渲染进图片，适合信息图
4. **产品UI概念图** — 展示"最终用户体验"时，比excalidraw手绘风更接近真实产品
5. **高分辨率** — 支持到4K (3840x2160)，适合大屏/印刷
6. **图片编辑(Inpainting)** — 可以修改已有图片的局部，用于迭代优化

### Use Case Decision Tree

```
需要什么类型的图？
├── 数据对比/趋势 → PptxGenJS (内置图表)
├── 云服务架构 → azure-diagrams (官方图标)
├── 手绘/概念草图 → excalidraw-diagram
└── 以下情况用 GPT-image-2:
    ├── 封面/标题页概念艺术
    ├── 行业场景写实图
    ├── 抽象概念可视化
    ├── 产品UI预览
    ├── 幻灯片背景
    └── 带多语言文字的信息图
```

## Quick Start

### 1. Prerequisites

```bash
# Set environment variables
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_API_KEY="your-key"
export GPT_IMAGE_DEPLOYMENT="gpt-image-2"

# Install dependencies
pip install requests pillow
```

### 2. Verify Setup

```bash
python3 scripts/generate_image.py verify
```

### 3. Generate an Image

```bash
python3 scripts/generate_image.py generate \
    --prompt "A modern smart city with IoT sensors and data streams" \
    --output outputs/test/cover.png \
    --size 1536x1024 \
    --quality high
```

### 4. Use Size Presets

```bash
python3 scripts/generate_image.py presets
# slide-full     1920x1080
# slide-right    1024x1024
# slide-wide     1536x1024
# slide-tall     1024x1536
# 4k             3840x2160
# banner         1920x640
# icon-large     512x512
```

## Integration with CSA-PPT Workflow

This skill is automatically routed by the `diagram-agent` in the `csa-ppt` orchestrator:

| Content Type | Routing |
|-------------|---------|
| Cloud architecture (Azure/AWS/GCP) | → azure-diagrams |
| Hand-drawn / whiteboard concepts | → excalidraw-diagram |
| Photorealistic / artistic visuals | → **gpt-image** |
| Data charts (bar/pie/line) | → pptx (PptxGenJS) |

Generated images are saved to `outputs/{project}/diagrams/` and referenced by the slide-builder-agent.

## Directory Structure

```
gpt-image/
├── SKILL.md                     ← Skill definition (read by Claude Code)
├── README.md                    ← This file
├── scripts/
│   └── generate_image.py        ← Image generation script (CLI + importable)
└── references/
    ├── prompt-templates.md      ← PPT-optimized prompt templates by use case
    └── ppt-integration.md       ← How to embed images in slides
```

## API Reference

### GPT-image-2 Key Specs

| Feature | Value |
|---------|-------|
| Max resolution | 3840px (4K) |
| Min pixel count | 655,360 |
| Max pixel count | 8,294,400 |
| Size constraint | Both edges multiples of 16px |
| Quality options | `low` / `medium` / `high` |
| Output formats | PNG, JPEG, WEBP |
| Transparent background | Supported (PNG only) |
| Images per request | 1-10 |
| Image editing | Inpainting + mask support |
| Text languages | EN, CN, JP, KR, HI, BN |
| Output type | Base64 (no URL option) |

### Pricing (Azure OpenAI)

| Token Type | Cost |
|-----------|------|
| Image Input | $8/1M tokens |
| Cached Image Input | $2/1M tokens |
| Image Output | $30/1M tokens |
| Text Input | $5/1M tokens |
| Text Output | $10/1M tokens |

## Changelog

### v1.0.0 (2026-04-23)
- Initial release
- Image generation via Azure OpenAI GPT-image-2
- Image editing (inpainting) support
- PPT-optimized size presets
- Prompt template library for 6 common slide use cases
- Integration guide for html2pptx and PptxGenJS workflows
