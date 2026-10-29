# Sanjivani Clinic Management System

Start with the [project handoff index](docs/README.md) and [current progress](docs/progress.md). The [decisions register](docs/decisions.md), [complete source-clause coverage](docs/requirements-coverage.md) and [verification evidence](docs/verification.md) distinguish mandatory product scope from unverified implementation. Work now proceeds through incremental issues and conventional commits. Existing application code must be preserved.

An internal clinic workspace for manual scheduling, shared group therapy, patient attendance, frequency plans, staff access and cumulative billing.

React/TypeScript/Vite/Tailwind with accessible Radix dialog primitives and TanStack Query connects to a Django/DRF modular monolith. PostgreSQL owns sessions, conflict reservations, audit, idempotency and the append-only financial ledger. Cloudflare Pages proxies same-origin API requests to Render; Neon stores durable data. Gmail uses HTTPS OAuth and a durable outbox.

## Local development

1. Create a Python 3.13 virtual environment and install `backend/requirements.txt`.
2. Start PostgreSQL using `docker compose up -d` or an isolated development database. Set environment values from `.env.example`; never use production for tests.
3. Run `python backend/manage.py migrate`.
4. Set a private E2E_PASSWORD and DEBUG=1, then run `python backend/manage.py seed_demo` for synthetic accounts. No common production password exists.
5. Start `python backend/manage.py runserver 127.0.0.1:8000`.
6. In frontend, run `npm ci` and `npm run dev`. Vite proxies `/api` to Django.

On this Windows workspace, the ignored private development configuration is loaded by `.venv/Scripts/python scripts/dev.py manage.py <command>`. It does not use the pilot database branch.

## Verification

Backend: `cd backend && pytest -q`; migration check: `python manage.py makemigrations --check --dry-run`. Repository lint: `ruff check backend scripts` and `ruff format --check backend scripts`.

Frontend: `npm run check`, `npm run build`, `npx playwright install chromium`, `npm run test:e2e`. Browser tests need synthetic demo accounts and private E2E_PASSWORD. CI supplies disposable PostgreSQL and synthetic credentials. `python scripts/check_public.py` scans tracked source for accidental private material.

See [verification evidence](docs/verification.md), [requirements](docs/requirements.md), [architecture](docs/architecture.md), [data model](docs/data-model.md), [permissions](docs/permissions.md), [scheduling](docs/scheduling.md), [billing](docs/billing.md), [deployment](docs/deployment.md), [operations](docs/operations.md) and [assumptions](docs/assumptions.md).

## Deployment policy

The pilot uses free Cloudflare Pages, Render and Neon. Render may sleep; reconciliation catches up after authorized activity. No keep-alive scheduler is configured. Production requires explicit paid-compute and go-live approval, verified backups/restore, operational scheduler, email verification and clinic acceptance. A successful build alone does not meet these gates.

Work follows Issue → Branch → Tests/Implementation → Conventional Commits → Push → PR → CI → Review → Merge. The final main merge requires owner approval. Phase 0A preserves the unverified implementation on `feat/1-initial-mvp`; consult the evidence register for current publication status and the [prioritized backlog](docs/backlog.md) for remaining work. This checkpoint is not a completed MVP.
