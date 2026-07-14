# Development Workflow (Multi-Scenario)

---

## Core Principles

1. **Plan before code** - figure out what to do before you start
2. **Specs injected, not remembered** - guidelines are injected via hook/skill, not recalled from memory
3. **Persist everything** - research, decisions, and lessons all go to files; conversations get compacted, files don't
4. **Incremental development** - one task at a time
5. **Capture learnings** - after each task, review and write new knowledge back to spec
6. **Scenario-aware routing** - identify the work scenario (long-term task / bugfix / performance optimization) before entering Phase 1, and route accordingly

---

## Trellis System

### Developer Identity

On first use, initialize your identity:

```bash
python ./.trellis/scripts/init_developer.py <your-name>
```

### Spec System

`.trellis/spec/` holds coding guidelines organized by package and layer.

### Task System

Every task has its own directory under `.trellis/tasks/{MM-DD-name}/` holding `task.json`, `prd.md`, optional `design.md`, optional `implement.md`, optional `research/`, and context manifests (`implement.jsonl`, `check.jsonl`).

```bash
python ./.trellis/scripts/task.py create "<title>" [--slug <name>] [--parent <dir>]
python ./.trellis/scripts/task.py start <name>
python ./.trellis/scripts/task.py finish
python ./.trellis/scripts/task.py archive <name>
```

---

## Scenario Routing

Before entering Phase 1, identify the work scenario. This determines which steps to run and which skills to load.

### Scenario Identification

When the user describes a task, classify it into one of three scenarios. **Always confirm with the user before proceeding.**

| Scenario | Trigger signals | Key skills |
|----------|----------------|-------------|
| **Long-term task** | New feature, large requirement, multi-session work | `anti-overfit-collaboration`, `route-lock-guardian`, `brainstorming`, `grill-me`, `trellis-task-contract`, `TDD` |
| **Bugfix** | Bug, error, something broken, unexpected behavior | `diagnosing-bugs`, `TDD` |
| **Performance optimization** | Slow, lag, memory, optimization needed | `research`, `grill-me`, `TDD` |

### Scenario Confirmation Rule

After identifying the scenario, explicitly tell the user:

> "This looks like a [scenario] task. Confirm? (If wrong, tell me the correct scenario)"

Once confirmed, the scenario is recorded in `prd.md` as a frontmatter field:

```markdown
---
scenario: long-term-task | bugfix | perf-optimization
---
```

### Scenario Switch Rule

If the scenario turns out to be wrong mid-flight, **do not switch mid-task**. Run `/trellis:finish-work` to close the current task, then start a new session with the correct scenario.

---

## Phase Index

```
Phase 1: Plan    -> identify scenario, clarify requirements, produce planning artifacts
Phase 2: Execute -> implement (scenario-specific), then check (scenario-specific verify)
Phase 3: Finish  -> scenario-specific retrospective, spec update, commit, and wrap up
```

### Request Triage

- Simple conversation or small task: ask only whether this turn should create a Trellis task. If the user says no, skip Trellis for this session.
- Complex task: ask whether you may create a Trellis task and enter planning. If the user says no, do not do broad inline implementation; explain, clarify scope, or suggest a smaller split.
- **Scenario identification**: before creating a task, identify the scenario (long-term-task / bugfix / perf-optimization) and confirm with the user.
- User approval to create a task is not approval to start implementation. Planning still happens first.

### Planning Artifacts

- `prd.md` - requirements, constraints, and acceptance criteria. Includes `scenario` frontmatter.
- `design.md` - technical design for complex tasks: boundaries, contracts, data flow, tradeoffs.
- `implement.md` - execution plan: ordered checklist, validation commands, review gates.
- `implement.jsonl` / `check.jsonl` - spec and research manifests for sub-agent context.
- Lightweight tasks may be PRD-only. Complex tasks must have `prd.md`, `design.md`, and `implement.md` before `task.py start`.

---

<!-- Per-turn breadcrumb: shown when there is no active task (before Phase 1) -->

[workflow-state:no_task]
No active task. First classify the current turn, identify the scenario (long-term-task / bugfix / perf-optimization), confirm with the user, then ask for task-creation consent.
Simple conversation / small task: ask only whether this turn should create a Trellis task. If the user says no, skip Trellis for this session.
Complex task: ask the user if you can create a Trellis task and enter the planning phase. If the user says no, explain, clarify scope, or suggest a smaller split.
[/workflow-state:no_task]

---

### Phase 1: Plan

Phase 1 behavior depends on the identified scenario. Each scenario has a different sub-flow.

#### Scenario A: Long-term Task

- 1.0 Create task `[required · once]` (only after task-creation consent)
- 1.1 Intent clarification `[required · repeatable]`
  - Load `anti-overfit-collaboration` skill to identify the user's real intent and prevent recency-bias overfitting
  - Write the clarified intent into `prd.md` as "Real Intent" section
- 1.2 Route locking `[required · once]`
  - Load `route-lock-guardian` skill to lock the long-term goal
  - Produce `docs/route/route-lock.md`, `docs/route/non-goals-and-killed-routes.md`
  - Write Route Alignment Note into `prd.md`
- 1.3 Requirement exploration `[required · repeatable]`
  - Load `brainstorming` skill (replaces `trellis-brainstorm` for this scenario)
  - Explore requirements interactively, produce `prd.md`, `design.md`, `implement.md`
  - For complex tasks, produce all three artifacts before implementation
- 1.4 Stress-test `[optional · repeatable]`
  - Load `grill-me` skill to stress-test the plan
  - One question at a time, wait for user response
  - If critical issues found, return to 1.3 and revise
  --- HUMAN CHECKPOINT: user answers grill questions ---
- 1.5 Task contract `[required · once]`
  - Load `trellis-task-contract` skill to generate anti-MVP acceptance criteria
  - Write into `prd.md` (acceptance criteria, non-goals) and `implement.md` (prohibited downgrades, checkpoints, evidence plan)
- 1.6 Stress-test contract `[optional · once]`
  - Load `grill-me` skill to check if acceptance criteria can be escaped
  --- HUMAN CHECKPOINT: user confirms criteria ---
- 1.7 Task decomposition `[required · once]`
  - Decompose into tracer-bullet vertical slices (each slice spans all layers, independently verifiable)
  - Declare blocking edges between slices
  - Group into Batch 1 (infrastructure, sequential) / Batch 2 (parallel) / Batch 3 (integration, sequential)
  - Write batch plan into `implement.md`
- 1.8 Test design `[required · once]`
  - Load `TDD` skill to identify test seams and write test plan
  - Confirm each slice has an independent test boundary
- 1.9 Configure context `[required · once]`
  - Curate `implement.jsonl` and `check.jsonl` (sub-agent platforms only)
- 1.10 Activate task `[required · once]`
  - Review gate, then `task.py start`; status -> in_progress

#### Scenario B: Bugfix

- 1.0 Create task `[required · once]` (only after task-creation consent)
- 1.1 Diagnosis `[required · repeatable]`
  - Load `diagnosing-bugs` skill for scientific diagnosis: hypothesis -> instrumentation -> reproduce -> analyze
  - If environment-dependent bug: ask user for reproduction steps
  - Write diagnosis findings into `{TASK_DIR}/research/diagnosis.md`
- 1.2 Code localization `[required · once]`
  - Dispatch `trellis-research` sub-agent to locate relevant code
  - Write findings into `{TASK_DIR}/research/`
- 1.3 Configure context `[required · once]`
  - Curate `implement.jsonl` and `check.jsonl` (sub-agent platforms only)
- 1.4 Activate task `[required · once]`
  - Review gate, then `task.py start`; status -> in_progress

#### Scenario C: Performance Optimization

- 1.0 Create task `[required · once]` (only after task-creation consent)
- 1.1 Bottleneck localization `[required · repeatable]`
  - Dispatch `trellis-research` sub-agent for profiling
  - Frontend: Lighthouse, Chrome DevTools, `web-perf` skill
  - Android: `dumpsys meminfo`, Perfetto, hprof dump
  - Write profiling data into `{TASK_DIR}/research/profiling.md`
- 1.2 Stress-test direction `[optional · repeatable]`
  - Load `grill-me` skill to question: is this the real bottleneck? Is the optimization worth it?
  --- HUMAN CHECKPOINT: user answers grill questions ---
- 1.3 Behavior baseline `[required · once]`
  - Load `TDD` skill to confirm existing tests are green (lock current behavior)
  - Write baseline test status into `implement.md`
- 1.4 Performance baseline `[required · once]`
  - Establish benchmark data (N warmup + M measurements, median + stddev)
  - Write baseline data into `implement.md`
- 1.5 Configure context `[required · once]`
  - Curate `implement.jsonl` and `check.jsonl` (sub-agent platforms only)
- 1.6 Activate task `[required · once]`
  - Review gate, then `task.py start`; status -> in_progress

<!-- Per-turn breadcrumb: shown throughout Phase 1 (status='planning') -->

[workflow-state:planning]
Scenario: long-term-task -> Load `anti-overfit-collaboration` + `route-lock-guardian` + `brainstorming` + `grill-me` + `trellis-task-contract` + `TDD`. Stay in planning until all artifacts are ready.
Scenario: bugfix -> Load `diagnosing-bugs`. Diagnosis first, then research. Skip brainstorming, route-lock, task-contract.
Scenario: perf-optimization -> Load `research` + `grill-me` + `TDD`. Profiling first, then baseline. Skip brainstorming, route-lock, task-contract.
Lightweight: `prd.md` can be enough. Complex: finish `prd.md`, `design.md`, and `implement.md`; ask for review before `task.py start`.
[/workflow-state:planning]

<!-- Per-turn breadcrumb: shown throughout Phase 1 when codex.dispatch_mode=inline -->

[workflow-state:planning-inline]
Same scenario routing as [workflow-state:planning], but skip jsonl curation; Phase 2 reads artifacts/specs via `trellis-before-dev`.
[/workflow-state:planning-inline]

---

### Phase 2: Execute

Phase 2 behavior depends on the scenario's verify requirements.

#### 2.1 Implement `[required · repeatable]`

[Claude Code, Cursor, OpenCode, codex-sub-agent, Kiro, Gemini, Qoder, CodeBuddy, Copilot, Droid, Pi, Oh My Pi, ZCode, Reasonix, Trae]

Spawn the implement sub-agent:
- **Agent type**: `trellis-implement`
- **Task description**: Implement the reviewed task artifacts
- **Dispatch prompt guard**: MUST start with `Active task: <task path>`, then say the spawned agent is `trellis-implement` and must implement directly

For **long-term task** (parallel execution):
- Batch 1: single session, `trellis-implement` -> `[needs_ui_review]` -> `trellis-check`
- Batch 2: parallel sessions (Codex Goal + git worktree), each worktree:
  - `git worktree add ../worktree-{task-name} -b {branch-name}`
  - In each worktree session: `task.py start {task-name}` -> `trellis-implement` -> `[needs_ui_review]` -> `trellis-check`
  - After all Batch 2 tasks done: merge to main branch
- Batch 3: single session, integration + `trellis-check` + `anti-overfit-reviewer`

For **bugfix**:
- Load `TDD` skill: write a failing test that reproduces the bug first
- Then `trellis-implement` to fix the code and make the test pass

For **perf-optimization**:
- `trellis-implement` to execute optimization
- Keep existing tests green throughout

[/Claude Code, Cursor, OpenCode, codex-sub-agent, Kiro, Gemini, Qoder, CodeBuddy, Copilot, Droid, Pi, Oh My Pi, ZCode, Reasonix, Trae]

[codex-inline, Kilo, Antigravity, Devin]

1. Load `trellis-before-dev` skill to read project guidelines
2. Read task artifacts (`prd.md` -> `design.md` -> `implement.md`)
3. Implement per scenario rules (same as above)
4. Run project lint and type-check

[/codex-inline, Kilo, Antigravity, Devin]

#### 2.2 Quality check `[required · repeatable]`

Scenario-specific verify commands:

**Long-term task (with frontend):**
```yaml
verify:
  - pnpm lint
  - pnpm typecheck
  - pnpm test
  - pnpm playwright test    # screenshot regression
```

**Long-term task (with Android):**
```yaml
verify:
  - ./gradlew lint
  - ./gradlew test
  - ./scripts/android-ui-check.sh    # adb uiautomator dump + screenshot
```

**Bugfix:**
```yaml
verify:
  - pnpm test    # must include the reproduction test
```

**Performance optimization:**
```yaml
verify:
  - pnpm test              # behavior unchanged (all green)
  - pnpm benchmark          # performance comparison vs baseline
```

Spawn the check sub-agent:
- **Agent type**: `trellis-check`
- Review code changes against specs and task artifacts
- Run scenario-specific verify commands
- Auto-fix issues, re-check until green

**Final pass**: the last 2.2 must run full-scope, not just the latest chunk.

#### 2.3 UI verification checkpoint `[on demand]`

For tasks involving frontend or Android UI, after implementation and before final check:

[workflow-state:needs_ui_review]
Code implementation is done. Please verify UI in browser/simulator:
1. Open the following pages: [list key pages]
2. Check: layout, colors, interactions, responsive behavior
3. If issues found, describe them and return to 2.1
4. If UI is correct, reply "UI verified" to continue to check phase
[/workflow-state:needs_ui_review]

#### 2.4 Performance verification checkpoint `[on demand]`

For performance optimization tasks, after implementation:

[workflow-state:needs_perf_review]
Optimization is done. Performance comparison:
- Baseline: [median ± stddev from Phase 1]
- After optimization: [run benchmark and fill in]
- Improvement: [calculate delta]
If improvement is insufficient, return to 2.1. If confirmed, reply "perf verified" to continue.
[/workflow-state:needs_perf_review]

#### 2.5 Rollback `[on demand]`

- `check` reveals a prd defect -> return to Phase 1, fix `prd.md`, then redo 2.1
- Implementation went wrong -> revert code, redo 2.1
- Need more research -> research (same as Phase 1), write findings into `research/`

<!-- Per-turn breadcrumb: shown while status='in_progress' -->

[workflow-state:in_progress]
Tools: `trellis-implement` / `trellis-research` are sub-agent types. `trellis-update-spec` and `trellis-check` exist as both skill and agent; prefer Agent form for checking.
Flow: `trellis-implement` -> [needs_ui_review or needs_perf_review if applicable] -> `trellis-check` -> `trellis-update-spec` -> commit (Phase 3.4) -> `/trellis:finish-work`.
Scenario-specific verify: long-term task -> lint + typecheck + test + UI screenshots; bugfix -> test (with reproduction test); perf-optimization -> test (all green) + benchmark comparison.
Dispatch prompt starts with `Active task: <task path>`. Read context: jsonl -> `prd.md` -> `design.md` -> `implement.md`.
[/workflow-state:in_progress]

[workflow-state:in_progress-inline]
Flow: `trellis-before-dev` -> edit -> `trellis-check` -> validation -> `trellis-update-spec` -> commit (Phase 3.4) -> `/trellis:finish-work`.
Do not dispatch implement/check sub-agents in inline mode.
Scenario-specific verify: same as [workflow-state:in_progress].
[/workflow-state:in_progress-inline]

---

### Phase 3: Finish

#### 3.2 Debug retrospective `[on demand]`

**Bugfix scenario (required):** Load `trellis-break-loop` skill to classify root cause, explain why earlier fixes failed, and propose prevention.

**Long-term task / perf-optimization (optional):** If repeated debugging occurred during implementation, load `trellis-break-loop`.

#### 3.3 Spec update `[required · once]`

Load `trellis-update-spec` skill and review whether this task produced new knowledge:
- Newly discovered patterns or conventions
- Pitfalls you hit
- New technical decisions

**Bugfix scenario**: also record the bug root cause and prevention mechanism into spec.

**Perf-optimization scenario**: also record the optimization technique and benchmark data into spec.

#### 3.4 Commit changes `[required · once]`

1. `git status --porcelain` to inspect dirty state
2. `git log --oneline -5` to learn commit style
3. Classify dirty files into AI-edited vs unrecognized
4. Draft commit plan, present once, ask for one-shot confirmation
5. On confirmation: `git add` + `git commit` per batch
6. On rejection: stop, let user commit manually

Rules: no `--amend`, no push, batched plan is one prompt.

#### 3.5 Wrap-up reminder

Remind the user they can run `/finish-work` to wrap up (archive the task, record the session).

---

<!-- Per-turn breadcrumb: shown while status='completed' (currently DEAD, kept for future) -->

[workflow-state:completed]
Code committed. Run `/trellis:finish-work`; if dirty, return to Phase 3.4 first.
[/workflow-state:completed]

---

### Active Task Routing

When a user request matches one of these intents inside an active task, route first, then load the detailed phase step.

[Claude Code, Cursor, OpenCode, codex-sub-agent, Kiro, Gemini, Qoder, CodeBuddy, Copilot, Droid, Pi, Oh My Pi, ZCode, Reasonix, Trae]

- Planning or unclear requirements -> `trellis-brainstorm` (long-term task) / `diagnosing-bugs` (bugfix) / `trellis-research` (perf-optimization)
- `in_progress` implementation/check -> dispatch `trellis-implement` / `trellis-check`
- User input is vague, contains examples, or questions assumptions -> `anti-overfit-collaboration`
- Long-term project direction concern -> `route-lock-guardian`
- Need to stress-test a plan or acceptance criteria -> `grill-me`
- Generating task acceptance criteria -> `trellis-task-contract`
- Before writing code, need test-first approach -> `TDD`
- Repeated debugging -> `trellis-break-loop`; spec updates -> `trellis-update-spec`

[/Claude Code, Cursor, OpenCode, codex-sub-agent, Kiro, Gemini, Qoder, CodeBuddy, Copilot, Droid, Pi, Oh My Pi, ZCode, Reasonix, Trae]

[codex-inline, Kilo, Antigravity, Devin]

- Planning or unclear requirements -> `trellis-brainstorm` (long-term task) / `diagnosing-bugs` (bugfix) / `trellis-research` (perf-optimization)
- Before editing -> `trellis-before-dev`; after editing -> `trellis-check`
- User input is vague, contains examples, or questions assumptions -> `anti-overfit-collaboration`
- Long-term project direction concern -> `route-lock-guardian`
- Need to stress-test a plan or acceptance criteria -> `grill-me`
- Generating task acceptance criteria -> `trellis-task-contract`
- Before writing code, need test-first approach -> `TDD`
- Repeated debugging -> `trellis-break-loop`; spec updates -> `trellis-update-spec`

[/codex-inline, Kilo, Antigravity, Devin]

### Guardrails

- Task creation approval is not implementation approval; implementation waits for `task.py start` after artifact review.
- Scenario must be identified and confirmed before entering Phase 1.
- If scenario is wrong mid-flight, finish the current task and start a new session; do not switch mid-task.
- PRD-only is valid for lightweight tasks; complex tasks need `design.md` + `implement.md`.
- Planning must be persisted to task artifacts; checks must run before reporting completion.
- UI verification checkpoint (`needs_ui_review`) is mandatory for frontend/Android tasks.
- Performance verification checkpoint (`needs_perf_review`) is mandatory for performance optimization tasks.

---

## Setup Notes

This workflow template adds two custom workflow-state blocks (`needs_ui_review`, `needs_perf_review`) and scenario-based routing. To make them work fully, configure the following:

### 1. Custom Status Lifecycle Hooks

Add hooks in `.trellis/config.yaml` to write custom status values:

```yaml
hooks:
  after_start:
    # No hook needed here - status is already in_progress
  after_finish:
    # No hook needed here - finish just clears active task pointer
```

Since `needs_ui_review` and `needs_perf_review` are **intermediate states within `in_progress`** (not separate task statuses), the AI sets them by **prompting the user directly** rather than changing `task.json.status`. The `task.json.status` stays `in_progress` throughout. The workflow-state blocks serve as **reference prompts** the AI reads from `workflow.md` when it reaches that step.

### 2. `/trellis:continue` Route Table Extension

If you want `/trellis:continue` to resume at the correct checkpoint, add rows to the continue command's route table (in `.{platform}/commands/trellis/continue.md` or equivalent):

| `status` | Artifact state | Resume at |
|----------|---------------|-----------|
| `in_progress` | implementation done, UI not verified | Phase 2.3 (needs_ui_review prompt) |
| `in_progress` | implementation done, perf not verified | Phase 2.4 (needs_perf_review prompt) |

Without this extension, `/trellis:continue` will resume at Phase 2.2 (check), which is acceptable - the AI will still read the workflow.md and know to do UI/perf verification first.

### 3. Custom Skills Installation

Install the 5 custom skills to `.agents/skills/`:

| Skill | Purpose | Scenario |
|-------|---------|----------|
| `anti-overfit-collaboration` | Prevent input overfitting, clarify real intent | Long-term task |
| `route-lock-guardian` | Lock long-term goal, track killed routes | Long-term task |
| `trellis-task-contract` | Anti-MVP acceptance criteria, prevent downgrades | Long-term task |
| `diagnosing-bugs` | Scientific diagnosis: hypothesis -> instrumentation -> reproduce | Bugfix |
| `TDD` | Test-first: red-green cycle, seam identification | All scenarios |

### 4. UI Verification Scripts (Optional)

For Android UI verification, create `./scripts/android-ui-check.sh`:

```bash
#!/bin/bash
# Android UI verification script
PACKAGE=$1
adb shell uiautomator dump /sdcard/view.xml
adb pull /sdcard/view.xml ./artifacts/view.xml
adb shell screencap -p /sdcard/screen.png
adb pull /sdcard/screen.png ./artifacts/screen.png
echo "UI dump saved to ./artifacts/"
```

For frontend, use Playwright screenshot tests in `verify` commands.

### 5. Parallel Execution Setup (Long-term Task Only)

For Batch 2 parallel execution using git worktree + Codex Goal:

```bash
# Create worktree for each parallel task
git worktree add ../worktree-{task-name} -b {branch-name}

# In each worktree session:
cd ../worktree-{task-name}
python ./.trellis/scripts/task.py start {task-name}
# AI implements in this isolated worktree

# After all parallel tasks done, merge:
git checkout main
git merge {branch-name-1}
git merge {branch-name-2}
# Resolve conflicts if any
```

### 6. `/trellis:continue` Compatibility

The standard `/trellis:continue` route table remains compatible because:
- `needs_ui_review` and `needs_perf_review` are handled within `in_progress` status (not separate statuses)
- Scenario identification is recorded in `prd.md` frontmatter, not in `task.json.status`
- The AI reads `workflow.md` to determine which scenario sub-flow to follow
