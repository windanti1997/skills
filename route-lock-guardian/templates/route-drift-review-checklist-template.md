# Route Drift Review Checklist

## Gate 1: Route Consistency

- [ ] Change matches `current-route-lock.md`.
- [ ] No current-stage forbidden behavior was introduced.
- [ ] Next-stage behavior is not enabled prematurely.

## Gate 2: User Journey

- [ ] First-time flow still works.
- [ ] Daily flow did not become more complex without explicit product reason.
- [ ] User interruption budget is preserved.
- [ ] Degraded mode is safe and understandable.

## Gate 3: Authority Safety

- [ ] No actor wrote state above its authority level.
- [ ] Auto-accept, if present, follows `authority-matrix.md`.
- [ ] Durable/high-authority state requires approval.

## Gate 4: Killed Route Regression

- [ ] No killed route appears in code.
- [ ] No killed route appears in default config.
- [ ] No killed route appears in docs/examples/generated instructions.
- [ ] Guard checks were added or updated.
