# Architecture

Consolidated 2026-10-29. This describes implemented structure and intended invariants, not a claim that tests pass. Read progress.md and verification.md before making readiness claims. decisions.md records finalized requirements, assumptions and unresolved conflicts. The full source-clause coverage is requirements-coverage.md.

The application is a modular Django monolith with a React client. Domain modules separate scheduling, billing, notification delivery, time policies and API presentation inside the clinic app; account identity lives in its own app. This avoids cross-app migration cycles without mixing financial behavior into views.

Browser requests use `/api/` on Cloudflare Pages. A Pages Function forwards to a fixed Render HTTPS origin and supplies a shared secret; it does not accept an upstream URL from the caller. Django also applies sessions, CSRF, role checks and object/date scopes. Patient responses have no-store headers. No financial or authentication data is put in browser local storage.

PostgreSQL is authoritative. Reservation uniqueness prevents double-booking under concurrency. Sessions and affected patients are locked inside transactions. Paise ledger entries and audit events are append-only at the database layer. API mutation keys persist the exact successful response and reject reuse with changed content.

Reconciliation runs on authorized clinic activity and an explicit protected maintenance operation. Pilot downtime delays processing; effective appointment end times remain unchanged. Production scheduling will invoke actual maintenance after approval. There is no in-memory timer or uptime-ping dependency.

The outbox commits with schedule changes. Sending is a separate operation. Confirmed failures receive bounded retries; ambiguous timeouts and interrupted sends require review to avoid blind duplicate sends. Gmail does not provide a transactional exactly-once delivery guarantee.

## Domain model and code map

| Domain | Entities / source | Responsibilities |
|---|---|---|
| Identity | accounts/models.py: User, Provider, LoginAttempt, CredentialToken | Role identity separate from schedulable identity; durable throttling; hashed single-use setup/reset tokens |
| Patients | clinic/models.py: Patient, FrequencyPlan | Stable IDs, duplicate names, active/review state, independently dated expectations |
| Scheduling | DailySchedule, Session, Assignment, Participation, provider/patient reservations; scheduling.py, time_rules.py | Day-level publication, fixed slots, group membership/status, ending time, versioned edits and conflict ownership |
| Accounting | LedgerEntry; billing.py | Signed paise, unique source references, snapshots/revisions, reversal links, cumulative balance and dues resolution |
| Notifications | Notification, EmailOutbox, IntegrationSecret; email_service.py | Persistent unresolved state, transaction-safe delivery events, bounded retries and encrypted sender credentials |
| Integrity | AuditLog, IdempotencyRecord, migration 0002 | Before/after/reason/actor, immutable record triggers, actor/key/payload response binding |
| API | clinic/api.py, accounts/views.py, config/urls.py, middleware.py | Session/CSRF, role/object/date serialization, protected origin and private responses |
| Client | src/pages/App, Schedule, Patients, Operations; api.ts; common.tsx | Role routes, operational tables/forms/dialogs, query invalidation, preserved mutation keys and errors |
| Edge/deployment | functions/api/[[path]].ts, render.yaml, docker-compose.yml, .github/workflows/ci.yml | Fixed API upstream, free pilot process, isolated local PostgreSQL and planned CI |

## Request and consistency boundaries

An authenticated clinic request currently runs bounded reconciliation and reminder recovery in ClinicView.initial before its handler. Session mutations lock the existing session, affected patients in ID order and the day, validate participants/providers/slot, synchronize reservations, reconcile charges, append audit/outbox and commit atomically. Unique resource/date/slot reservations are the final database conflict defense. This sequence is present code; concurrent booking/payment/correction/deadlock behavior still requires passing evidence.

Manual ledger operations lock the patient; balance derives from ledger aggregation. Idempotent API mutations bind actor plus UUID to path/payload digest, serialize same-user writes and retain response JSON. Frontend retains a mutation key across retries of identical content. Do not silently reuse a key with changed content or promise exactly-once external email delivery.

An outbox worker claims a pending row with locking, persists sending before HTTPS I/O and records sent/provider ID only on success. A crash or ambiguous network result can leave sending/uncertain state; operator recovery/alerts remain incomplete. No timer or persistent browser is authoritative for accounting.

## Deployment topology and separation

Static frontend must remain available while the free backend sleeps. Browser cookies belong to the frontend origin; its fixed proxy supplies a shared secret and forwards CSRF/Origin/Set-Cookie without exposing secrets to client bundles. Direct backend bypass and proxy timeout/redirect/cache behavior need deployed tests. PostgreSQL-backed sessions survive application restarts; ephemeral hosting disk is not durable storage.

Prior work created a Neon free pilot branch and separate cloud development branch in Singapore; local development was later switched to Docker PostgreSQL. Tests use a dedicated disposable test database. Private local wrappers load ignored configuration; fresh agents must inspect targets safely. Never test against pilot/production or infer availability from stored credentials.

Production scheduler and encrypted external backups are required architecture deliverables, not completed integrations. The paid upgrade is separate from go-live approval and does not itself schedule maintenance. All eight open concerns in decisions.md must remain visible until resolved in scoped issues.
