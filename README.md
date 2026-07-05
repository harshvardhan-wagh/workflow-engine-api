# Workflow Engine API

Minimal FastAPI + PostgreSQL workflow/approval engine. v1 scope: dynamic multi-step
approval workflows (define steps as an ordered list of roles), start an instance,
approve/reject step by step, view audit trail.

## Stack
- FastAPI
- PostgreSQL (SQLAlchemy ORM)
- JWT auth (python-jose + passlib)
- Docker + docker-compose for local dev

## Run locally with Docker

1. Copy the env file:
   ```
   cp .env.example .env
   ```
2. Build and start everything (API + Postgres):
   ```
   docker compose up --build
   ```
3. API is live at http://localhost:8000
   Interactive docs (Swagger UI): http://localhost:8000/docs

The API container mounts `./app` as a volume and runs with `--reload`, so code
changes on your machine are picked up automatically — no rebuild needed for
plain code edits (only rebuild if you change `requirements.txt`).

## Endpoints (v1)

| Method | Path                          | Description                          |
|--------|-------------------------------|---------------------------------------|
| POST   | /auth/register                | Create a user                        |
| POST   | /auth/login                   | Get JWT access token                 |
| POST   | /workflows                    | Create a workflow definition         |
| GET    | /workflows                    | List workflow definitions            |
| GET    | /workflows/{id}                | Get one workflow definition          |
| POST   | /workflows/{id}/start           | Start a new instance of a workflow   |
| GET    | /instances/{id}                | Get instance status + audit trail    |
| POST   | /instances/{id}/decide          | Approve/reject the current step      |

## Example flow

1. Register two users — one `employee`, one `manager`.
2. Login as the manager-creating user, `POST /workflows` with:
   ```json
   { "name": "Leave Request", "steps": ["manager"] }
   ```
3. `POST /workflows/1/start` to create an instance.
4. Login as the `manager` user, `POST /instances/1/decide` with:
   ```json
   { "decision": "approved", "comment": "Looks good" }
   ```
5. `GET /instances/1` to see status `approved` and the approval in the audit trail.

## Not in v1 (intentionally out of scope)

Workflow versioning, revoke/resume rollback, dynamic runtime reassignment —
already built once in PHP at C-DAC. Left out here to keep this project minimal
and finished, rather than half-built and complex.

## Next steps (not done yet)
- Alembic migrations (currently uses `Base.metadata.create_all` on startup)
- Dockerize for production (multi-stage build, non-root user)
- Deploy to Kubernetes
