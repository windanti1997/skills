# Review Gates

Use these gates for any implementation, planning, review, dogfood, or release task.

## Gate 1: Route Consistency

Check whether the task preserves the route described in `docs/route/current-route-lock.md`.

Fail if:

- the change enables next-stage behavior early
- the change contradicts a must-stay-true invariant
- the task completes a local module while ignoring the intended product route

## Gate 2: User Journey

Check whether the intended user flow is still true.

Fail if:

- the user must understand internal modules to use the project
- setup requires unexplained extra commands
- the system interrupts the user more often than allowed
- degraded mode is unsafe or confusing

## Gate 3: Authority Safety

Check whether each actor wrote only what it is allowed to write.

Fail if:

- a proposal directly becomes durable state
- a hook or background job writes active state without authority
- auto-accept applies to preferences, behavior rules, safety rules, lifecycle transitions, team/spec rules, or model inference

## Gate 4: Killed Route Regression

Check whether abandoned ideas returned through code, config, prompts, docs, generated instructions, examples, test fixtures, or status messages.

Fail if any killed route reappears without an explicit route change.
