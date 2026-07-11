---
name: route-lock-guardian
description: Use this skill for any long-running project before planning, continuing, implementing, reviewing, dogfooding, or releasing work when product direction, architecture boundaries, user journey, automation authority, or agent-executed tasks could drift from the intended route. It creates and enforces route-lock contracts, killed-route records, authority matrices, workflow-event policies, and route-level review gates so future agents cannot locally complete tasks while globally violating the project direction.
---

# Route Lock Guardian

## Purpose

Prevent route drift in long-running projects.

A project drifts when tasks are locally completed but the final system no longer matches the intended product route, architecture boundary, user journey, safety boundary, or business goal.

This skill turns project direction into durable repo-level contracts, task gates, review gates, and drift checks.

Core rule:

```text
Do not rely on conversation memory to preserve project direction.
Put the route into files, templates, review gates, and tests.
```

---

## When to Use This Skill

Use this skill before any task that affects:

- product direction
- user onboarding or daily workflow
- architecture boundaries
- installation or setup flow
- workflow ownership
- lifecycle state
- automation hooks
- background jobs
- persistence or memory
- generated rules or policies
- approval / auto-approval behavior
- release readiness
- dogfood readiness
- any project where agents may keep implementing after context has thinned

Also use this skill when the user says or implies:

- “做完才发现不对”
- “路线又变了”
- “之前没考虑到”
- “怎么又缺斤少两”
- “过几轮你又会忘”
- “其他项目也会这样”
- “沉淀成 skill”
- “不要再反复重构路线”
- “先别写代码，重新想清楚”

---

## What This Skill Must Produce

For a project without route-lock files, create:

```text
docs/route/current-route-lock.md
docs/route/user-journey-contract.md
docs/route/non-goals-and-killed-routes.md
```

For a project with automation, agents, hooks, approvals, generated state, persistent memory, or workflow ownership, also create:

```text
docs/route/architecture-boundary-contract.md
docs/route/authority-matrix.md
docs/route/workflow-event-policy.md
docs/route/dogfood-readiness-gate.md
docs/route/release-readiness-gate.md
docs/route/route-drift-review-checklist.md
```

Use the templates in `templates/`.

---

## Required Procedure Before Implementation

Before implementing or continuing a task:

1. Read existing `docs/route/*.md` files.
2. Identify the current route, killed routes, affected user journey, affected authority level, and affected workflow event.
3. Write a Route Alignment Note using `templates/route-alignment-note-template.md`.
4. Define route-level acceptance criteria.
5. Only then modify code, docs, prompts, workflows, hooks, or configuration.

If route files are missing, create a minimal route lock first. Do not proceed on a high-impact implementation task with only conversation memory as the source of truth.

---

## Route Alignment Note Requirements

Every implementation or review task must include:

```text
Route Files Read:
- docs/route/current-route-lock.md
- docs/route/user-journey-contract.md
- docs/route/non-goals-and-killed-routes.md

What This Task Is Allowed To Change:
...

What This Task Must Not Change:
...

User Journey Affected:
...

Authority Level Affected:
...

Workflow Event Affected:
...

Killed Routes To Avoid:
...

Route-Level Acceptance Criteria:
...

Drift Risks:
...

Mitigations:
...
```

If this note cannot be written clearly, stop and clarify or create the missing route contract.

---

## Mandatory Review Gates

A task is not complete just because code builds and tests pass.

Review every task through four gates:

### Gate 1: Route Consistency

Does the change preserve `current-route-lock.md`?

### Gate 2: User Journey

Does the user still get the intended first-time flow, daily flow, interruption budget, and degraded-mode behavior?

### Gate 3: Authority Safety

Did any actor, hook, agent, automation, model, generated artifact, or background job write or activate state at a higher authority level than allowed?

### Gate 4: Killed Route Regression

Did the change reintroduce any abandoned route through code, default config, docs, generated instructions, hook behavior, tests, prompts, naming, or status messages?

If any gate fails, the task must not be marked complete.

---

## Authority Policy Pattern

Use an authority matrix whenever a system can store rules, memories, preferences, configurations, permissions, workflow decisions, generated instructions, or persistent state.

Default pattern:

```text
L0 evidence / log / artifact
L1 observed fact
L2 candidate / proposal
L3 active user-approved rule
L4 active auto-accepted low-risk fact
L5 team / spec / organizational rule
L6 quarantined / rejected item
```

Auto-accept is allowed only when all are true:

```text
- low risk
- narrow scope
- explicit evidence
- reversible
- expiry or TTL exists
- does not control future behavior strongly
```

Auto-accept is forbidden for:

```text
- user preference
- behavior rule
- safety rule
- permission rule
- lifecycle transition
- team/spec rule
- model inference without evidence
- anything containing strong control language such as always, never, must, skip, bypass, delete, ignore
```

---

## Workflow Event Policy Pattern

For systems with hooks, agents, automation, CI, lifecycle events, or background processing, define each event with:

```text
can_read
can_write
can_suggest
can_block
can_ask_user
can_create_candidate
can_create_active_state
must_not_do
failure_behavior
```

Default safe pattern:

```text
Start/session events:
- may load context
- may inject advisory context
- must not execute hidden work by default

Pre-action events:
- may warn
- may record evidence
- must not block unless guard mode is explicitly enabled

Post-action events:
- may record evidence
- may create candidates
- must not create high-authority active state by default

User-response events:
- may parse explicit approval
- may activate only the approved item

Stop/finalization events:
- may summarize
- may produce a review digest
- must not run expensive or hidden workflows by default
```

---

## User Confirmation Cost Pattern

Do not ask the user to approve every candidate one by one.

Use:

```text
- automatic evidence logging
- low-risk observed-fact auto-accept under authority policy
- batch review for behavior rules, preferences, and durable decisions
- quarantine for high-risk items
- explicit approval for durable or high-authority state
```

Default interruption budget:

```text
max_prompts_per_session: 1
max_items_per_prompt: 5
batch_on_stop: true
```

---

## Killed Route Handling

Every abandoned direction must be recorded in `docs/route/non-goals-and-killed-routes.md`.

For each killed route, record:

```text
- what it was
- why it was killed
- where it previously appeared
- forbidden resurrection signals
- guard tests or review checks
```

Killed routes commonly reappear through:

```text
- generated instructions
- old default config
- CLI help text
- hook status messages
- test fixtures
- examples
- templates
- docs
- fallback paths
- “temporary” compatibility code
```

Search these surfaces during review.

---

## Drift Smells

Treat these as warnings:

```text
- “Tests pass” but no user journey was simulated
- default config enables an old behavior
- generated instructions mention a killed route
- hook silently writes durable state
- verifier or checker mutates lifecycle state
- user must understand internal modules to complete setup
- task says complete while core acceptance is deferred
- auto-accept exists without authority classification
- a new mode is added without route docs
- docs and runtime disagree about ownership or lifecycle
```

See `references/drift-smells.md`.

---

## Scripts

This skill includes two optional helper scripts.

Initialize route-lock docs:

```bash
python scripts/init_route_lock.py <project-root> --minimal
python scripts/init_route_lock.py <project-root> --full
```

Check for missing route files and common drift smells:

```bash
python scripts/check_route_drift.py <project-root>
```

The scripts are helpers only. The route contracts and review gates remain the source of truth.

---

## Standard Review Output

Use this format:

```text
结论：通过 / 不通过 / 部分通过

Route Consistency:
...

User Journey:
...

Authority Safety:
...

Killed Route Regression:
...

Blocking Issues:
1. ...
2. ...

Required Fix:
...

Repair Prompt:
...
```

---

## Non-Negotiable Rule

Never treat local task completion as proof of product correctness.

A task is complete only when:

```text
code passes
tests pass
route gates pass
user journey still works
authority boundaries hold
killed routes stay dead
```
