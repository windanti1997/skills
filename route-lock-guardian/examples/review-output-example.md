# Review Output Example

结论：不通过

## Route Consistency

The change implements the local module but violates the current route lock because it enables a next-stage behavior before dogfood readiness has passed.

## User Journey

The first-time flow now requires users to run two internal setup commands. This violates the user journey contract, which requires one guided entry point.

## Authority Safety

The implementation allows a generated proposal to become active state without explicit approval. This violates the authority matrix.

## Killed Route Regression

The default config reintroduced a killed background workflow. This appears in config, docs, and generated instructions.

## Blocking Issues

1. Default config enables killed behavior.
2. Generated instructions tell the agent to run the old workflow.
3. No route-level acceptance test exists.

## Required Fix

Disable the killed route by default, remove it from generated instructions, add a regression test, and update the route alignment note.
