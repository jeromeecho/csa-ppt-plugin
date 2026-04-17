# 模版 F：多列等宽特性卡片

**适用场景**：功能展示、优势对比、分类展示（3-4项等权）

**选择信号**：内容含 3-4 个等权并列项目、"分类"、"优势"、"特性"，每项地位相同

---

## 布局骨架

```
┌──────────────────────────────────────────────────────┐
│ 标题（左上）+ 副标题                                    │ 58pt
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌─ 特性1 ─────┐ ┌─ 特性2 ─────┐ ┌─ 特性3 ─────┐  │
│  │ #f0f2f5     │ │ #f0f2f5     │ │ #f0f2f5     │  │
│  │ 彩色图标    │ │ 彩色图标    │ │ 彩色图标    │  │
│  │ (48pt居中)  │ │ (48pt居中)  │ │ (48pt居中)  │  │ 340pt
│  │ 标题 Bold   │ │ 标题 Bold   │ │ 标题 Bold   │  │
│  │ 正文列表    │ │ 正文列表    │ │ 正文列表    │  │
│  │ 或详细说明  │ │ 或详细说明  │ │ 或详细说明  │  │
│  └─────────────┘ └─────────────┘ └─────────────┘  │
│                                                      │
├──────────────────────────────────────────────────────┤
│ 浅灰底部栏 #f5f5f7 ｜洞察总结                          │ 56pt
└──────────────────────────────────────────────────────┘
```

## 区域说明

- **3 或 4 列等宽卡片**：浅灰底 `#f0f2f5`，圆角 8pt
- 每卡**顶部居中**放彩色图标（40-48pt）
- **标题** Bold 16pt，**正文** 12pt 列表
- **卡片间距** 16pt

## 高度预算（960pt x 540pt）

```
标题区:     58pt  (10.7%)
卡片区:    340pt  (63.0%)
底部栏:     56pt  (10.4%)
间距+余:    86pt  (15.9%)
总计:      540pt  → 覆盖率 ~96%
```

## HTML 结构参考

```html
<div class="title-area">标题 + 副标题</div>
<div class="cards-area" style="position:absolute; top:66pt; left:18pt; width:924pt; height:340pt; display:flex; gap:16pt;">
  <div class="feature-card" style="flex:1; background:#f0f2f5; border-radius:8pt; padding:16pt; text-align:center;">
    <img src="icon-1.png" style="width:48pt; height:48pt; margin:0 auto 12pt;"/>
    <h3 style="color:#1a1a2e; font-size:16pt; font-weight:bold;">特性名称</h3>
    <ul style="text-align:left; color:#333333; font-size:12pt;">...</ul>
  </div>
  <!-- x3 or x4 -->
</div>
<div class="insight-bar" style="position:absolute; top:434pt; left:18pt; width:924pt; height:56pt; background:#f5f5f7; border-radius:8pt;">...</div>
```
