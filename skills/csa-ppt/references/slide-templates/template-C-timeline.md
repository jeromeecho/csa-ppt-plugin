# 模版 C：时间线/里程碑

**适用场景**：演进路径、发展历程、阶段规划

**选择信号**：内容含"阶段"、"演进"、"路线图"、"里程碑"、"版本"、时间顺序的事件列表

---

## 布局骨架

```
┌──────────────────────────────────────────────────────┐
│ 标题（左上）+ 副标题                                    │ 58pt
├──────────────────────────────────────────────────────┤
│  ┌─ 核心数字/概览 ──────────────────────────────┐    │
│  │ 大号数字 48-64pt + 说明文字                    │    │ 80pt
│  └──────────────────────────────────────────────┘    │
│                                                      │
│  ●─────────●─────────●─────────●─────────●          │ (横轴)
│  ┌───┐    ┌───┐    ┌───┐    ┌───┐    ┌───┐         │
│  │M1 │    │M2 │    │M3 │    │M4 │    │M5 │         │ 200pt
│  │   │    │   │    │   │    │   │    │   │         │
│  └───┘    └───┘    └───┘    └───┘    └───┘         │
│                                                      │
├──────────────────────────────────────────────────────┤
│ 浅橙底警告栏 或 浅灰洞察栏                              │ 50pt
├──────────────────────────────────────────────────────┤
│ 浅灰底部栏 #f5f5f7                                    │ 52pt
└──────────────────────────────────────────────────────┘
```

## 区域说明

- **大号核心数字**：48-64pt，橙色 `#E8913A` Bold
- **时间线横轴**：灰色线 `#e0e0e0` 2pt + 彩色节点圆点
- **里程碑卡片**：浅灰底 `#f0f2f5`，橙色序号徽章
- **可选警告栏**：浅橙底 `#FFF8F0` + 左竖线 `#E8913A`

## 高度预算（960pt x 540pt）

```
标题区:     58pt  (10.7%)
核心数字:   80pt  (14.8%)
时间线区:  200pt  (37.0%)
警告栏:     50pt   (9.3%)
底部栏:     52pt   (9.6%)
间距+余:   100pt  (18.5%)
总计:      540pt  → 覆盖率 ~96%
```

## HTML 结构参考

```html
<div class="title-area">标题 + 副标题</div>
<div class="hero-number" style="position:absolute; top:66pt; left:18pt; width:924pt; height:80pt; background:#f0f2f5; border-radius:8pt;">
  <span style="font-size:56pt; color:#E8913A; font-weight:bold;">5</span>
  <span style="font-size:16pt; color:#333333;">个关键里程碑</span>
</div>
<div class="timeline-area" style="position:absolute; top:150pt; left:18pt; width:924pt; height:200pt;">
  <!-- SVG timeline or flex cards -->
</div>
<div class="warning-bar" style="position:absolute; top:358pt; left:18pt; width:924pt; height:50pt; background:#FFF8F0; border-left:4pt solid #E8913A; border-radius:8pt;">...</div>
<div class="insight-bar" style="position:absolute; top:414pt; left:18pt; width:924pt; height:52pt; background:#f5f5f7; border-radius:8pt;">...</div>
```
