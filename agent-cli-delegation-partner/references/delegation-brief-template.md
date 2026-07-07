# 委托 Brief 模板

Codex 调用外部 Agent CLI 前，先按这个结构写清楚任务边界。

```markdown
# Delegation Brief

## Workspace

<项目工作目录，优先绝对路径>

## Task

<一个聚焦任务，不要把多个无关任务塞在一起>

## User Intent

<用户真正想要什么，为什么要做>

## Project Workflow Detected

- Repository instructions: <AGENTS.md / CLAUDE.md / README / none>
- Workflow artifact: <Trellis / Superpowers / spec / plan / other / none>
- Required workflow update: <执行 Agent 需要先更新或遵循什么文档/流程>

## Relevant Context

- <已经确认相关的文件、目录、命令、文档>
- <用户明确给过的约束>
- <项目规则里的关键要求>

## Non-goals

- <明确不要做的事情>
- Do not commit, push, create PRs, or roll back unrelated user changes unless explicitly authorized.
- Do not reformat unrelated files.
- Do not introduce broad architecture changes unless required by the brief.

## Acceptance Criteria

- <可观察验收标准 1>
- <可观察验收标准 2>
- <文档/spec/task 更新要求>
- <验证要求>

## Verification

Run the minimal relevant checks, or discover and explain the best available checks.

Suggested commands:

```text
<command 1>
<command 2>
```

## Output Required

Return:

1. Summary of changes.
2. Files changed.
3. Verification commands and results.
4. Risks or incomplete items.
5. Recommended next action.
```
