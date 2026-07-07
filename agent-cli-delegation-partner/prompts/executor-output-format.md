# 执行 Agent 输出格式

Codex 应要求执行 Agent 在结束时使用这个结构输出：

```markdown
## Summary

<what changed>

## Files Changed

- <path>: <short reason>

## Workflow Artifacts Updated

- <path or none>: <what was updated>

## Trellis State / Implementation Record

<Trellis task state, implement.md update, task.py commands used, or N/A>

## Verification

- `<command>`: <passed/failed/skipped and why>

## Risks / Incomplete Items

- <risk or none>

## Recommended Next Step

<accept / review specific files / run specific command / delegate follow-up>
```
