# 示例：测试失败循环修复

## 场景

用户让 Codex 修复失败测试。日志很长，可能需要多轮读日志、定位、修复、再跑测试。

## Codex 应该怎么做

1. 识别失败命令和大致范围。
2. 把日志阅读和迭代修复委托给执行 Agent。
3. 要求执行 Agent 报告每个验证命令和最终结果。
4. Codex 最后 review diff，判断修复是否最小、是否有越界改动。

## Brief 片段

```markdown
Task: Fix the failing tests from `<command>`.
Focus only on the failure surfaced by this command. Do not refactor unrelated code.
Run the command after changes. If failures remain, report the exact failing test and your best root-cause hypothesis.
```

## Review 重点

- 修复是否聚焦？
- 测试是否真的重跑？
- 执行 Agent 是否隐藏或泛化了剩余失败？
