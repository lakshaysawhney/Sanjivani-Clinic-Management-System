# Mandatory repository instructions

## Read before work

Read `docs/README.md`, `docs/progress.md`, `docs/requirements.md`, `docs/decisions.md`, `docs/permissions.md`, `docs/architecture.md`, `docs/verification.md`, and relevant `docs/requirements-coverage.md` rows before starting. Consult sanitized source specifications in `docs/sources/` for exact acceptance details. Never depend on conversation history.

Work is now incremental professional engineering. The historical one-shot directive does not authorize continuing unrelated implementation during a scoped issue. Latest user instructions control scope. Preserve existing code. Documentation-only work must not change application code, run migrations, provision services, deploy or modify operational data.

## Professional workflow

Follow Issue → Branch → Implementation → Tests → Conventional Commits → Push → PR → Review → Merge. Use meaningful issue-focused branch names; follow an environment-required prefix if one exists without inventing assistant-name prefixes. The inherited branch name is historical, not a convention or authorization to rename it during documentation work.

Use conventional commit types `feat`, `fix`, `test`, `refactor`, `docs`, `chore`, `ci`. Never include AI-agent names in project-authored branch names, code comments, documentation or commit messages. Service/product names required to identify dependencies are allowed. Keep commits logical/reviewable, avoid destructive history changes and artificial issues. Never merge into `main` without explicit owner approval.

Write meaningful comments/docstrings explaining business logic, complex decisions, invariants and architecture. Do not describe obvious code redundantly. Update progress.md, verification.md, coverage and relevant decisions after every completed issue. Record commands, environment, counts, failures, revision and limitations. Never mark a feature verified without test evidence. Test source or a successful build is not a passing acceptance run.

## Product invariants

- Session authentication with CSRF, secure cookies, server roles/object/date scopes on every list/detail/report and future export. No JWT, browser-local-storage secrets or public signup.
- Exactly ADMIN/RECEPTIONIST/THERAPIST; separate users/providers; no staff deletion, unrestricted role escalation or real shared default password.
- IST ten fixed 45-minute slots, lunch 12:15-13:00, completion at slot end, no No-show state.
- Ordinary session: one child/provider. Group Therapy: one shared session, multiple assignments and per-child attendance. Preserve database booking conflicts and cancellation history.
- Fixed desktop six-plus-five stacked timetable, private bootstrap order, no diary-derived patient fixtures.
- Reception correction cutoff exactly 18:00 on appointment date; tomorrow stays editable. Final slot ends 18:15, requiring admin for later corrections. Admin all-time; reception history current plus previous two calendar months; therapist own completed history current plus previous month. Daily publication expiry is separate.
- Only Completed participation counts/bills. Use exact currency, immutable ledger/audit, historical fee snapshots, explicit accounting cutoff, auditable reversals, transactions and idempotency. Balances never reset monthly; financial markers never silently change prices.
- Recover after sleep/restart through durable bounded reconciliation/reminders/outbox. Generic emails contain no child/financial details. Preserve ambiguities explicitly in decisions.md rather than silently changing requirements.

## Privacy and approvals

Repository stays public. Only synthetic committed fixtures. Never publish private staff/sender contacts, patient information, diary images, passwords, secrets, connection strings, OAuth credentials or dumps in source/history/logs/issues/PRs/screenshots/CI artifacts. `.private/` and `.env` stay ignored. Private bootstrap inputs come through authorized private storage; never request secrets in chat.

Stage A: Cloudflare Pages Free, Render Free, Neon Free, Gmail HTTPS API. Let Render sleep. No synthetic keep-alive or recurring pilot pings. Use authorized activity and explicit maintenance, documenting delays.

Stage B: explicit approval for existing-service Starter upgrade and real-data go-live. Verify current price, performance/memory, security, accounting, genuine scheduler, email, encrypted external backups/restoration and clinic acceptance. More expensive tiers, destructive operations, real-data migration and real staff invitations/test email require applicable explicit approval. Available tools do not prove account access.

## Structure and validation

Backend: accounts, clinic domain service modules, config and tests. Frontend: src, functions and tests. PostgreSQL is required for integration/concurrency evidence; never substitute SQLite. Tests must use disposable test databases, never pilot/production. Inspect private configuration targets safely without printing credentials. Fast hashing is allowed only for synthetic tests; runtime retains secure hashing.

Future issue commands: `ruff check backend scripts`; `ruff format --check backend scripts`; backend `pytest -q`, `python manage.py makemigrations --check --dry-run`; frontend `npm run check`, `npm run build`, `npm run test:e2e`. Windows wrappers: `.venv/Scripts/python scripts/dev.py manage.py ...`, `.venv/Scripts/python scripts/dev.py -m pytest -q --reuse-db`, `.venv/Scripts/python scripts/browser_tests.py`. Browser Windows launcher remains an open failure. Do not run application tests during documentation-only work.

Preserve failed forms and mutation keys. No U+2014 em dash in visible website copy. Verify 1366×768, 1536×864 and mobile therapist views with synthetic data. Local tests do not verify deployed sessions, CSRF, OAuth delivery or backups.
