# Deployment

Dominion is deployable as separate frontend and backend services backed by Postgres and Redis.

## Required Production Settings

- `APP_ENV=production`
- `BACKEND_CORS_ORIGINS`: comma-separated HTTPS origins allowed to call the API.
- `DATABASE_URL`: production Postgres DSN.
- `REDIS_URL`: production Redis DSN.
- `JWT_SECRET`: long random secret managed by the hosting platform.
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`: optional unless live WorldMind calls are enabled.
- `MODERATION_PROVIDER_KEY`: optional until external moderation is wired in.
- `WORLD_DEFAULT_MODEL_TIER`: `fast` or `deep`.
- `ARCHIVE_THRESHOLD_EVENTS`: event count threshold before archive summaries are generated.

## Docker Compose Smoke Test

```bash
docker compose -f infra/docker-compose.yml up --build
```

Frontend: `http://localhost:5173`
Backend: `http://localhost:8000`
Health check: `http://localhost:8000/health`

## Standalone Backend

```bash
python -m pip install -e ".[dev]"
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

## Standalone Frontend

```bash
cd frontend
npm ci
npm run build
npm run dev
```

## Current Production Limits

The repository is a working vertical slice. It still needs account-level hosting setup, production database/Redis provisioning, secrets, a persistent save model, and admin/moderation operations before it can be treated as a complete production game service.
