---
name: gpt-image
description: >
  AI image generation skill using Azure OpenAI GPT-image-2 model. Generates photorealistic
  illustrations, conceptual visuals, scene imagery, hero backgrounds, and custom icons for
  presentations. Use this skill when slides need visual storytelling beyond structural diagrams —
  cover art, industry scenario photos, abstract concept illustrations, product UI mockups,
  or decorative backgrounds. Complements azure-diagrams (architecture) and excalidraw-diagram
  (hand-drawn) by providing the "visual expression layer" that programmatic tools cannot produce.
  Supports Chinese/English/Japanese/Korean text rendering in images. Output: PNG files ready
  for embedding into slides via the pptx skill.
compatibility: Requires Python 3.8+, openai Python SDK, and Azure OpenAI GPT-image-2 deployment.
license: MIT
metadata:
  author: huqianghui
  version: "1.0.0"
---

# GPT-Image Generation Skill

Generate photorealistic and artistic images using Azure OpenAI GPT-image-2 for presentations.

## When to Use This Skill

| Use Case | Example | Why GPT-image-2 |
|----------|---------|-----------------|
| **Cover / Title slides** | "AI赋能数字化转型" concept art | No existing tool can create photorealistic concept illustrations |
| **Industry scenario imagery** | Retail store, factory floor, hospital, smart city | Scene-based visuals for solution demos |
| **Abstract concept visuals** | "Zero Trust Security" metaphor, "Cloud Native" illustration | Visual storytelling beyond boxes and arrows |
| **Product UI mockups** | Dashboard preview, mobile app concept | More realistic than excalidraw hand-drawn |
| **Hero backgrounds** | Gradient mesh with tech elements for slide backgrounds | CSS gradients are flat; AI creates depth |
| **Custom icons / logos** | Branded concept icons not in Azure icon library | Fills gaps in standard icon sets |
| **Multilingual infographics** | Images with embedded Chinese/English text | Native CJK text rendering support |

## When NOT to Use This Skill

| Scenario | Use Instead |
|----------|-------------|
| Cloud architecture diagrams (Azure/AWS/GCP) | **azure-diagrams** — has 700+ official icons |
| Hand-drawn / whiteboard style sketches | **excalidraw-diagram** — purpose-built for that aesthetic |
| Data charts (bar, pie, line) | **pptx** built-in PptxGenJS charts |
| Simple icons and gradient bars | **SVG + Sharp** rasterization |

## Execution Method

**Always execute inline** — do not create separate .py files:

```bash
python3 << 'EOF'
import os, base64, requests

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
api_key = os.environ["AZURE_OPENAI_API_KEY"]
deployment = os.environ.get("GPT_IMAGE_DEPLOYMENT", "gpt-image-2")
api_version = "2025-04-01-preview"

url = f"{endpoint}openai/deployments/{deployment}/images/generations?api-version={api_version}"

response = requests.post(url, headers={
    "Api-Key": api_key,
    "Content-Type": "application/json"
}, json={
    "prompt": "YOUR PROMPT HERE",
    "n": 1,
    "size": "1536x1024",
    "quality": "high",
    "output_format": "png"
}).json()

if "error" in response:
    print(f"ERROR: {response['error']}")
else:
    img_data = base64.b64decode(response["data"][0]["b64_json"])
    output_path = "outputs/{project}/diagrams/image-name.png"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(img_data)
    print(f"Image saved: {output_path} ({len(img_data)} bytes)")

EOF
```

## Prerequisites

### Configuration (Required)

**推荐方式：编辑 `config.json`**（在 skill 根目录 `gpt-image/config.json`）：

```json
{
  "azure_openai_endpoint": "https://your-resource.openai.azure.com/",
  "azure_openai_api_key": "your-api-key",
  "deployment_name": "gpt-image-2",
  "api_version": "2025-04-01-preview"
}
```

> 配置优先级：CLI 参数 > config.json > 环境变量

**备选方式：环境变量**（如果 config.json 未填写，会自动回退到环境变量）：

```bash
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_API_KEY="your-key"
export GPT_IMAGE_DEPLOYMENT="gpt-image-2"
```

### Python Dependencies

```bash
pip install requests pillow
```

### Verify Setup

```bash
# 查看当前配置来源
python3 scripts/generate_image.py config

# 完整验证（含 API 连通性测试）
python3 scripts/generate_image.py verify
```

## API Parameters

| Parameter | Values | Default | Notes |
|-----------|--------|---------|-------|
| `size` | See size table below | `1024x1024` | Both edges must be multiples of 16 |
| `quality` | `low`, `medium`, `high` | `high` | `low` = fast/cheap, `high` = best quality |
| `n` | 1-10 | 1 | Number of images per request |
| `output_format` | `png`, `jpeg`, `webp` | `png` | Use `png` for transparency support |
| `background` | `auto`, `transparent` | `auto` | Requires `png` format |
| `output_compression` | 0-100 | — | JPEG only |

### Recommended Sizes for PPT

| Use Case | Size | Aspect Ratio | Notes |
|----------|------|-------------|-------|
| **Full-width slide image** | `1536x1024` | 3:2 | Fits 16:9 slide well |
| **Right-panel diagram** | `1024x1024` | 1:1 | For 左文右图 layout |
| **Wide banner / hero** | `1920x1080` | 16:9 | Full slide background |
| **Tall sidebar** | `1024x1536` | 2:3 | Vertical illustration |
| **4K high-res** | `3840x2160` | 16:9 | For print or zoom |

> GPT-image-2 supports arbitrary resolutions: both edges must be multiples of 16px, long edge up to 3840px, pixel count 655,360–8,294,400.

## Prompt Engineering for PPT Images

### Core Principles

1. **Describe the visual scene, not the concept** — "A modern glass-walled data center with blue LED server racks and holographic dashboards floating in the air" is better than "cloud computing"
2. **Specify the style** — "corporate illustration style", "isometric 3D", "flat design with subtle gradients", "photorealistic"
3. **Include composition guidance** — "wide angle", "bird's eye view", "centered subject with blurred background"
4. **Match the PPT color palette** — mention colors explicitly: "predominantly white and light gray background with orange (#E8913A) accent elements"
5. **Request clean backgrounds** — for slide embedding: "clean white background" or "transparent background"

### Prompt Templates by Use Case

#### Cover / Title Slide Art
```
A [style] illustration of [concept], featuring [specific visual elements].
The scene uses a clean, modern aesthetic with a predominantly white/light
background. Key accent colors: warm orange and cool blue tones.
Corporate presentation quality, high detail, professional.
```

#### Industry Scenario
```
A photorealistic view of [industry setting], showing [specific activity].
Modern, well-lit environment. Shot from [angle]. Professional quality,
suitable for a business presentation. No text overlays.
```

#### Abstract Concept
```
An abstract [style] visualization representing [concept]. Use geometric
shapes, flowing lines, and a color palette of [colors]. Minimalist
composition with strong visual hierarchy. Clean background suitable
for slide overlay text.
```

#### Background / Hero Image
```
A subtle, abstract background pattern for a presentation slide.
Soft gradients blending [color1] to [color2] with [geometric/organic]
elements. Low contrast, suitable for overlaying dark text. Resolution:
1920x1080, corporate and modern feel.
```

### Text in Images (Multilingual)

GPT-image-2 supports rendering text in Chinese, English, Japanese, Korean, Hindi, Bengali:

```
Create an infographic with the title "数字化转型路线图" in bold Chinese text
at the top. Below it, show 4 stages with labels in Chinese...
```

> Tip: Keep embedded text short and large. Complex multi-paragraph text may render poorly.

## Integration with CSA-PPT Workflow

### File Output Convention

All generated images go to `{workspace_path}/diagrams/` with descriptive names:

```
outputs/{project}/diagrams/
├── cover-concept.png          ← Title slide illustration
├── retail-scenario.png        ← Industry scenario image
├── zero-trust-visual.png      ← Abstract concept art
├── hero-background.png        ← Slide background
└── manifest.md                ← Updated with new entries
```

### Manifest Entry Format

When adding to `diagrams/manifest.md`:

```markdown
| cover-concept.png | Concept Art | gpt-image-2 | 1536x1024 | AI digital transformation concept for title slide |
```

### Quality Verification

After generating each image:

1. **Check file exists and is non-empty**: `ls -la {path}`
2. **Verify dimensions**: `python3 -c "from PIL import Image; img=Image.open('{path}'); print(img.size)"`
3. **Visual check**: Use the Read tool to view the image (Claude Code supports image viewing)

### Retry Strategy

If generation fails:
1. **content_policy_violation**: Rephrase the prompt to be less specific about people/faces
2. **Rate limit (429)**: Wait 10 seconds, retry with `quality="medium"`
3. **Timeout**: Retry with smaller size or `quality="low"`
4. **Persistent failure**: Log to `progress.md` as `[ERROR]`, suggest using SVG+Sharp as fallback for simple visuals

## Image Editing (Advanced)

GPT-image-2 also supports editing existing images (inpainting):

```bash
python3 << 'EOF'
import os, base64, requests

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
api_key = os.environ["AZURE_OPENAI_API_KEY"]
deployment = os.environ.get("GPT_IMAGE_DEPLOYMENT", "gpt-image-2")
api_version = "2025-04-01-preview"

url = f"{endpoint}openai/deployments/{deployment}/images/edits?api-version={api_version}"

with open("source_image.png", "rb") as img_file:
    response = requests.post(url,
        headers={"Api-Key": api_key},
        data={
            "prompt": "Replace the background with a modern office setting",
            "n": 1,
            "size": "1024x1024",
            "quality": "high"
        },
        files={
            "image": ("source.png", img_file, "image/png"),
            # Optional mask for targeted editing:
            # "mask": ("mask.png", open("mask.png", "rb"), "image/png"),
        }
    ).json()

if "error" in response:
    print(f"ERROR: {response['error']}")
else:
    img_data = base64.b64decode(response["data"][0]["b64_json"])
    with open("edited_image.png", "wb") as f:
        f.write(img_data)
    print("Edited image saved")

EOF
```

Use cases for editing:
- **Background replacement**: Generate a concept image, then replace its background to match slide theme
- **Style transfer**: Edit an existing diagram to add artistic elements
- **Localization**: Replace English text in an image with Chinese text

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `DeploymentNotFound` | Wrong deployment name | Check `GPT_IMAGE_DEPLOYMENT` env var |
| `401 Unauthorized` | Invalid API key | Verify `AZURE_OPENAI_API_KEY` |
| `429 Too Many Requests` | Rate limit | Wait + retry with lower quality |
| `content_policy_violation` | Prompt blocked by content filter | Rephrase prompt, avoid specific faces/people |
| `InvalidPayload` | Bad parameters | Check size is multiple of 16, valid format |

## Guidelines

- **Always use `quality="high"`** for final presentation images. Use `"medium"` only for drafts/iteration.
- **Prefer `1536x1024`** as the default size for most PPT use cases (good balance of quality and speed).
- **Transparent backgrounds** (`background="transparent"`) are useful for overlaying on colored slide backgrounds.
- **Keep prompts detailed** — vague prompts produce generic results. Include style, composition, colors, mood.
- **Match the PPT color palette** — reference the CLAUDE.md color scheme (orange `#E8913A`, blue `#4472C4`, etc.) in prompts.
- **No text-heavy images** — GPT-image-2 handles short labels well but struggles with paragraphs. Use slide text overlays instead.
- **One image per prompt** — generate n=1 for quality control. Batch generation (n>1) gives varied results.
