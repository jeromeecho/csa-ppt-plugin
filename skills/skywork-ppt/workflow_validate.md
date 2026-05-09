# PPT Visual Validation Workflow (MANDATORY)

**This workflow is MANDATORY after ANY PPTX generation or modification.** No PPTX output may be delivered to the user until validation passes.

This applies to ALL paths:
- `workflow_generate.md` (new PPT)
- `workflow_imitate.md` (template-based)
- `workflow_edit.md` (edit existing)
- `workflow_local.md` (structural operations that add content)
- **Any custom Python script** that creates or modifies `.pptx` files

## 0. Set script path

```bash
CSA_SCRIPTS="$HOME/.claude/plugins/marketplaces/csa-skills/scripts"
```

## 1. Run validation

```bash
$PYTHON_CMD "$CSA_SCRIPTS/validate_visual.py" /absolute/path/output.pptx --output /tmp/ppt_validation.json
```

Exit code:
- `0` = PASS (no issues, proceed to deliver)
- `1` = FAIL (issues found, must fix before delivering)

## 2. Auto-fix if issues found

```bash
$PYTHON_CMD "$CSA_SCRIPTS/fix_overflow.py" /absolute/path/output.pptx \
  --report /tmp/ppt_validation.json \
  -o /absolute/path/output.pptx
```

The fix script applies these strategies following the priority:
**完整可见 > 合理布局 > 字体大小**
(Content fully visible > good layout > font size)

字体大小是**软约束**，内容完整可见是**硬约束**。为保证内容完整显示，字体可缩至任意合理大小。

1. Expand container height (if space available — preserves font, avoids wrapping)
2. Widen shape (eliminates widow lines without shrinking font)
3. Reduce font size (no hard minimum — content visibility is the hard constraint)
4. Reduce paragraph spacing
5. Truncate text (last resort)

## 3. Re-validate (算法)

```bash
$PYTHON_CMD "$CSA_SCRIPTS/validate_visual.py" /absolute/path/output.pptx --output /tmp/ppt_validation.json
```

## 4. LLM 视觉校验（MANDATORY — 与算法校验结合）

**算法校验通过后，还必须进行 LLM 视觉校验。两者都通过才算通过。**

PIL 文本测量与 PowerPoint 实际渲染存在差异（行距、字间距、margin处理不同），
算法显示"不溢出"但实际渲染可能仍然裁切。因此必须结合 LLM 看截图确认。

### 执行方法（模型无关 — 不绑定任何特定 LLM）

Coding agent 自身就是 LLM，直接使用 agent 内置的多模态能力读取截图：

**Step 4a: 渲染幻灯片为 PNG**

```bash
$PYTHON_CMD "$CSA_SCRIPTS/render_slides.py" /absolute/path/output.pptx \
  --output-dir /tmp/slide_renders/ \
  --slides <新建或修改的页码>
```

渲染优先使用 LibreOffice（高保真），不可用时降级为 PIL 近似渲染。

**Step 4b: Agent 直接读取 PNG 图片进行视觉验证**

Agent 使用自身的 Read 工具（或等效的图片查看能力）逐张读取 `/tmp/slide_renders/slide-*.png`，确认：

1. ✅ 所有文本完整可见（无裁切、无截断、无溢出边界）
2. ✅ 无 widow line（换行后最后一行仅1-2个字符）
3. ✅ 布局合理（无重叠、无异常空白、元素对齐）
4. ✅ 图表/图标正常显示

**Step 4c: 发现问题时的处理**

如果视觉检查发现问题 → 回到 Step 2 修复 → 重新渲染截图 → 再次检查。

### 重要说明

- **不绑定特定模型**：任何 coding agent（Claude Code、Codex、Copilot 等）都可执行此流程
- Agent 已经配置好了模型，直接使用 agent 的 Read/图片查看能力即可
- 不需要额外调用外部 API 或硬编码任何模型名称
- Agent 本身就是多模态 LLM，天然具备图片理解能力

**只有算法校验 + LLM 视觉校验都通过，才可交付。**

## 5. Repeat or report

- If 算法 PASS + LLM 视觉 PASS → deliver the file
- If FAIL with <= 5 minor issues (overflow < 0.1") on pre-existing slides → acceptable, deliver with note
- If FAIL with overflow > 0.2" on newly created/edited slides → **do NOT deliver**. Manually fix the source code that generated these slides (adjust font sizes, text box heights, or content length) and regenerate.

## Key rules

1. **Never deliver a PPTX without running validation first**
2. **Newly created slides must have ZERO text_overflow or widow_line issues**
3. Pre-existing slides may have minor issues that are acceptable
4. **内容完整可见是硬约束** — 所有文本必须完整显示，这是最高优先级
5. **No widow lines** — if text wraps and the last line has < 20% of content, fix it (reduce font or widen)
6. 字体大小尽量 >= 10pt，但为满足完整可见可缩至任意合理大小（软约束，永远让步于内容可见性）

## Dependencies

### 必需 (Required)
- `python-pptx`
- `Pillow` (PIL)

```bash
$PYTHON_CMD -m pip install -q python-pptx Pillow
```

### 推荐 (Recommended — 高保真渲染)

LibreOffice 用于将 PPTX 渲染为高保真 PNG（比 PIL 近似渲染准确得多）。
**跨平台可用，但非强制依赖** — 没有 LibreOffice 时自动降级为 PIL 渲染 + 增强安全系数。

| 平台 | 安装命令 |
|------|---------|
| macOS | `brew install --cask libreoffice` |
| Windows | `choco install libreoffice` 或从 [libreoffice.org](https://www.libreoffice.org/download/) 下载 |
| Linux (Debian/Ubuntu) | `sudo apt install libreoffice` |
| Linux (RHEL/Fedora) | `sudo dnf install libreoffice-impress` |

`render_slides.py` 会自动检测所有平台上的 LibreOffice 路径，无需手动配置。

### 降级策略

当 LibreOffice 不可用时：
1. **算法校验** 使用增强的安全系数（1.18x-1.25x）补偿 PIL 测量偏差
2. **PIL 渲染** 提供近似视觉输出供 LLM 检查（已知不如 PowerPoint 精确）
3. **建议**：对于关键交付物，强烈建议安装 LibreOffice 以获得最准确的视觉校验

### ⚠️ 已知限制：PIL 渲染 vs PowerPoint 的差异

**重要**：PIL 渲染存在以下已知问题，LLM 看 PIL 截图可能无法发现真实溢出：

| 差异项 | PIL 渲染 | PowerPoint 实际 |
|--------|---------|----------------|
| 行距 | 使用字体高度 * 1.0（紧凑） | 使用字体高度 * 1.2-1.5（标准单倍行距） |
| 段间距 | 忽略或最小化 | 有明显的段前/段后间距 |
| CJK 字符 | 部分字体无法渲染（显示为□） | 完整渲染 |
| 文本裁剪 | **不裁剪** — 所有文本都画出来 | **按文本框边界裁剪** |
| 字间距 | 近似计算 | 精确 kerning |

**核心问题**：PIL 不会裁剪溢出的文本（它把所有内容都画出来），而 PowerPoint 会在文本框边界处截断。因此 LLM 看 PIL 图可能觉得"一切正常"，但实际在 PowerPoint 中文本已被裁剪。

**应对措施**：
1. **有 LibreOffice**：高保真渲染，与 PowerPoint 一致，LLM 能准确判断
2. **无 LibreOffice**：依赖算法校验的安全系数（已对多行密集内容加 1.25x 补偿）；LLM 视觉校验仅作为辅助，不能完全信任
3. **最佳实践**：首次使用时安装 LibreOffice（一次性操作），之后所有校验都是高保真的

### 代码中的 fallback 逻辑

`render_slides.py` 中的处理顺序：

```python
# 1. 尝试 LibreOffice（跨平台路径自动检测）
output_files = render_with_libreoffice(pptx_path, output_dir, slides)

if output_files:
    # 高保真渲染成功
    pass
else:
    # 2. 降级为 PIL 渲染（近似，有已知差异）
    output_files = render_with_pil(pptx_path, output_dir, slides)
```

`validate_visual.py` 中的安全系数：

```python
# 根据内容密度动态调整安全系数
para_count = len([p for p in paragraphs if p.text.strip()])
if para_count <= 2:      safety_factor = 1.0   # 标题/标签
elif para_count <= 4:    safety_factor = 1.10  # 中等内容
elif para_count <= 8:    safety_factor = 1.18  # 较密内容
else:                    safety_factor = 1.25  # 密集多段落
```
