# Requirements Audit

Source: `dominion-codex-prompt.md`

This audit uses the original Dominion prompt as the source of truth. The current repository is a working vertical slice, not a complete production game.

## Summary

| Status | Count |
| --- | ---: |
| PASS | 21 |
| PARTIAL | 29 |
| FAIL | 9 |

## Findings

| Requirement | Status | Evidence |
| --- | --- | --- |
| World model has regions, polities, settlements, tags, and world logic | PASS | `backend/app/simulation/models.py`, `backend/app/worldgen/presets.py` |
| Region tags excluded from LLM prompt context | PASS | `ChronicleLog.prompt_context`, `test_region_tags_do_not_enter_prompt_context` |
| Procedural generation with seed and knobs | PARTIAL | Preset generator exists; full seeded planet generation is not implemented. |
| Three historical basemaps and two invented presets | PARTIAL | Preset names are declared; full scenario assets are not. |
| Pannable/zoomable vector map with culling | PARTIAL | Frontend renders an SVG vector map; pan/zoom/culling are not complete. |
| Chronicle log is append-only source of truth | PASS | `ChronicleLog.append`, decree/divine/blessing/disaster routes append events. |
| Archive threshold creates durable summaries and preserves raw IDs | PASS | `ArchiveEngine`, `test_archive_engine_preserves_raw_ids_in_summary_payload` |
| State projection recomputes derived state from chronicle events | PASS | `StateProjection`, projection tests. |
| WorldMind supports model tiers and token/cost accounting | PASS | `WorldMind.calls`, quota service, API call accounting. |
| Clock supports presets and world pressure | PARTIAL | Day/week/month/year exist; custom/until-major-event and full offline scheduler do not. |
| Rewind forks timelines | PASS | `RewindService`, rewind test. |
| Throne founding/inheritance and difficulty setup | PARTIAL | Demo polity exists; setup flow is not complete. |
| Freeform decrees with cost preview | PARTIAL | Decrees work and spend credits in UI; multi-decree turn preview is not complete. |
| Plausibility gate | PASS | `DecreeService` rejects out-of-logic laser decrees. |
| Diplomacy | FAIL | No negotiation pipeline or multi-party chat exists. |
| Chancellor reads compact state | PASS | `Chancellor.brief`, `ModeDetails` panel. |
| Autonomous world pressure | PARTIAL | Clock emits hunger pressure; richer rival/nature schedules are missing. |
| No scripted ending | PASS | No hardcoded victory/defeat state. |
| Providence blessings/curses have bounded mechanical effects | PASS | `BlessingCurseService`, magnitude test. |
| Player-invoked disasters | PASS | `DisasterService`, UI drought action. |
| Free-form divine acts materialize structured effects | PASS | `GroundingEngine`, high/low magic tests. |
| Omens | PASS | `OmenService`; UI still needs a separate omen button. |
| Omen Log shows interpretation trail | PASS | Frontend Omen Log and backend payload. |
| Settlement autonomy dashboard | PARTIAL | Settlement state is visible; emergent local events are minimal. |
| Multiple settlements in one sandbox | PASS | Three settlements are selectable and affected independently. |
| World Forge terrain/region/settlement editor | PARTIAL | Backend editor and UI panel exist; drawing/painting tools are not complete. |
| Publish, browse, copy, version worlds | PARTIAL | Community service and UI panel exist; no persistent hub database yet. |
| Published-world moderation | PARTIAL | Moderation and report queue exist; publish scan persistence is not complete. |
| Mode switcher and combined overview | PASS | Frontend mode switcher and overview panel. |
| Shared chrome, chronicle, diff view | PARTIAL | Chronicle and diff strip exist; timeline scrubber is missing. |
| First-time onboarding | FAIL | No onboarding flow. |
| Accessibility | PARTIAL | ARIA labels and semantic controls exist; full WCAG audit is not done. |
| Tablet usability | PARTIAL | Responsive CSS exists; tablet-specific workflow testing is not complete. |
| Visible credit/budget system | PASS | Credit balance and quota service. |
| Per-world/per-turn tier choice | PARTIAL | Backend tiers exist; UI selector/locking is missing. |
| Shared quota service | PASS | `QuotaService`. |
| Persistence and save dashboard | FAIL | In-memory demo world only; no Postgres persistence. |
| Shared worlds with permissions/activity feed | PARTIAL | Contracts/docs mention it; production behavior is missing. |
| Export full chronicle and state as JSON | PASS | `/api/worlds/demo/export`, frontend export action. |
| Queue, timeout, retry, progress states | FAIL | Worker placeholder exists; real queue/retry policy is not implemented. |
| Archive engine background job | PARTIAL | Engine exists; production background scheduling is missing. |
| Rate limits/circuit breakers/fallback | FAIL | Not implemented beyond docs. |
| Lighthouse targets | FAIL | No Lighthouse run or budget. |
| Moderation on decrees, diplomacy, divine acts, published worlds | PARTIAL | Decrees/divine/blessing/disaster/report routes check moderation; diplomacy/publish flow missing. |
| Safety documentation | PASS | `SAFETY.md`. |
| In-app reporting/admin review queue | PARTIAL | Report endpoint and UI action exist; admin UI is missing. |
| Stack and repo layout | PASS | FastAPI, Vite/React, Docker, frontend/backend container targets, Makefile, docs, GitHub workflows. |
| Production CORS configuration | PASS | `BACKEND_CORS_ORIGINS` config and backend config tests. |
| Recorded LLM fixtures, unit, integration, E2E tests | PARTIAL | Grounding/unit/E2E tests exist; broader integration matrix is incomplete. |

## Fixed In This Pass

- Added configurable backend CORS through `BACKEND_CORS_ORIGINS`.
- Added a frontend production Dockerfile and compose service.
- Added deployment documentation covering required production env values.
- Added frontend ESLint config for the existing `npm run lint` and `make lint` scripts.
- Added input moderation to backend decree, divine act, blessing, disaster, and report routes.
- Added JSON export for the demo world projection and chronicle.
- Added WorldMind token/cost call accounting.
- Added mode-specific frontend panels for Dashboard, Throne, Providence, World Forge, and Community.
- Added frontend export/report actions.
- Added API tests for moderation, export, and reporting.
