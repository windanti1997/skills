---
name: agent-cli-delegation-partner
description: Use when Codex expects a task to consume long context or many tokens, especially broad code implementation, reading many files, maintaining task/spec/plan docs, running test-fix loops, reviewing large diffs, or when the user asks Codex to delegate work to Mimo, MimoCode, or another agent CLI. Codex should remain the accountable decision-maker: clarify scope, detect the project workflow, prepare a bounded delegation brief, invoke an appropriate agent CLI when available, then review and verify the result before reporting back.
---

# Agent CLI Delegation Partner

## Purpose

This skill defines a reusable delegation protocol for Codex.

Codex should not carry every long-context implementation loop in the main conversation. When a task is broad, repetitive, log-heavy, or likely to pollute the current context, Codex may delegate execution to a command-line agent while keeping ownership of intent, scope, tradeoffs, review, verification, and final communication.

Mimo and MimoCode are examples of compatible agent CLIs, not hard dependencies. This skill must remain usable with any CLI agent that can receive a bounded prompt, work in a target workspace, and return structured results.

## When to Use

Use this skill when one or more of these are true:

- The task is likely to consume long context: broad implementation, large refactor, many files, long docs, large logs, or large diffs.
- The user asks to delegate to Mimo, MimoCode, another agent, or an external coding agent.
- The task involves creating or updating project task artifacts such as Trellis tasks, Superpowers materials, specs, plans, implementation notes, or design docs.
- The task is an implementation/test-fix loop that may require repeated execution and log reading.
- The task needs a large review pass after another agent modifies the workspace.

Do not use this skill for ordinary short answers, simple one-file edits, small explanations, or low-cost local fixes.

## Core Rule

Codex may delegate execution, but Codex may not delegate responsibility.

Before delegation, Codex must make the task narrow enough to execute. After delegation, Codex must inspect evidence and decide whether the result is acceptable.

Never treat an executor's "done" message as sufficient proof.

## Workflow Detection

Before writing the delegation brief, inspect the project for existing workflow conventions. Prefer project-local rules over this generic skill.

Look for, in this order:

1. Repository guidance: `AGENTS.md`, `CLAUDE.md`, `README.md`, `.cursor/rules/`, `.windsurfrules`, or other explicit agent instructions.
2. Trellis: `.trellis/`, `.trellis/tasks/`, Trellis workflow/spec files.
3. Superpowers-style guidance: files or directories that mention `superpower`, `superpowers`, `using-superpowers`, `use-superpowers`, skill packs, or command/workflow docs that tell the agent how to operate.
4. Spec/plan workflows: `spec.md`, `SPEC.md`, `plan.md`, `PLAN.md`, `design.md`, `implementation.md`, `tasks.md`, `docs/specs/`, `docs/plans/`, `.kiro/specs/`, or equivalent.
5. Test/build conventions: package manager files, CI config, Makefile, task runner files, or documented verification commands.

If a workflow exists, ask the delegated agent to update the appropriate workflow artifact before implementation, unless the user explicitly says not to. Do not force Trellis on projects that use another system.

## Delegation Boundary

Delegate work that is mechanical, broad, or context-heavy:

- reading and summarizing many files;
- creating or updating task/spec/plan artifacts;
- implementing bounded changes;
- generating tests;
- running local checks and iterating on failures;
- producing structured change summaries.

Keep these with Codex:

- clarifying ambiguous user intent;
- choosing architecture and tradeoffs when not obvious;
- deciding scope and non-goals;
- reviewing final diffs;
- interpreting test failures that imply product/design decisions;
- final user-facing explanation and risk disclosure.

## Agent CLI Selection

Use an available CLI execution agent. Do not hardcode one agent as required.

Recommended selection order:

1. If the user named an agent CLI, use that.
2. If project docs specify a preferred agent CLI, use that.
3. If a compatible known CLI such as `mimo` or `mimocode` is available, use it as a convenient default.
4. If another configured agent CLI is available, adapt the command using `scripts/delegate-agent.py --command-template`.
5. If no suitable CLI is available, do not fake delegation. Prepare the brief and execute locally as Codex, or tell the user what is missing.

A usable agent CLI must support the practical equivalent of:

- running in or against a workspace directory;
- receiving a bounded prompt;
- reading/writing project files when authorized;
- running verification commands when authorized;
- returning a summary, verification result, and risk list.

## Environment Handling

Do not assume PowerShell, Bash, zsh, Linux, macOS, or Windows.

Before giving shell-specific commands to a delegated agent or script:

- infer the current shell and OS from the tool environment when possible;
- prefer cross-platform scripts from this skill when useful;
- when shell syntax is unavoidable, state the detected shell and keep commands compatible with it;
- do not hardcode `export`, `source`, `$env:`, path separators, or shell quoting rules unless that environment is known.

The helper scripts in `scripts/` are Python-based to reduce shell assumptions.

## Delegation Brief Requirements

Every delegated task must be passed as a narrow brief containing:

- workspace path;
- one focused task;
- background and user intent;
- discovered project workflow, such as Trellis, Superpowers, spec, plan, or none;
- files or directories likely relevant;
- explicit non-goals;
- acceptance criteria;
- verification commands to run, or instructions to discover the minimal verification command;
- constraints: no automatic commit, push, PR, destructive cleanup, unrelated formatting, or rollback of user changes unless explicitly authorized;
- required output format: summary, changed files, verification result, risks, follow-up recommendations.

Use `references/delegation-brief-template.md` as the canonical structure.

## Optional Helper Scripts

Use scripts only when they improve reliability. Do not call them blindly.

- `scripts/delegate-agent.py`: cross-platform wrapper for invoking Mimo, MimoCode, or any compatible agent CLI from a prompt file. It supports presets, custom command templates, dry-run mode, and log capture.
- `scripts/collect-review-context.py`: gathers concise git status, changed file names, diff stats, recent commits, and optional capped diffs so Codex can review delegated work with less noise.

These scripts are runtime helpers for Codex while using the skill. They are not installation, packaging, or marketing scripts.

## Default Delegation Flow

1. Understand the user request and decide whether delegation is justified.
2. Inspect repository instructions and workflow artifacts.
3. Define target, non-goals, acceptance criteria, and minimal verification.
4. Write a delegation brief, usually in a temporary file or a project task/spec file if the workflow expects one.
5. Select an agent CLI. Prefer the named agent, project default, a compatible known preset, or a custom command template.
6. Run the delegated agent, preferably through `scripts/delegate-agent.py` for logging and portability.
7. When it finishes, inspect `git status`, key diffs, updated workflow docs, and verification output.
8. If the result is wrong or incomplete, either delegate a narrower repair brief or make a small local fix.
9. Report what changed, what was verified, what remains risky, and whether the result should be accepted.

## Review Checklist

Codex must review at least these points after delegation:

- Does the result satisfy the original user intent and acceptance criteria?
- Did the delegated agent update the correct Trellis/Superpowers/spec/plan artifacts when the project uses them?
- Did it expand scope, reformat unrelated files, or rewrite architecture without approval?
- Did it preserve user changes and avoid destructive actions?
- Are tests, builds, or static checks meaningful for the change?
- Are failures explained rather than hidden?
- Are generated docs consistent with code?
- Is there any security, migration, data compatibility, permission, or rollback risk?
- Is another delegation pass needed, or is a small Codex-side fix safer?

## Replacement Agent CLI Contract

To replace the default executor, define an adapter command that accepts three logical inputs:

- `{workspace}`: absolute or relative project path;
- `{title}`: short task title;
- `{prompt_file}` or `{prompt}`: delegation brief.

Examples:

```text
mimo run --dir {workspace} --title {title} {prompt}
```

```text
other-agent run --cwd {workspace} --task-file {prompt_file}
```

```text
custom-agent "{prompt}"
```

Prefer `{prompt_file}` over inline `{prompt}` when the target CLI supports file input because it avoids shell quoting problems and preserves formatting. Use `--command-template` to adapt any compatible CLI.

## Memory Boundary

This skill defines a reusable cross-project delegation protocol. Project-specific decisions belong in the target repository's own instructions, tasks, specs, or plans. Do not write temporary project decisions into this global skill.
