# Prompt Patterns

## Start a Route Lock

Use `route-lock-guardian` before implementation. Create minimal route files under `docs/route/`, then write a Route Alignment Note for the current task.

## Continue a Task Safely

Before continuing, read `docs/route/current-route-lock.md`, `docs/route/user-journey-contract.md`, and `docs/route/non-goals-and-killed-routes.md`. State which route is being continued and which killed routes must not reappear.

## Review a Completed Task

Review using the four gates: route consistency, user journey, authority safety, and killed route regression. Do not mark the task complete if any gate fails.

## Repair Drift

Create a route repair task. First update route docs, killed routes, matrices, and checks. Then repair code, config, prompts, hooks, templates, and tests that violate the route.

## Ask for Clarification Without Stalling

If route files are missing and the task is high-impact, draft a minimal route lock from available context and ask the user to confirm the route before implementation.
