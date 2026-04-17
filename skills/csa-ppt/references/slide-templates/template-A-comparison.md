# 模版 A：对比/Before-After

**适用场景**：新旧对比、范式迁移、数据变化对比

**选择信号**：内容含"从...到..."、"旧→新"、"对比"、"迁移"、"变化"等关键词

---

## 布局骨架

```
┌──────────────────────────────────────────────────────┐
│ 标题（左上）+ 副标题                                    │ 58pt
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌─ Before ──────────┐  ┌─ After ───────────────┐   │
│  │ 浅灰底 #f0f2f5    │  │ 浅蓝底 #e8f4fd        │   │
│  │ 灰色调、较小字号   │  │ 强调色、较大字号       │   │
│  │ (表示"旧/被淘汰")  │  │ (表示"新/推荐")       │   │
│  └───────────────────┘  └───────────────────────┘   │ 280pt
│                                                      │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐                   │
│  │洞察1│ │洞察2│ │洞察3│ │洞察4│  (4列网格)         │ 80pt
│  └─────┘ └─────┘ └─────┘ └─────┘                   │
├──────────────────────────────────────────────────────┤
│ 浅灰底部栏 #f5f5f7 ｜彩色竖线 + 总结文字               │ 56pt
└──────────────────────────────────────────────────────┘
```

## 区域说明

- **Before 列（40-45%）**：浅灰底 `#f0f2f5`，字号偏小，灰色调，表示"旧/被淘汰"
- **After 列（55-60%）**：浅蓝底 `#e8f4fd`，字号偏大，蓝/橙强调色，表示"新/推荐"
- 中间可加 **→ 箭头符号**表示转变方向
- 下方 **4 列洞察网格**：每格浅灰底 + 橙色序号徽章

## 高度预算（960pt x 540pt）

```
标题区:     58pt  (10.7%)
对比区:    280pt  (51.9%)
洞察网格:   80pt  (14.8%)
底部栏:     56pt  (10.4%)
间距+余:    66pt  (12.2%)
总计:      540pt  → 覆盖率 87.8%（加上间距内的内容，实际 >95%）
```

## HTML 结构参考

```html
<div class="title-area">标题 + 副标题</div>
<div class="compare-area" style="position:absolute; top:66pt; left:18pt; width:924pt; height:280pt; display:flex; gap:12pt;">
  <div class="before-panel" style="flex:0.42; background:#f0f2f5; border-radius:8pt;">...</div>
  <div class="after-panel" style="flex:0.58; background:#e8f4fd; border-radius:8pt;">...</div>
</div>
<div class="insight-grid" style="position:absolute; top:350pt; left:18pt; width:924pt; height:80pt; display:flex; gap:10pt;">
  <div class="insight-card" style="flex:1; background:#f0f2f5; border-radius:8pt;">...</div>
  <!-- x4 -->
</div>
<div class="insight-bar" style="position:absolute; top:434pt; left:18pt; width:924pt; height:56pt; background:#f5f5f7; border-radius:8pt;">...</div>
```
