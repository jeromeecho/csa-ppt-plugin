# PPT 全局模版规范 (Multi-Template Design System)

所有 PPT / 幻灯片 / 演示文稿默认必须严格遵循此模版规范。除非用户明确要求其他风格，否则一律以此为准。

> 设计理念：**淡雅清新、留白为主、彩色点缀**。标题左上深色粗体，浅灰卡片背景，底部栏用浅色底+彩色竖线，禁止全幅深色横条。

---

## 1. 页面基础

| 属性 | 值 |
|------|-----|
| 幻灯片尺寸 | 16:9 宽屏（13.33" x 7.5" / 960pt x 540pt） |
| 页面背景色 | **纯白 `#ffffff`** |
| 整体风格 | 浅色留白为主，彩色仅用于点缀（序号徽章、竖线、图标），信息密度高、层次分明 |
| 内容覆盖率 | **>= 95%** 页面面积（横向+纵向），禁止大面积空白 |

---

## 2. 配色方案

| 用途 | 色值 | 说明 |
|------|------|------|
| **主强调色（橙）** | `#E8913A` | 序号徽章、图标填色、关键数字、左竖线 |
| **辅助色（蓝）** | `#4472C4` | 图表系列色、链接色、少量辅助强调 |
| **成功/绿** | `#70AD47` | 通过标记、正面指标 |
| **警告/红** | `#E74C3C` | 失败标记、警告信息 |
| **标题色** | `#1a1a2e` | 页面主标题、粗体大字 |
| **正文色** | `#333333` | 正文内容、列表项 |
| **副标题/辅助色** | `#666666` | 副标题、辅助说明文字 |
| **卡片背景** | `#f0f2f5` | 内容卡片、模块区块底色 |
| **浅蓝特殊背景** | `#e8f4fd` | 架构图区域、特殊强调卡片 |
| **底部栏背景** | `#f5f5f7` | 底部摘要/洞察栏 |
| **分隔线** | `#e0e0e0` | 卡片间细线、区域分隔 |

### 禁止使用的样式

- **禁止** 全幅深色标题栏（如 `#4472C4` 全宽蓝条）
- **禁止** 全幅深色底部栏（如 `#2F5496` 全宽深蓝条）
- **禁止** 蓝色/深色背景的栏目头
- **禁止** 大面积深色色块占据超过页面 15% 的面积
- 彩色仅用于：序号徽章、左侧竖线（4pt宽）、图标、图表、关键数字

### 图表配色（PptxGenJS 无 # 前缀）

主系列 `E8913A` | 第二 `4472C4` | 第三 `70AD47` | 第四 `FFC000` | 第五 `5B9BD5` | 第六 `A5A5A5`

---

## 3. 字体与排版

| 元素 | 字号 | 字重 | 颜色 | 对齐 |
|------|------|------|------|------|
| **页面主标题** | **28-32pt** | **Bold** | `#1a1a2e` | **左对齐**，无背景色 |
| **页面副标题** | 14-16pt | Regular | `#666666` | **左对齐** |
| **卡片标题** | 16-18pt | **Bold** | `#1a1a2e` 或强调色 | 左对齐 |
| **卡片引导语** | 13-14pt | *Italic* | 对应强调色 | 左对齐 |
| **正文/列表** | 12-14pt | Regular | `#333333` | 左对齐 |
| **底部洞察** | 11-13pt | Regular/Bold | `#333333`/`#1a1a2e` | 左对齐 |
| **序号徽章** | 16-20pt | **Bold** | `#ffffff` | 居中（橙底白字） |
| **最小字号** | **>= 10pt** | — | — | — |

字体：英文 **Arial** / Segoe UI | 中文 **Microsoft YaHei** | 代码 Courier New

---

## 4. 模版选择指南

**根据内容语义选择模版，不要所有页面都用同一模版。** 详见 [`templates/`](templates/) 目录。

| 内容类型 | 模版 | 文件 |
|----------|------|------|
| 新旧对比、范式迁移 | **A** | [template-A-comparison.md](templates/template-A-comparison.md) |
| 系统架构、功能模块 | **B** | [template-B-architecture.md](templates/template-B-architecture.md) |
| 时间演进、里程碑 | **C** | [template-C-timeline.md](templates/template-C-timeline.md) |
| 最佳实践、多要点（3-6项） | **D** | [template-D-numbered-grid.md](templates/template-D-numbered-grid.md) |
| 概念说明、需图表配合 | **E** | [template-E-text-diagram.md](templates/template-E-text-diagram.md) |
| 功能展示、等权分类 | **F** | [template-F-multi-column.md](templates/template-F-multi-column.md) |

通用组件规范（卡片、徽章、底部栏、扩展区等）见 [templates/_shared.md](templates/_shared.md)。

模版索引与扩展说明见 [templates/README.md](templates/README.md)。

---

## 5. 可视化图表规范

**每页幻灯片都应包含至少一种可视化元素**，禁止纯文字罗列。

| 图表类型 | 适用场景 | 实现方式 |
|----------|----------|----------|
| 柱状图/折线图/饼图 | 数值对比、趋势、占比 | PptxGenJS |
| 流程图/循环图/时间线 | 步骤、反馈闭环、演进 | SVG → PNG (Sharp) |
| 金字塔/同心圆/三角图 | 层级、包含、三方关系 | SVG → PNG (Sharp) |

布局原则：
- **两栏布局（推荐）**：左文字(35-40%) + 右图表(55-62%)
- **禁止上下堆叠**文字和图表
- 图表配色用第 2 节色板，主系列橙色 `E8913A`

---

## 6. 版本管理

- 修改PPT时默认保留前一个版本备份
- 命名：`原文件名_vN.pptx`（N 递增）

---

## 7. html2pptx 高度填充强制规则

**最高优先级：内容必须纵向+横向填满 95% 以上页面面积。**

### 核心规则

html2pptx 对 CSS 坐标做 **1:1 pt→inch 映射**，不会自动缩放。HTML body 尺寸必须匹配 PPTX 幻灯片尺寸。

| PPTX 尺寸 | HTML body | PptxGenJS |
|---|---|---|
| 960pt x 540pt | `width: 960pt; height: 540pt;` | `defineLayout({ width: 13.333, height: 7.5 })` |
| 720pt x 405pt | `width: 720pt; height: 405pt;` | `pptx.layout = 'LAYOUT_16x9'` |

### 强制方法：绝对定位 + 显式高度预算

```css
body { width: 960pt; height: 540pt; margin: 0; padding: 0; position: relative; }
.title-area     { position: absolute; top: 0;     left: 24pt; width: 912pt; height: 62pt;  }
.main-content   { position: absolute; top: 66pt;  left: 18pt; width: 924pt; height: 280pt; }
.extension-area { position: absolute; top: 350pt; left: 18pt; width: 924pt; height: 80pt;  }
.insight-bar    { position: absolute; top: 434pt; left: 18pt; width: 924pt; height: 56pt;  }
/* 高度预算：62+280+80+56+间距 = 97.4% ✓ */
```

### 禁止事项

- **禁止** `720pt x 405pt` HTML 匹配 `960pt x 540pt` PPTX
- **禁止** 依赖 flex 自动高度撑满
- **禁止** 仅用 `max-height` 不设 `height`
- **禁止** 提交前不做覆盖率验证
