# Drift Smells

These are signs that a project may be drifting even if local tasks pass.

- “Tests pass” but no user journey was simulated.
- A task says complete while core acceptance is deferred.
- Default configuration enables behavior from an abandoned route.
- Generated instructions mention a killed route.
- Hook behavior writes durable state silently.
- A checker/verifier mutates lifecycle state.
- The user must understand internal modules to finish setup.
- A new mode is added without updating route docs.
- Auto-accept exists without authority classification.
- The implementation adds background work without a workflow-event policy.
- Documentation and runtime disagree about ownership.
- A fallback path revives an old architecture.
- Review focuses on file existence rather than route gates.
