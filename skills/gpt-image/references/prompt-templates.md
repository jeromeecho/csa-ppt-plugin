# GPT-image-2 Prompt Templates for PPT

## PPT Color Palette Reference

When writing prompts, reference these colors to match the slide design system:

- **Primary accent (orange)**: `#E8913A` — warm orange for emphasis
- **Secondary (blue)**: `#4472C4` — professional blue
- **Success (green)**: `#70AD47` — positive indicators
- **Background**: white/light gray — clean, minimal
- **Text**: dark navy `#1a1a2e` — contrast

---

## Template 1: Cover / Title Slide Art

**Use when**: Creating the opening slide's hero visual

```
Create a [style] illustration for a professional presentation cover slide.
The scene depicts [main concept/metaphor].

Visual elements:
- [Specific element 1]
- [Specific element 2]
- [Specific element 3]

Style: Modern corporate illustration, clean lines, subtle depth.
Color palette: Predominantly white and light gray background (#f0f2f5),
with warm orange (#E8913A) and blue (#4472C4) accent elements.
Composition: [Left-weighted / Centered / Right-weighted] with
ample space on [side] for title text overlay.
Mood: Professional, forward-looking, innovative.
No text in the image.
```

**Examples**:
- "数字化转型": futuristic cityscape with digital overlay, data streams connecting buildings
- "AI赋能业务": human hand and robotic hand reaching toward each other, surrounded by floating data nodes
- "云原生迁移": containers being lifted by clouds, from legacy server racks to cloud platforms

---

## Template 2: Industry Scenario

**Use when**: Showing a real-world application scenario for a solution

```
A photorealistic view of [industry] environment showing [specific scene].

Setting: [Detailed environment description]
Activity: [What people/systems are doing]
Technology elements: [Screens, devices, dashboards visible]
Lighting: Bright, modern, well-lit professional environment.
Camera angle: [Wide shot / Medium shot / Over-the-shoulder]
Style: High-quality commercial photography aesthetic.
No text overlays. No logos.
```

**Industry examples**:
- **Retail**: "Modern retail store with digital price tags, a customer using a mobile app for product recommendations, and an AI-powered inventory management dashboard visible on a tablet held by a store associate"
- **Manufacturing**: "Smart factory floor with robotic arms, IoT sensor indicators glowing blue on machinery, and a large monitoring dashboard showing real-time production metrics"
- **Healthcare**: "Modern hospital command center with multiple screens showing patient flow data, AI-assisted diagnostic imaging on one screen, and healthcare workers in scrubs reviewing data"
- **Finance**: "Sleek trading floor with multiple monitors showing financial dashboards, holographic data visualizations floating above desks, modern glass office aesthetic"

---

## Template 3: Abstract Concept Visualization

**Use when**: Visualizing technical concepts that have no physical form

```
An abstract visualization representing the concept of [concept name].

Visual metaphor: [Describe the metaphor]
Geometric elements: [Shapes, patterns, flows]
Color scheme: Gradient from [color1] to [color2], with [accent] highlights.
Composition: [Centered radial / Left-to-right flow / Layered depth]
Style: [Flat design with subtle shadows / Isometric 3D / Glassmorphism]
Background: Clean, light, suitable for overlaying presentation text.
```

**Concept examples**:
- **Zero Trust Security**: Concentric translucent shields around a glowing core, with verification checkpoints at each layer, blue-to-cyan gradient
- **Microservices**: Network of connected geometric pods, each a different subtle color, with data streams flowing between them
- **Data Lake**: Calm digital lake surface reflecting data nodes like stars, streams flowing in from multiple sources
- **DevOps Pipeline**: Flowing conveyor belt of code blocks transforming through stages (build → test → deploy), with green checkmarks

---

## Template 4: Slide Background / Hero Image

**Use when**: Creating subtle backgrounds for text-heavy slides

```
A subtle, abstract background for a presentation slide.

Pattern: [Geometric grid / Flowing waves / Particle field / Gradient mesh]
Colors: Soft gradient from [light color] to [slightly different light color].
Opacity: Very low contrast — the background must not compete with dark text overlaid on top.
Elements: [Faint geometric shapes / Soft bokeh lights / Circuit-like patterns]
Resolution: 1920x1080, seamless edges.
Style: Modern, corporate, calming.
```

> Important: Keep backgrounds VERY subtle. If text won't be readable on top, it's too busy.

---

## Template 5: Product/UI Concept Preview

**Use when**: Showing what an end-user experience looks like

```
A realistic mockup of [product type] displayed on [device].

Screen content: [Describe the UI - dashboard, app, portal]
Key features visible: [Sidebar navigation / Data visualization / Chat interface]
Device: [Modern laptop / Tablet / Phone / Large monitor]
Environment: [Clean desk / Blurred office background / Floating in space]
Perspective: [Slight angle / Front-facing / Over-shoulder view]
Style: Polished product photography, sharp focus on screen content.
```

---

## Template 6: Comparison / Before-After

**Use when**: Showing transformation (legacy → modern, manual → automated)

```
A split-screen comparison illustration:

LEFT side (Before): [Old/problematic state description]
- Muted, desaturated colors (grays, browns)
- [Specific visual elements showing the problem]
- Mood: Cluttered, outdated, inefficient

RIGHT side (After): [New/improved state description]
- Vibrant, clean colors (blues, greens, white)
- [Specific visual elements showing the solution]
- Mood: Organized, modern, efficient

Dividing line: Diagonal or vertical gradient transition from left to right.
Style: Corporate illustration, clear visual contrast between the two sides.
```

---

## Prompt Modifiers (Append to Any Template)

### Style Modifiers
- `corporate illustration style` — clean, professional, not too artistic
- `isometric 3D style` — popular for tech/architecture visuals
- `flat design with subtle gradients` — modern, minimal
- `photorealistic` — for industry scenarios
- `blueprint style on dark blue background` — for technical deep-dives
- `watercolor style` — for creative/design topics

### Composition Modifiers
- `leave the left 40% relatively empty for text overlay`
- `main subject centered with radial composition`
- `bird's eye view / top-down perspective`
- `wide panoramic format`

### Quality Modifiers
- `high detail, 4K quality`
- `sharp focus, studio lighting`
- `professional commercial quality`

### Negative Guidance
- `No text, no words, no letters in the image`
- `No watermarks or logos`
- `No busy patterns that would make overlaid text hard to read`
- `No specific real people or recognizable faces`
