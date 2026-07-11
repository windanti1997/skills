# route-lock-guardian

A generic Agent Skill for preventing route drift in long-running projects.

It is intentionally project-agnostic. It does not assume any specific repository, product, framework, agent, or architecture.

## Install

Copy this folder to a supported skills directory, for example:

```text
.agents/skills/route-lock-guardian/
.claude/skills/route-lock-guardian/
.trellis/skills/route-lock-guardian/
```

## Use

Ask the agent to use `route-lock-guardian` before planning, continuing, implementing, reviewing, dogfooding, or releasing a long-running project.

## Included assets

- `SKILL.md`: trigger rules and operating procedure
- `templates/`: route-lock contract templates
- `references/`: review gates, drift smells, and prompt patterns
- `scripts/`: optional route-lock initialization and drift-check scripts
- `examples/`: generic examples, not tied to a specific project
