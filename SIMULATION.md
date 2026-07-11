# Simulation

The chronicle log is append-only. Projection is deterministic and produces ownership, resources, population, relations, active effects, and event history from logged events only.

## Archive Engine

When a world's raw chronicle length crosses the configured threshold, the Archive Engine compresses the oldest chunk into a durable summary event. Raw event IDs remain linked in the summary payload so the Deep Archive can still browse original history.

Before:

```text
1 decree: repair levee
2 disaster: flood
3 diplomacy: iron pact
...
12 world_event: famine pressure
```

After:

```text
13 archive_summary: compressed 12 old events
payload.raw_event_ids = [1..12]
payload.summary = "1:decree:repair levee; ..."
```

Future WorldMind calls receive current projection, recent events, and compact summaries rather than the full raw log.

## Clock

Throne Mode supports day/week/month/year/custom advancement. Providence Mode uses deterministic missed-day catchup on next open for offline progression.

## Rewind

Rewind never mutates the original timeline. Continuing from an old event creates a forked world with `branch_of` pointing back to the source world.
