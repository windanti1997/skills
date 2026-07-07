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

## Skill 发现路径

Codex 应主动查找项目和用户级 skill 路径，例如：

- 仓库内明确声明的 skill 目录
- `AGENTS.md` 里列出的 skill 路径
- `~/.codex/skills/`
- 用户当前消息明确提到的 skill

如果用户已经安装过相关 skill，Codex 不应该等用户再次提醒才使用。

## Trellis

信号：

- `.trellis/`
- `.trellis/tasks/`
- `.trellis/scripts/task.py`
- task 文档包含 PRD / design / implementation / checklist 结构
- 仓库文档提到 Trellis workflow

委托行为必须写清楚，而不是只写“按 Trellis 约定”：

- 哪个 `.trellis/tasks/...` 是权威任务。
- 是否允许执行 Agent 调用 `.trellis/scripts/task.py start/finish/archive`。
- `task.json` 状态由 Codex 还是执行 Agent 负责。
- `implement.md` 或等价执行记录由谁更新。
- 明确禁止执行 Agent 用自己的内部 task 系统替代 Trellis。

推荐默认：

- Codex 负责决定状态流转。
- 执行 Agent 至少负责更新 `implement.md` 执行记录。
- 如果授权执行 Agent 做状态流转，必须要求它使用项目的 Trellis 命令，例如 `python .trellis/scripts/task.py start <task>`，而不是自己的 task 工具。

Review 时必须同时检查：

- Trellis task 状态
- `implement.md` 执行记录
- 实际代码 diff
- 验证结果

代码已经实现但 Trellis 仍停在 planning，通常说明 workflow 脱节。

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
