# Architecture

Dominion uses an append-only chronicle log as the source of truth. Every decree, diplomatic exchange, divine act, omen, disaster, autonomous world event, and archive summary is written as a chronicle event. The projected world state is recomputed from those events.

## Backend

- `api/`: REST routes for world loading, Throne decrees, Providence actions, and clock advancement.
- `simulation/`: chronicle log, state projection, clock, archive engine, and rewind/fork behavior.
- `throne/`: decree plausibility, chancellor summaries, and diplomacy extension points.
- `providence/`: blessing/curse math, disasters, omens, and the grounding engine.
- `worldgen/`: procedural and authored preset starting worlds.
- `worldforge/`: pre-game scenario authoring.
- `community/`: publish, browse, copy, and version contracts.
- `worldmind/`: provider-neutral LLM call abstraction with fixture behavior in CI.

## Workers

Production workers should run four independent queues: turn simulation, archive compression, settlement ticks, and moderation review. Local development ships a simple worker entry point so the command surface is stable before queues are wired to Redis.

## Realtime

The intended channel model is one websocket/SSE stream per open world. Chronicle events are pushed as they commit; clients recompute or fetch a compact projection after each event batch.
