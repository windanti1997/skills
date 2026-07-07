# 示例：Trellis 项目里的大功能实现

## 场景

用户让 Codex 实现一个跨多个模块的新功能。仓库里存在 `.trellis/tasks/` 和 `.trellis/scripts/task.py`。

## 问题案例

错误 brief：

```text
按 Trellis 约定实现这个任务，task.json 状态由 Codex 决定。
```

这个写法会导致执行 Agent 只把 Trellis 文档当资料读，甚至使用自己的内部 task 系统。结果可能是：代码改了，但 Trellis task 仍停留在 planning，`implement.md` 没记录执行过程。

## 正确委托

Codex 应该明确：

1. 哪个 `.trellis/tasks/...` 是权威任务。
2. 是否允许执行 Agent 调用 `.trellis/scripts/task.py start/finish/archive`。
3. 如果状态流转由 Codex 保留，执行 Agent 仍必须更新 `implement.md` 执行记录。
4. 明确禁止执行 Agent 使用自己的内部 task 系统替代 Trellis。
5. 执行完成后，Codex 同时检查 Trellis 状态、`implement.md`、代码 diff 和验证结果。

## Brief 片段：Codex 控制状态流转

```markdown
Project workflow detected: Trellis.
Authoritative Trellis task: `.trellis/tasks/T1-route-b-first-cut/`.
State transition owner: Codex.
Delegated agent must not change `task.json` state and must not mark the task complete.
Delegated agent must update `.trellis/tasks/T1-route-b-first-cut/implement.md` with implementation steps, changed files, verification commands, results, and remaining risks.
Delegated agent must not use its own internal task system as a substitute for Trellis.
Do not commit or push.
```

## Brief 片段：执行 Agent 被授权做状态流转

```markdown
Project workflow detected: Trellis.
Authoritative Trellis task: `.trellis/tasks/T1-route-b-first-cut/`.
State transition owner: delegated agent.
Use the repository Trellis command, not your internal task system:

```text
python .trellis/scripts/task.py start T1-route-b-first-cut
```

After implementation and verification, update `implement.md` with execution records. Only run the documented finish command if all acceptance criteria pass.
Do not commit or push.
```

## Review 重点

- `task.json` 状态和预期一致吗？
- `implement.md` 是否记录了这次执行？
- 执行 Agent 是否绕开 Trellis 使用了自己的 task 系统？
- 代码 diff 是否和 Trellis task 的 PRD/design/implement 一致？
- 验证命令是否真的跑过？
