# Workflow Event Policy

## Event Matrix

| Event | Can Read | Can Write | Can Suggest | Can Block | Can Ask User | Can Create Candidate | Can Create Active State | Must Not Do | Failure Behavior |
|---|---|---|---|---|---|---|---|---|---|
| Start / SessionStart |  |  |  |  |  |  |  |  |  |
| PreAction / PreToolUse |  |  |  |  |  |  |  |  |  |
| PostAction / PostToolUse |  |  |  |  |  |  |  |  |  |
| UserResponse / UserPromptSubmit |  |  |  |  |  |  |  |  |  |
| Stop / Finalize |  |  |  |  |  |  |  |  |  |

## Default Safe Pattern

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
