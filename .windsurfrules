# CSA PPT Plugin — Default Slide Design System

> 本文件为所有平台通用的 PPT 设计规范。详细模版定义见 `skills/csa-ppt/references/slide-templates/`。

## 设计理念

**淡雅清新、留白为主、彩色点缀**。标题左上深色粗体，浅灰卡片背景，底部栏用浅色底+彩色竖线，禁止全幅深色横条。

## 核心规则

### 页面基础
- 幻灯片尺寸：16:9（960pt x 540pt）
- 页面背景：纯白 `#ffffff`
- 内容覆盖率 >= 95%，禁止大面积空白

### 配色方案
| 用途 | 色值 |
|------|------|
| 主强调色（橙） | `#E8913A` — 序号徽章、图标、关键数字、左竖线 |
| 辅助色（蓝） | `#4472C4` — 图表系列、链接、少量强调 |
| 成功/绿 | `#70AD47` |
| 警告/红 | `#E74C3C` |
| 标题色 | `#1a1a2e` |
| 正文色 | `#333333` |
| 卡片背景 | `#f0f2f5` |
| 底部栏背景 | `#f5f5f7` |

### 禁止样式
- **禁止** 全幅深色标题栏（`#4472C4` 全宽蓝条）
- **禁止** 全幅深色底部栏（`#2F5496` 全宽深蓝条）
- **禁止** 大面积深色色块 > 15%
- 彩色仅用于：徽章、竖线（4pt）、图标、图表

### 字体
- 标题：28-32pt Bold `#1a1a2e` 左对齐
- 正文：12-14pt `#333333`
- 最小字号 >= 10pt
- 英文 Arial | 中文 Microsoft YaHei | 代码 Courier New

### 可视化
- 每页必须包含至少一种图表/可视化元素
- 推荐两栏布局：左文字(35-40%) + 右图表(55-62%)
- 图表配色：主系列 `E8913A` → `4472C4` → `70AD47` → `FFC000`

## 模版选择

根据内容语义选择模版（详见 `skills/csa-ppt/references/slide-templates/`）：

| 内容类型 | 模版 | 文件 |
|----------|------|------|
| 新旧对比 | A | `template-A-comparison.md` |
| 系统架构 | B | `template-B-architecture.md` |
| 时间线 | C | `template-C-timeline.md` |
| 编号网格 | D | `template-D-numbered-grid.md` |
| 左文右图 | E | `template-E-text-diagram.md` |
| 多列卡片 | F | `template-F-multi-column.md` |

通用组件：`_shared.md` | 索引：`README.md`

## html2pptx 高度填充

HTML body 尺寸必须匹配 PPTX：`width:960pt; height:540pt;`。使用绝对定位+显式高度预算，禁止依赖 flex 自动撑满。

## Hook 强制规则

`scripts/check-slide-html.sh` 可作为 PostToolUse hook 自动检查 slide HTML 违规。配置模版见 `skills/csa-ppt/hooks-settings.json`。
