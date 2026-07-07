# 项目工作流识别指南

Codex 委托执行前，先识别项目已有工作流，并把识别结果写进 delegation brief。

## 仓库级规则

优先查找：

- `AGENTS.md`
- `CLAUDE.md`
- `README.md`
- `.cursor/rules/`
- `.windsurfrules`
- 其他项目内的 Agent 指令

这些规则优先级高于本 skill 的通用建议。

## Trellis

信号：

- `.trellis/`
- `.trellis/tasks/`
- task 文档包含 PRD / design / implementation / checklist 结构
- 仓库文档提到 Trellis workflow

委托行为：

- 要求执行 Agent 先创建或更新对应 `.trellis/tasks/` 文档。
- 要求任务文档、实现记录、验收标准和代码保持一致。

## Superpowers 类工作流

信号：

- 文件或目录提到 `superpower`、`superpowers` 或类似工作流关键词。
- 项目要求先使用某个 skill、checklist、workflow 或 plan。
- 仓库文档明确说明 Agent 工作流程。

委托行为：

- 要求执行 Agent 遵守发现的 workflow。
- 不要强行改成 Trellis。
- 如果 workflow 要求先写 plan/checklist，就把这个要求放进 brief。

## Spec / Plan 工作流

信号：

- `spec.md` / `SPEC.md`
- `plan.md` / `PLAN.md`
- `design.md`
- `implementation.md`
- `tasks.md`
- `docs/specs/`
- `docs/plans/`
- `.kiro/specs/`

委托行为：

- 要求执行 Agent 先读已有 spec / plan。
- 行为变化时更新对应文档。
- 不要额外创建 Trellis 文件，除非项目本身也使用 Trellis。

## 没有发现工作流

委托行为：

- 使用 delegation brief 作为任务契约。
- 不要为了显得完整而创建重流程文件。
- 只有任务足够大或用户要求时，才让执行 Agent 先写简短实现计划。
