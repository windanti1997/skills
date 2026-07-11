# Authority Matrix

## Authority Levels

| Level | Name | Description | Can Be Auto-Accepted? | Requires Approval? | Expiry/TTL? |
|---|---|---|---|---|---|
| L0 | evidence / log / artifact | Raw record, output, trace, report, observation | yes | no | optional |
| L1 | observed fact | Low-risk fact grounded in explicit evidence | yes, if policy allows | no | required |
| L2 | candidate / proposal | Suggested rule, memory, config, or action | no | yes before activation | optional |
| L3 | active user-approved rule | Durable behavior-affecting state approved by user/maintainer | no | yes | recommended |
| L4 | active auto-accepted low-risk fact | Narrow observed fact auto-accepted under strict constraints | yes | no | required |
| L5 | team / spec / organization rule | Shared durable standard | no | yes | policy-dependent |
| L6 | quarantined / rejected item | Unsafe, stale, rejected, or blocked item | no | yes to release | optional |

## Auto-Accept Allowed Only If

- low risk
- narrow scope
- explicit evidence
- reversible
- TTL or expiry exists
- no strong behavior-control language

## Auto-Accept Forbidden For

- user preference
- behavior rule
- safety rule
- permission rule
- lifecycle transition
- team/spec rule
- model inference without evidence
- anything containing strong control language such as always, never, must, skip, bypass, delete, ignore

## Approval Required For

- 

## Promotion Rules

- Candidate to active:
- Active local to team/spec:
- Quarantine release:
