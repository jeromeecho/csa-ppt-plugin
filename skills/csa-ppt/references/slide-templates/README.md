# PPT 模版索引

> 先分析内容语义，再选模版。不要所有页面都用同一模版。

## 模版选择决策表

| 内容类型 | 推荐模版 | 文件 |
|----------|----------|------|
| 新旧对比、范式迁移、数据变化 | **A** 对比/Before-After | [template-A-comparison.md](template-A-comparison.md) |
| 系统架构、功能模块、产品特性 | **B** 架构/特性展示 | [template-B-architecture.md](template-B-architecture.md) |
| 时间演进、里程碑、阶段规划 | **C** 时间线/里程碑 | [template-C-timeline.md](template-C-timeline.md) |
| 最佳实践、多要点总结（3-6项） | **D** 编号网格 | [template-D-numbered-grid.md](template-D-numbered-grid.md) |
| 概念说明、需图表配合的内容 | **E** 左文右图 | [template-E-text-diagram.md](template-E-text-diagram.md) |
| 功能展示、等权分类（3-4项） | **F** 多列等宽特性卡片 | [template-F-multi-column.md](template-F-multi-column.md) |

## 通用组件

所有模版共享的组件规范（标题区、卡片、徽章、底部栏等）见 [_shared.md](_shared.md)。

## 如何新增模版

1. 在 `templates/` 目录下创建 `template-G-xxx.md`（按字母顺序递增）
2. 使用统一格式：适用场景 → 布局骨架 → 区域说明 → 高度预算 → HTML 结构参考
3. 在本文件的决策表中添加一行
4. 在 `CLAUDE.md` 的模版选择指南中添加对应条目
