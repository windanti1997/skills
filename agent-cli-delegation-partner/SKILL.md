---
name: agent-cli-delegation-partner
description: Use when Codex expects a task to consume long context or many tokens, especially broad code implementation, reading many files, maintaining task/spec/plan docs, running test-fix loops, reviewing large diffs, or when the user asks Codex to delegate work to Mimo, MimoCode, or another agent CLI. Codex remains accountable: clarify scope, detect workflow, prepare a bounded delegation brief, invoke an appropriate agent CLI, then review workflow state, implementation records, diffs, and verification before reporting back.
---

# Agent CLI Delegation Partner

## Purpose

This skill defines a reusable delegation protocol for Codex.

Codex may delegate long-context execution to a command-line agent, but Codex keeps ownership of user intent, scope, tradeoffs, review, verification, and final communication.

Mimo and MimoCode are compatible examples, not required dependencies. Any CLI agent can be used if it can receive a bounded prompt, work in a target workspace, and return structured results.

## Core Rule

Codex may delegate execution, but Codex may not delegate responsibility.

Before delegation, Codex must make the task narrow enough to execute. After delegation, Codex must inspect evidence and decide whether the result is acceptable.

Never treat an executor's "done" message as sufficient proof.

## When to Use

Use this skill when one or more are true:

- broad implementation, large refactor, many files, long docs, large logs, or large diffs;
- user asks to delegate to Mimo, MimoCode, another agent, or another coding CLI;
- task involves Trellis, Superpowers, spec, plan, implementation notes, or design docs;
- task is a test-fix loop with repeated execution and log reading;
- task needs a large review pass after another agent modifies the workspace.

Do not use this skill for short answers, simple one-file edits, small explanations, or low-cost local fixes.

## Skill Discovery

Codex should proactively look for relevant skills in project-local locations and common user/global locations such as `~/.codex/skills/`, especially when `AGENTS.md` or repository docs mention skill paths.

## Workflow Detection

Before writing a delegation brief, inspect project-local rules first:

1. `AGENTS.md`, `CLAUDE.md`, `README.md`, `.cursor/rules/`, `.windsurfrules`, or equivalent agent instructions.
2. Trellis: `.trellis/`, `.trellis/tasks/`, `.trellis/scripts/task.py`.
3. Superpowers-style guidance: files or docs mentioning `superpower`, `superpowers`, or similar workflow rules.
4. Spec/plan workflows: `spec.md`, `plan.md`, `design.md`, `implementation.md`, `tasks.md`, `docs/specs/`, `docs/plans/`, `.kiro/specs/`.
5. Test/build conventions from package manager files, CI config, Makefiles, or docs.

Use `references/workflow-detection.md` for detailed handling.

## Trellis Delegation Contract

If Trellis is detected, do not merely tell the executor to "follow Trellis". The brief must explicitly name:

- the authoritative Trellis task path;
- whether the delegated agent may run `.trellis/scripts/task.py` state commands;
- whether `task.json` state transitions are owned by Codex or the delegated agent;
- which `implement.md` or equivalent execution record must be updated;
- that the executor's own internal task system must not replace Trellis.

Default policy:

- Codex owns final state decisions unless the brief says otherwise.
- The delegated agent may update implementation records such as `implement.md`.
- The delegated agent must not mark Trellis complete unless explicitly authorized.
- If the brief authorizes state transitions, require the repository Trellis command rather than the executor's internal task tool.

Codex review must check Trellis state, execution record, code diff, and verification together. Code implemented while Trellis remains in planning is not an acceptable final state unless Codex intentionally deferred the state transition and reports that clearly.

## Delegation Boundary

Delegate broad or mechanical work:

- reading and summarizing many files;
- creating or updating task/spec/plan artifacts;
- implementing bounded changes;
- generating tests;
- running local checks and iterating on failures;
- producing structured change summaries.

Keep these with Codex:

- user intent clarification;
- architecture and tradeoff decisions when not obvious;
- scope and non-goal decisions;
- final acceptance;
- final diff review;
- final user-facing explanation and risk disclosure.

## Agent CLI Selection

Recommended order:

1. user-named agent CLI;
2. project-specified agent CLI;
3. known compatible preset such as `mimo` or `mimocode`;
4. custom command via `scripts/delegate-agent.py --command-template`;
5. if none is available, do not fake delegation.

A usable CLI should run against a workspace, receive a bounded prompt, operate within authorization, run useful verification, and return summary, verification, and risks.

## Environment Handling

Do not assume PowerShell, Bash, zsh, Linux, macOS, or Windows.

The delegation brief must include detected OS/shell when known. Shell-specific syntax should only be used after the environment is known.

`scripts/delegate-agent.py` is Python-based and supports Windows `.cmd`/`.bat` launchers, real-time output, log capture, dry-run mode, and background mode.

## Delegation Brief Requirements

Every delegated task must include:

- workspace path;
- detected OS and shell;
- one focused task;
- user intent;
- detected workflow and workflow-specific responsibilities;
- relevant files/directories;
- non-goals;
- acceptance criteria;
- verification commands or discovery instructions;
- output format covering summary, changed files, workflow artifacts updated, verification result, risks, and next action.

Use `references/delegation-brief-template.md` as the canonical template.

## Review Checklist

After delegation, Codex must review:

- original intent and acceptance criteria;
- Trellis/Superpowers/spec/plan artifacts when used;
- for Trellis: `task.json` state, `implement.md` or equivalent execution record, and code diff consistency;
- whether the executor used its own task system instead of the project workflow;
- scope expansion or unrelated formatting;
- preservation of user changes;
- verification quality and pre-existing failures;
- security, migration, data compatibility, permission, and rollback risks.

Then Codex must choose: accept, delegate a narrower repair, make a small local fix, or ask the user because the remaining issue is a product/architecture decision.

## Replacement Agent CLI Contract

Adapter commands can use:

- `{workspace}`: project path;
- `{title}`: short task title;
- `{prompt_file}` or `{prompt}`: delegation brief.

Prefer `{prompt_file}` when the CLI supports it.

For CLIs implemented with yargs or similar parsers, place positional arguments before repeatable array flags such as `-f`, or use `--` to separate CLI options from task arguments.

## Memory Boundary

This skill defines a reusable cross-project delegation protocol. Project-specific decisions belong in the target repository's own instructions, tasks, specs, or plans.
