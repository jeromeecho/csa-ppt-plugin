# 模版 B：架构/特性展示

**适用场景**：系统架构、功能模块、产品特性展示

**选择信号**：内容含"架构"、"模块"、"特性"、"功能"、"组件"、需要一个大图 + 几个特性卡片

---

## 布局骨架

```
┌──────────────────────────────────────────────────────┐
│ 标题（左上）+ 副标题                                    │ 58pt
├──────────────────────────────────────────────────────┤
│ ┌─ 左大卡片(60%) ────┐  ┌─ 右侧小卡片堆叠 ─────┐   │
│ │ 浅蓝底 #e8f4fd     │  │ ┌─ 特性卡片1 ───────┐│   │
│ │ 核心架构图/大图     │  │ │ #f0f2f5 + 图标    ││   │
│ │ 或主要内容区       │  │ └──────────────────┘│   │ 320pt
│ │                    │  │ ┌─ 特性卡片2 ───────┐│   │
│ │                    │  │ │ #f0f2f5 + 图标    ││   │
│ │                    │  │ └──────────────────┘│   │
│ └────────────────────┘  │ ┌─ 特性卡片3 ───────┐│   │
│                          │ │ #f0f2f5 + 图标    ││   │
│                          │ └──────────────────┘│   │
│                          └──────────────────────┘   │
├──────────────────────────────────────────────────────┤
│ 浅灰底部摘要栏 #f5f5f7 ｜3列洞察                       │ 56pt
└──────────────────────────────────────────────────────┘
```

## 区域说明

- **左大卡片（55-65%）**：浅蓝底 `#e8f4fd`，放架构图/流程图/核心内容
- **右侧 2-4 张小卡片堆叠**：浅灰底 `#f0f2f5`，每张有彩色图标+标题+说明

## 高度预算（960pt x 540pt）

```
标题区:     58pt  (10.7%)
主内容区:  320pt  (59.3%)
底部栏:     56pt  (10.4%)
间距+余:   106pt  (19.6%)
总计:      540pt  → 内容覆盖率 ~97%
```

## HTML 结构参考

```html
<div class="title-area">标题 + 副标题</div>
<div class="main-content" style="position:absolute; top:66pt; left:18pt; width:924pt; height:320pt; display:flex; gap:12pt;">
  <div class="left-panel" style="flex:0.6; background:#e8f4fd; border-radius:8pt;">
    <img src="architecture.png" style="width:100%; height:100%; object-fit:contain;"/>
  </div>
  <div class="right-stack" style="flex:0.4; display:flex; flex-direction:column; gap:8pt;">
    <div class="feature-card" style="flex:1; background:#f0f2f5; border-radius:8pt; padding:12pt;">...</div>
    <div class="feature-card" style="flex:1; background:#f0f2f5; border-radius:8pt; padding:12pt;">...</div>
    <div class="feature-card" style="flex:1; background:#f0f2f5; border-radius:8pt; padding:12pt;">...</div>
  </div>
</div>
<div class="insight-bar" style="position:absolute; top:434pt;">...</div>
```
