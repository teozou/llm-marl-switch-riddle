# Switch Riddle as a Dec-POMDP

## Definition

M = (N, S, {A_i}, {O_i}, T, R, γ)

- N = {0, 1, ..., n-1} — the agents
- S = {0,1} × 2^N × N — (light, visited set, current agent)
- A_i = {0, 1, 2} — noop, toggle, declare
- O_i = {0,1} × {i} — each agent sees only (light, own ID)
- γ = 0.99

## Transitions

- action 0 (noop): light unchanged, next agent picked uniformly at random
- action 1 (toggle): light flipped, next agent picked uniformly at random
- action 2 (declare): episode ends

After each step, current agent is added to the visited set.

## Reward

- declare when visited = N → +1
- declare when visited ⊊ N → -1
- otherwise → 0

## Optimal Protocol

Agent 0 is the counter. Others are signalers.

Signalers: first time you see light OFF, toggle ON. Otherwise do nothing.
Counter: if light ON, toggle OFF, count += 1. If count = n-1, declare.

This works because each signaler toggles exactly once, so the counter receives exactly n-1 signals before declaring.