# GPT-image-2 PPT Integration Guide

## Workflow in CSA-PPT Pipeline

```
csa-ppt orchestrator
    ├── Phase 1: Research → findings.md
    ├── Phase 2: Diagrams → diagram-agent
    │   ├── azure-diagrams     (architecture, ERD, swimlane)
    │   ├── excalidraw-diagram (hand-drawn, conceptual)
    │   └── gpt-image          (photorealistic, scenarios, covers)  ← NEW
    ├── Phase 3: Slides → slide-builder-agent
    ├── Phase 4: Assembly
    └── Phase 5: Review
```

## Image Sizing for Slide Layouts

### Template A: Comparison (左右对比)
- **场景图**: `1024x1024` per side, showing before/after
- **放置**: Left card and right card each get one image

### Template B: Architecture (系统架构)
- **架构图**: Use azure-diagrams, NOT gpt-image
- **装饰背景**: `1920x1080` subtle background under the architecture area
- **场景配图**: `512x512` small scenario icon in corner

### Template C: Timeline (时间线)
- **里程碑图**: `512x512` per milestone, illustrating each phase
- **时间线背景**: `1920x320` wide banner strip along the timeline

### Template D: Numbered Grid (要点网格)
- **卡片插图**: `512x512` per card, 3-6 small illustrations
- **使用 transparent background** so cards' `#f0f2f5` background shows through

### Template E: Text + Diagram (文图结合)
- **右侧大图**: `1024x1024` or `1536x1024` on the right panel
- **占页面 55-62%** 的宽度

### Template F: Multi-Column (多列等权)
- **列头图**: `512x512` per column header
- **使用一致风格** — generate all column images in one session with similar prompts

## Embedding in html2pptx Slides

```html
<!-- In the slide HTML, reference the generated PNG -->
<div class="main-content" style="position: absolute; top: 66pt; left: 18pt; width: 924pt; height: 380pt;">
    <div style="display: flex;">
        <!-- Left: text content (38%) -->
        <div style="width: 38%; padding-right: 16pt;">
            <h3>方案概述</h3>
            <ul>...</ul>
        </div>
        <!-- Right: generated image (62%) -->
        <div style="width: 62%;">
            <img src="diagrams/scenario-image.png" 
                 style="width: 100%; height: auto; border-radius: 8px;" />
        </div>
    </div>
</div>
```

## Embedding in PptxGenJS Slides

```javascript
// Reference the generated PNG in PptxGenJS
slide.addImage({
    path: 'outputs/project/diagrams/scenario-image.png',
    x: 5.0,    // inches from left
    y: 1.2,    // inches from top
    w: 7.5,    // width in inches
    h: 5.0,    // height in inches
    rounding: true,  // optional rounded corners
});
```

## Best Practices

### DO
- Generate images at **1536x1024** or larger for crisp rendering on slides
- Use **transparent backgrounds** for images that overlay colored card backgrounds
- **Match the PPT color palette** — mention `#E8913A` orange and `#4472C4` blue in prompts
- Save to `{workspace}/diagrams/` alongside azure-diagrams and excalidraw outputs
- Update `diagrams/manifest.md` with every new image
- Verify image dimensions before embedding

### DON'T
- Don't use gpt-image for architecture diagrams — that's azure-diagrams' job
- Don't generate text-heavy images — use slide text overlays instead
- Don't generate more than 2-3 images per slide — keep it clean
- Don't use `quality="low"` for final output — only for drafts
- Don't embed enormous (>5MB) images without compression

## Common Combinations

| Slide Type | azure-diagrams | excalidraw | gpt-image |
|-----------|----------------|------------|-----------|
| Title/Cover | — | — | Hero concept art |
| Architecture Overview | Main architecture diagram | — | Background texture |
| Industry Solution | Service topology | — | Scenario photography |
| Best Practices | — | Concept flow | Card illustrations |
| Summary/CTA | — | — | Inspiring closing visual |
| Comparison | — | — | Before/after imagery |
| Timeline | — | — | Milestone illustrations |
