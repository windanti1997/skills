# 示例：项目使用 spec / plan 工作流

## 场景

仓库有 `docs/specs/checkout.md` 和 `docs/plans/checkout-plan.md`，但没有 Trellis。

## Codex 应该怎么做

1. 先读相关 spec 和 plan。
2. 要求执行 Agent 只有在行为变化时才更新对应文档。
3. brief 保持短而具体。
4. 执行完成后，Codex 检查代码和文档是否一致。

## Brief 片段

```markdown
Project workflow detected: spec/plan docs.
Read `docs/specs/checkout.md` and `docs/plans/checkout-plan.md` before coding.
If behavior changes, update the relevant spec/plan section. Do not create Trellis files.
```

## Review 重点

- 代码是否符合 spec？
- 执行 Agent 是否避免发明新流程？
- plan 更新是否具体，并且能追溯到代码变化？
