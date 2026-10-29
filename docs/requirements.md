# MVP requirements and acceptance register

## Authority and complete source preservation

Consolidated 2026-10-29. This document and the complete sanitized [master specification](sources/master-specification.md) and [final deployment amendment](sources/deployment-amendment.md) together form the product contract. **Every retained source clause is mapped in [requirements coverage](requirements-coverage.md)**. These sources are normative for product/acceptance detail, not instructions to execute historical one-shot work during a scoped issue. Latest user scope now requires incremental professional engineering. The amendment overrides conflicting master deployment/scheduler language; no other feature is waived.

Private names, exact roster contacts, sender address and bootstrap order mappings are withheld publicly and preserved as authorized local source documents in ignored `.private/handoff/`. Public placeholders preserve stable identity references and the required order without publishing private roster data. Do not seed from the diary or publish it. A fresh clone must retrieve those private inputs securely only when onboarding is authorized.

## Exact time and counting contract

All times and calendar boundaries use Asia/Kolkata. Fixed slots are identifiers validated by the backend; code currently indexes them 0-9, while the following table numbers them 1-10 for humans.

| Slot | IST interval |
|---|---|
| 1 | 10:00-10:45 |
| 2 | 10:45-11:30 |
| 3 | 11:30-12:15 |
| Lunch (not a slot) | 12:15-13:00 |
| 4 | 13:00-13:45 |
| 5 | 13:45-14:30 |
| 6 | 14:30-15:15 |
| 7 | 15:15-16:00 |
| 8 | 16:00-16:45 |
| 9 | 16:45-17:30 |
| 10 | 17:30-18:15 |

No arbitrary/outside-hours appointment start or fake lunch slot. Operating days are configurable. Capacity is at most 110 provider-slots, not an expected load. Complete at the **end**, preserving effective end times through downtime. Reception corrections are allowed only before 18:00 on the appointment date; admin can correct retrospectively. Reception can still prepare future drafts after today's cutoff. Last-slot corrections after 18:15 require admin.

History: admin all time; reception current month plus previous two calendar months (future drafts unrestricted); therapist own completed current and previous calendar month. Weekly actual frequency uses Monday-Sunday. Completed participation counts once per child; a shared group counts once per assigned provider in therapist history. Do not add a category breakdown to the therapist's own history page. Cumulative finances are exempt from attendance-history month cutoffs.

Publication: Draft/Published are day-level states, separate from Scheduled/Completed/Cancelled. Publish current/next operational day as soon as ready; no wait until 18:00 and no republish after edits. Assigned therapists see their own published assignments until D+1 10:00. The original also intends no more than two visible days; preserve the unresolved early-publication edge case C01 in decisions.md. At 18:30, tomorrow's unpublished schedule creates a persistent admin/reception reminder, recoverable after missed activity. Closed-day semantics are C02, not an invented finalized rule.

## Catalog and finance contract

| Selectable label | Default INR |
|---|---:|
| OT | 900 |
| Sp. Edu. | 900 |
| ABA | 900 |
| Group Therapy | 900 |
| Assessment (2000) | 2000 |
| Assessment (2500) | 2500 |
| Assessment + Home Plan | 4500 |

Exactly seven options. Prefer Sp. Edu.; SE only in exceptional constrained space. The last visible label does not include 4500. Backend owns rates and historical snapshots; ignore unauthorized frontend prices.

Balance = opening + payments + signed adjustments - chargeable completed sessions, including auditable reversals. Positive is credit, negative dues, zero neither. Never reset at month rollover. Group fee is per completed child, never per provider. Opening balances may be positive/negative/zero and are ledger entries; corrections never overwrite them. Explicit accounting cutoff prevents pre-launch double billing. Payments require patient/amount/effective date-time/actor, optional method/reference/notes; exact paise or Decimal only. Corrections retain original and reversal/adjustment with actor/time. Special-fee patients initially receive standard charges and an amber `₹!` review marker, hidden from therapist payloads/views. Nonnegative-to-negative balances create durable deduplicated warnings; recovery to nonnegative resolves them and existing dues remain discoverable after login.

## Diary-derived interaction contract

Two vertically stacked tables, first six then five providers in the privately specified order, each with ten slot rows and a lunch divider. Never switch to an eleven-column default laptop grid or reorder by appointment density. Preserve short/full-name distinctions through bootstrap and administrator-controlled ordering. Test 1366×768 and 1536×864 at ordinary zoom, aiming for one screen without sacrificing readable patient names. Compact rows, restrained colors and no permanently expanded width-consuming sidebar.

Cells show child, therapy where space permits, status and authorized fee marker; long names use accessible truncation/details. Empty cells open preselected provider/date/slot. Existing cells open edit/details; group supports multiple children/providers, ordinary exactly one. Patient search and inline patient creation preserve the booking draft. Save/cancel/reassign/move/change therapy/correct status must show friendly conflict/validation and await server confirmation; never silently overwrite or assert an unconfirmed save. Cancelled history must not block replacement cells. Date navigation/picker/Today, publication status/action, compact summary, pending-change indication, refresh/loading/errors are required. Mobile reception may adapt or navigate providers; therapist portal must be mobile-friendly. The photo contributes workflow/layout only, never real patient data or handwritten styling.

## Identity, data minimization and operational requirements

The clinic serves children with developmental conditions; this is operational software, not a demonstration. Minimum patients have stable non-name IDs, creation time, active state, review flag and independent expected weekly/monthly counts. Duplicate names are valid. Do not collect diagnoses, treatment notes or reports without explicit scope. Profiles combine monthly attendance/category/provider breakdowns, plan details/history, a collapsed-by-default View Financial Details ledger before detailed history, and cumulative finance summary. Search/sorting/date controls/pagination must be practical, not an all-time unbounded default.

Initial roster is 12 accounts: one admin/provider, one reception-only account, ten therapist/providers. Provision privately, idempotently, preserving names/roles/aliases/order without public migration fixtures or default passwords. Support secure intended admin password setup and pending activation until authorized onboarding. Staff management is admin-only, shows identity/username/email/specialization/role/status, and supports therapist add/edit/deactivate/reactivate/reset/resend without permanent deletion or arbitrary role escalation. Deactivation revokes future session access, preserves records and flags future bookings for manual resolution; protect last active admin.

Authentication includes current-user endpoint, approximately 30-day configurable renewing sessions, safe shared-computer behavior, password change/reset/activation, forced initial setup, admin reset, CSRF and rate limiting. Secure HttpOnly session cookies and suitable SameSite are mandatory. No sensitive browser-local-storage authentication. Complete server/object/date enforcement applies to all endpoints and future reports/exports. See permissions.md for the full matrix.

Notification emails are generic, go only to affected therapists for material changes to published assignments and cover added/removed providers, moves, cancellations and group changes; no draft/no-op/unrelated notifications or sensitive email content. Durable transaction-safe outbox records recipient/event/state/attempts/error/times and bounded retries, without rolling back saves on provider failures. In-app notifications include persistent negative balances, publication reminders, operational warnings, unresolved status and a header indicator. Gmail API over HTTPS with official libraries, least-privilege gmail.send, offline OAuth, secure refresh/rotation and verified production token longevity is mandatory. Private initial sender is the owner-designated account, not the clinic administrator's account.

## Engineering, testing and release requirements

Required stack and domain/test/security rules are retained below and in source parts 19-24. Avoid microservices, Kafka, Kubernetes, Redis/message brokers without a compelling need. Preserve relational integrity, transactions, Django migrations, immutable financial/audit history and idempotency of bootstrap/completion/ledger/notifications/maintenance. PostgreSQL tests, deterministic frozen time and actual concurrent booking/financial tests are mandatory; SQLite cannot prove those guarantees.

Full test inventories (authorization, scheduling, completion, all fees/corrections, month/week histories, frequency changes, notifications/Gmail mocks, frontend/visuals and the **23-step acceptance scenario**) are preserved verbatim apart from privacy substitutions in master part 22, each mapped separately in coverage. CI must include appropriate lint/format, migrations, PostgreSQL tests, TS/build, frontend/browser, secret and copy checks, with synthetic data and no production credentials. No em dash in any visible copy, accessible keyboard/labels/dialog/focus/contrast/errors, responsive design and proper success/loading/empty/error/retry states.

Stage A uses free Pages/Render/Neon/Gmail HTTPS with provider-assigned HTTPS domains. Fixed same-origin proxy must forward methods/bodies/cookies/CSRF/Set-Cookie/redirects/status/content types safely and enforce origins/timeouts/no-store, with no open-proxy/backend-auth bypass. Backend sessions/data/secrets cannot depend on ephemeral disk. Cold-start interface preserves drafts, uses backoff/manual Retry, distinguishes availability/auth/permission/application failures, avoids exact restart promises and never blindly retries non-idempotent writes or guarantees stale financial data.

No synthetic keep-alive, paid pilot upgrade or externally recurring idle-prevention traffic. Use authorized-activity reconciliation and explicit bounded maintenance during pilot; document processing delays while sleeping. Production needs explicit Starter upgrade approval, current price verification (source estimate USD 7/month), preserving existing service/config/URLs, post-upgrade verification and further approval for a costlier tier based on measured need. Configure real authenticated idempotent business maintenance, preferably each minute if supported, with retries/logging/alerts and fallback reconciliation. Paid hosting does not schedule jobs automatically.

Actual deployed frontend/backend/proxy/login/cookies/CSRF/roles/booking/maintenance/cold-start/Gmail/secrets verification is required, not just a build. External account setup should be performed through available authorized integrations/APIs/browser, requesting only missing access/consent/2FA or sensitive/paid/destructive authorization; never request raw secrets in chat. Before real data: owner go-live approval, paid non-sleeping service, measured performance/memory, permissions/finance/background/email tests, encrypted external backups and successful restore, operational acceptance and clinic privacy responsibilities. No claim of legal compliance without evidence.

All original definition-of-done checks, architecture/documentation requirements and final-report fields remain mandatory and are linked in coverage. The former one-shot work cadence is replaced by issue-focused GitHub Flow and conventional commits; no assistant names in new project-authored branches/comments/docs/messages, no unapproved main merge, and progress/verification updates after every issue.

The private master specification and its Final Deployment Requirement Update are the source of authority. This public register deliberately excludes the private staff roster and the diary photograph. The deployment update takes precedence: Stage A is free, sleeping pilot hosting; Stage B needs approval for paid Starter compute and real-data launch. No synthetic keep-alive traffic is permitted.

## Functional acceptance

| Area | Required behavior | Evidence location |
|---|---|---|
| Identity | Exactly ADMIN, RECEPTIONIST, THERAPIST; distinct users/providers; pending activation; no public signup; persistent sessions; shared-computer logout; CSRF; throttled login; password reset/change | accounts, backend tests |
| Staff | Admin-only list/add/edit/deactivate/reactivate/reset; no deletion; preserve references; protect last admin; flag future inactive-provider bookings; private idempotent bootstrap of 12 accounts / 11 providers | accounts management, staff API/UI |
| Slots | IST; ten 45-minute slots 10:00 through 18:15; lunch 12:15 to 13:00; configured operating days | time_rules, scheduling tests |
| Catalog | OT, Sp. Edu., ABA, Group Therapy at INR 900; Assessment (2000), Assessment (2500), Assessment + Home Plan at INR 4500; backend-owned historical snapshots | catalog migration, fee tests |
| Booking | Ordinary exactly one child/provider; shared groups multiple children/providers; patient/provider conflict constraints across active sessions; concurrency-safe; cancelled reservations released; no hard-deleted sessions | scheduling, PostgreSQL tests |
| Attendance | Scheduled, Completed, Cancelled only; complete at end; per-child group attendance; durable catch-up; retries cannot duplicate charges | reconciliation tests |
| Corrections | Receptionist before 18:00 on appointment date; future editing still allowed; admin all-time; final slot ends 18:15; audit before/after/actor/reason | cutoff tests, audit |
| Publication | Day-level draft/published; current/next operational day; changes retain publication; therapists own assignments only; D+1 10:00 expiry; history separate; durable 18:30 reminder | publication tests |
| Schedule UI | Dense six-provider + five-provider tables; persistent order supplied by private bootstrap; ten rows; lunch divider; searchable patient chooser; inline patient creation; editable date/slot/therapy/providers/attendance; cancelled-history access without blocked cells; date navigation, Today, refresh, publication | Playwright and visual review |
| Therapist | Mobile own published assignments; shared group once; own completed history current/previous month; no fees, dues, financial marker or full patient access | API permission and browser tests |
| Patients | Stable IDs; duplicate names allowed; active status; search/edit; monthly completed/cancelled/category/provider breakdown; independently editable weekly/monthly plans with effective dates; expandable ledger; completed history | patient and frequency APIs/UI |
| Finance | Opening + payments + adjustments - completed charges; positive credit, negative dues; no monthly reset; exact paise; immutable ledger; reversal corrections; charge once per completed child/group; explicit accounting cutoff; special-fee marker for administration only | ledger and billing tests |
| Frequency | Monday-Sunday actual completed participation count; selected calendar month; independent expectations; monthly cancelled counts; searchable/sortable/editable; plan history | frequency tests/UI |
| History | Admin all time; receptionist current + prior two calendar months, future allowed; therapist own current + prior calendar month; cumulative ledger not subject to attendance cutoff | permission tests |
| Notifications | Dues alert on negative state, persistent until resolved; publication reminders; material published edits notify affected old/new providers; no-op suppression; generic emails without child data; durable retry outbox | notifications and outbox tests |
| Email | Gmail HTTPS API, gmail.send only; offline OAuth; encrypted refresh tokens; sender configurable privately; explicit test-email/staff-invitation consent; production token lifetime checked | integration verification pending |
| Frontend | React/TS/Vite/Tailwind/shadcn-style Radix primitives/TanStack Query/router; accessible labels/dialogs; role navigation; no em dash; branded cold start and retry; writes use persistent request idempotency keys | build, copy check, browser tests |
| Infrastructure | Cloudflare Pages Free + same-origin fixed proxy; Render Free + Gunicorn; isolated Neon development/pilot; production secure cookies and origin boundary; health and protected bounded maintenance; no pilot scheduler | deployment verification |
| Security | Public repository has only synthetic fixtures; no secrets/private roster/photos; server permissions; CSRF; safe logging; no-store; immutable audit; backups and restore before go-live | scan, tests, operational gate |
| Delivery | Logical commits, issue/branch/PR workflow; final main merge only with owner approval; CI; docs; independent review with truthful evidence | issue #1, verification register |

## Acceptance and launch gates

Run the full backend and browser suites and record the commands, results and limitations in verification.md. Verify the actual deployed frontend origin, cookies, CSRF, persistence, roles, scheduling and cold-start recovery. Check Gmail delivery only after authorization. Do not substitute a local test or successful build for deployed integration evidence.

Before real patient records: explicit go-live approval, approved paid Render Starter upgrade, actual business scheduler, measured memory/performance, encrypted backup and successful restoration, clinic operational acceptance, and privacy responsibilities confirmed. Paid service is not implied by pilot authorization.
