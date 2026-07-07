# 示例：Trellis 项目里的大功能实现

## 场景

用户让 Codex 实现一个跨多个模块的新功能。仓库里存在 `.trellis/tasks/`。

## Codex 应该怎么做

1. 先读 `AGENTS.md` 和 Trellis workflow 文档。
2. 必要时和用户确认验收标准。
3. 写 delegation brief，要求执行 Agent 先更新 Trellis task，再写代码。
4. 调用 Agent CLI 执行。
5. 执行完成后，Codex review Trellis 文档、diff 和测试结果。

## Brief 片段

```markdown
Project workflow detected: Trellis.
Before implementation, create or update `.trellis/tasks/<task-name>.md` with goal, design notes, implementation checklist, and acceptance criteria.
Do not commit or push.
After implementation, run the smallest relevant verification command and report failures honestly.
```

## 为什么适合委托

执行 Agent 可以把上下文花在项目扫描、任务文档更新、代码实现、测试修复循环上。

Codex 保留高层意图、边界控制和最终 review 上下文。
