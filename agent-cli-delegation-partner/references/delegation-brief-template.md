# 委托 Brief 模板

Codex 调用外部 Agent CLI 前，先按这个结构写清楚任务边界。不要只写“按项目约定执行”，要把状态流转、执行记录、验证责任写明白。

```markdown
# Delegation Brief

## Workspace

<项目工作目录，优先绝对路径>

## Detected Environment

- OS: <Windows / macOS / Linux / unknown>
- Shell: <PowerShell / cmd / bash / zsh / unknown>
- Path style: <Windows / POSIX>
- Shell notes: <不要使用不适配当前 shell 的 export/source/$env 等语法>

## Task

<一个聚焦任务，不要把多个无关任务塞在一起>

## User Intent

<用户真正想要什么，为什么要做>

## Project Workflow Detected

- Repository instructions: <AGENTS.md / CLAUDE.md / README / none>
- Workflow artifact: <Trellis / Superpowers / spec / plan / other / none>
- Authoritative workflow files: <具体路径>
- Required workflow update: <执行 Agent 需要先更新或遵循什么文档/流程>

## Trellis Responsibilities

仅在项目使用 Trellis 时填写；否则写 N/A。

- Authoritative task: <.trellis/tasks/...>
- Trellis command: <python .trellis/scripts/task.py ... 或项目文档里的等价命令>
- State transition owner: <Codex / delegated agent>
- Allowed state transitions: <none / start only / start+finish / other>
- Execution record file: <implement.md 或项目等价文件>
- Required record update: <实现步骤、验证结果、剩余风险>
- Internal task systems: Do not use the executor's own internal task system as a substitute for Trellis.

如果 state transition owner 是 Codex，执行 Agent 仍然必须更新 implementation/execution record，不能只改代码。

## Relevant Context

- <已经确认相关的文件、目录、命令、文档>
- <用户明确给过的约束>
- <项目规则里的关键要求>

## Non-goals

- <明确不要做的事情>
- Do not commit, push, create PRs, or roll back unrelated user changes unless explicitly authorized.
- Do not reformat unrelated files.
- Do not introduce broad architecture changes unless required by the brief.
- Do not use your own internal task system when the project workflow already has an authoritative task system.

## Acceptance Criteria

- <可观察验收标准 1>
- <可观察验收标准 2>
- <文档/spec/task 更新要求>
- <Trellis 状态/执行记录要求>
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
3. Workflow artifacts updated.
4. Trellis state and implementation record status, if applicable.
5. Verification commands and results.
6. Risks or incomplete items.
7. Recommended next action.
```
