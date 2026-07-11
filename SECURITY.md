# Security

Do not commit `.env` files or provider keys. Use `.env.example` for variable names only.

Report vulnerabilities privately through GitHub Security Advisories once the repository is published.

Production deployments should use:

- Managed Postgres and Redis credentials from a secret store.
- HTTPS-only frontend and API origins.
- JWT secret rotation.
- Provider API keys scoped per environment.
- Rate limits and circuit breakers around WorldMind calls.
