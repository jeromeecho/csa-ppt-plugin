# 模版 E：左文右图

**适用场景**：概念解释、需要图表配合的内容、三层控制模型等

**选择信号**：内容需要一侧文字说明 + 一侧图表/图形，含"模型"、"概念"、"公式"、"框架"

---

## 布局骨架

```
┌──────────────────────────────────────────────────────┐
│ 标题（左上）+ 副标题                                    │ 58pt
├──────────────────────────────────────────────────────┤
│ ┌─ 左侧文字(38%) ──┐  ┌─ 右侧图表(58%) ─────────┐  │
│ │ ┌─ 卡片1 ──────┐ │  │ 浅灰底 #f0f2f5           │  │
│ │ │ #f0f2f5      │ │  │ 或浅蓝底 #e8f4fd          │  │
│ │ │ 彩色标题+列表 │ │  │                           │  │
│ │ └──────────────┘ │  │   控制流图 / 架构图        │  │ 278pt
│ │ ┌─ 卡片2 ──────┐ │  │   / 流程图 / 数据图表      │  │
│ │ │ #f0f2f5      │ │  │                           │  │
│ │ │ 彩色标题+列表 │ │  │                           │  │
│ │ └──────────────┘ │  │                           │  │
│ │ ┌─ 卡片3 ──────┐ │  │                           │  │
│ │ │ #f0f2f5      │ │  │                           │  │
│ │ └──────────────┘ │  └───────────────────────────┘  │
│ └──────────────────┘                                  │
├──────────────────────────────────────────────────────┤
│ ┌─ 公式/洞察(46%) ─┐  ┌─ 问题框架(50%) ──────────┐  │
│ │ #f0f2f5+蓝竖线    │  │ #f0f2f5+橙竖线            │  │ 80pt
│ └──────────────────┘  └───────────────────────────┘  │
├──────────────────────────────────────────────────────┤
│ 浅灰底部栏 #f5f5f7 ｜3列洞察（图标+标题+正文）          │ 56pt
└──────────────────────────────────────────────────────┘
```

## 区域说明

- **左侧（35-40%）**：2-4 张浅灰卡片竖向堆叠，每张有彩色圆点/图标+标题+列表
- **右侧（55-62%）**：大图表区域（浅灰或浅蓝底），放架构图/流程图/控制图
- **中间扩展区**：两栏，浅灰底+左侧彩色竖线（4pt），放公式/框架
- **底部 3 列洞察栏**

## 高度预算（960pt x 540pt）

```
标题区:     58pt  (10.7%)
主内容区:  278pt  (51.5%)
扩展区:     80pt  (14.8%)
底部栏:     56pt  (10.4%)
间距+余:    68pt  (12.6%)
总计:      540pt  → 覆盖率 97.4%
```

## HTML 结构参考

```html
<div class="title-area" style="position:absolute; top:8pt; left:24pt; width:912pt; height:54pt;">
  <h1 style="color:#1a1a2e; font-size:28pt; font-weight:bold;">标题</h1>
  <p style="color:#666666; font-size:13pt;">副标题</p>
</div>
<div class="left-col" style="position:absolute; top:66pt; left:18pt; width:350pt; height:278pt; display:flex; flex-direction:column; gap:6pt;">
  <div class="layer-card" style="flex:1; background:#f0f2f5; border-radius:8pt; padding:8pt 12pt;">
    <div style="display:flex; align-items:center; gap:8pt;">
      <div style="width:10pt; height:10pt; border-radius:50%; background:#4472C4;"></div>
      <p style="color:#4472C4; font-size:15pt; font-weight:bold;">卡片标题</p>
    </div>
    <ul style="color:#333333; font-size:11pt;">...</ul>
  </div>
  <!-- more cards -->
</div>
<div class="right-col" style="position:absolute; top:66pt; left:378pt; width:564pt; height:278pt;">
  <div style="background:#f0f2f5; border-radius:8pt; width:100%; height:100%;">
    <img src="diagram.png"/>
  </div>
</div>
<div class="extension-area" style="position:absolute; top:348pt; left:18pt; width:924pt; height:80pt; display:flex; gap:12pt;">
  <div style="flex:1; background:#f0f2f5; border-radius:8pt; border-left:4pt solid #4472C4; padding:10pt 14pt;">...</div>
  <div style="flex:1; background:#f0f2f5; border-radius:8pt; border-left:4pt solid #E8913A; padding:10pt 14pt;">...</div>
</div>
<div class="insight-bar" style="position:absolute; top:432pt; left:18pt; width:924pt; height:56pt; background:#f5f5f7; border-radius:8pt;">...</div>
```
