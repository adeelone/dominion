# Dominion

Dominion is an AI-assisted world simulation sandbox where a player can rule a nation directly in Throne Mode or intervene indirectly as an unseen deity in Providence Mode.

## Stack Justification

- Backend: Python 3.12 and FastAPI keep the simulation core explicit, testable, and easy to run in workers.
- Frontend: Vite, React, TypeScript, Zustand, and TanStack Query keep the map-heavy interface responsive without a server-rendering dependency.
- Data: Postgres is the source of truth for chronicle events and projections; Redis backs queues, quotas, rate limits, and realtime fanout.
- WorldMind: a provider abstraction supports a cheap fast tier and a deeper quality tier. CI uses recorded fixtures only.
- Map renderer: the first implementation uses a culled SVG/vector layer. The shape contracts are compatible with MapLibre or deck.gl if the map scale grows.

## Quickstart

```bash
make install
make dev
```

Or run the full local stack:

```bash
docker compose -f infra/docker-compose.yml up --build
```

Frontend: `http://localhost:5173`  
Backend: `http://localhost:8000`
Health check: `http://localhost:8000/health`

## Core Flows

1. Create or copy a world from Dashboard or Community.
2. Use World Forge to edit terrain, region borders, settlements, polity tags, and world logic rules.
3. Enter Throne Mode to issue decrees, negotiate, ask the Chancellor, and advance time.
4. Switch to Providence Mode to cast blessings, curses, disasters, omens, and free-form divine acts.
5. Review the Chronicle, Omen Log, and What Changed diff after each simulation step.
6. Rewind any world to a prior chronicle event and continue on a preserved fork.

## Assumptions

- Single-player is the baseline path; shared worlds are implemented through role-based participation records and a shared feed, but do not yet include conflict-resolution UX for simultaneous edits.
- Offline Providence progression is deterministic: settlements accrue missed day ticks on next world open rather than running an always-on scheduler locally.
- Historical basemaps ship as compact authored presets rather than full GIS datasets.
- Free-form AI behavior is fixture-backed in tests and locally deterministic unless provider keys are configured.

## Scripts

```bash
make lint
make typecheck
make test
make test:e2e
make format
```

## Environment

Copy `.env.example` to `.env` and set provider keys only for live WorldMind calls. Tests do not require live LLM credentials.

For production deployment settings, see `DEPLOYMENT.md`.

## Screenshots

The primary app shell is a map-first operations interface with mode tabs, decree/divine-act tools, an Omen Log, and a chronicle timeline.

## Next Steps

- Add production deployment targets for API, workers, frontend, Postgres, and Redis.
- Expand shared-world permissions into live conflict handling.
- Add a mobile-native companion interface for chronicle review and light interventions.
- Add a mod API for data-defined blessings, curses, disasters, and entity behaviors.
