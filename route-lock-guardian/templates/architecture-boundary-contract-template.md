# Architecture Boundary Contract

## Components

| Component | Owns | May Read | May Write | Must Not Write | Must Not Decide |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Control Surfaces

List surfaces that require explicit ownership.

- lifecycle state
- persistent state
- configuration
- approval state
- release state
- user preference
- team/spec rule

## Forbidden Cross-Boundary Writes

- 

## Boundary Review Questions

- Did any component write state it does not own?
- Did any proposal directly become durable state?
- Did any checker/verifier mutate lifecycle state?
- Did any generated instruction override source-of-truth docs?
