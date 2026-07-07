# 示例：项目使用 Superpowers / using-superpowers

## 场景

仓库中存在 `using-superpowers` 或类似 Superpowers 风格的工作流说明。

## Codex 应该怎么做

1. 先阅读项目里的 workflow guidance。
2. 不要强行套 Trellis。
3. 把发现的 Superpowers 指令写进 delegation brief。
4. 要求执行 Agent 按项目 workflow 先完成必要 plan/checklist/skill invocation。
5. Codex 最后检查执行 Agent 是否真的遵守了该 workflow。

## Brief 片段

```markdown
Project workflow detected: Superpowers-style guidance.
Follow the repository's `using-superpowers` instructions exactly. If that workflow requires a plan/checklist/skill invocation before coding, do that first.
Do not replace this with Trellis unless the repository explicitly requires both.
```

## Review 重点

- 执行 Agent 是否遵守了仓库自己的 agent workflow？
- 是否生成了 workflow 要求的 plan / checklist / artifact？
- 实现是否和这些 artifact 一致？
