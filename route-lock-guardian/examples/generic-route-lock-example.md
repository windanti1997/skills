# Generic Route Lock Example

## Current Route

The project is a local-first automation tool that helps users complete repetitive project work without hiding irreversible decisions.

## Must Stay True

- First-time setup must be one command or one guided flow.
- Automation may suggest actions but must not perform irreversible changes without approval.
- User-facing workflow must stay simpler than the internal architecture.
- Background work must be visible, bounded, and recoverable.

## Must Not Happen

- No hidden long-running background process by default.
- No auto-approval of user preferences, permissions, lifecycle changes, or team rules.
- No setup flow that requires users to understand internal modules.
- No release claim before a fresh-install dogfood path passes.

## Current Stage

Dogfood shadow mode.

## Allowed Now

- Collect evidence.
- Create proposals.
- Produce advisory warnings.
- Auto-accept low-risk observed facts with evidence and TTL.

## Forbidden Now

- Irreversible writes without explicit approval.
- Team/spec promotion without maintainer review.
- Hidden background jobs as default behavior.
