# 模版 D：编号网格

**适用场景**：最佳实践、多要点总结、功能列表（3-6项）

**选择信号**：内容含 3-6 个并列要点、"最佳实践"、"原则"、"要素"、"步骤"（非时间顺序）

---

## 布局骨架

```
┌──────────────────────────────────────────────────────┐
│ 标题（左上）+ 副标题                                    │ 58pt
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌─ ① ──────┐  ┌─ ② ──────┐  ┌─ ③ ──────┐         │
│  │ 橙色徽章  │  │ 橙色徽章  │  │ 橙色徽章  │         │
│  │ 图标+标题 │  │ 图标+标题 │  │ 图标+标题 │         │ 上排
│  │ 正文列表  │  │ 正文列表  │  │ 正文列表  │         │ 180pt
│  └──────────┘  └──────────┘  └──────────┘         │
│                                                      │
│  ┌─ ④ ──────┐  ┌─ ⑤ ──────┐  (可选 ⑥)              │
│  │ 橙色徽章  │  │ 橙色徽章  │                         │ 下排
│  │ 图标+标题 │  │ 图标+标题 │                         │ 140pt
│  │ 正文列表  │  │ 正文列表  │                         │
│  └──────────┘  └──────────┘                         │
│                                                      │
├──────────────────────────────────────────────────────┤
│ 浅灰底部栏 #f5f5f7 ｜洞察总结                          │ 56pt
└──────────────────────────────────────────────────────┘
```

## 区域说明

- **3+2 或 3+3 网格布局**
- 每张卡片：浅灰底 `#f0f2f5`，左上角橙色圆形序号徽章（28pt白色数字），彩色图标，标题+正文
- **卡片间距** 12-16pt
- 序号徽章：`#E8913A` 橙色圆形，白色数字

## 高度预算（960pt x 540pt）

```
标题区:     58pt  (10.7%)
上排卡片:  180pt  (33.3%)
下排卡片:  140pt  (25.9%)
底部栏:     56pt  (10.4%)
间距+余:   106pt  (19.6%)
总计:      540pt  → 覆盖率 ~97%
```

## HTML 结构参考

```html
<div class="title-area">标题 + 副标题</div>
<div class="grid-top" style="position:absolute; top:66pt; left:18pt; width:924pt; height:180pt; display:flex; gap:12pt;">
  <div class="grid-card" style="flex:1; background:#f0f2f5; border-radius:8pt; padding:12pt;">
    <div class="badge" style="width:28pt; height:28pt; background:#E8913A; color:#fff; border-radius:50%; font-size:16pt; font-weight:bold; text-align:center; line-height:28pt;">1</div>
    <h3>标题</h3>
    <ul>...</ul>
  </div>
  <!-- x3 -->
</div>
<div class="grid-bottom" style="position:absolute; top:254pt; left:18pt; width:924pt; height:140pt; display:flex; gap:12pt;">
  <!-- x2 or x3 cards -->
</div>
<div class="insight-bar" style="position:absolute; top:434pt;">...</div>
```
