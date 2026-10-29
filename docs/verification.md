# Verification evidence and failure register

## Phase 0A bounded baseline checks, 2026-10-29 (Asia/Kolkata)

Verdict: **unverified baseline; not a completed MVP; not ready for clinic use**. The application/source checks below apply to the unchanged implementation preserved by the forthcoming Phase 0A checkpoint on `feat/1-initial-mvp` (parent `f08921f`). The actual checkpoint SHA, draft PR and CI evidence will be added after publication. Local source preservation comparison: 61 implementation files checked, zero changed/missing.

Environment: Windows PowerShell, Python 3.13.3, Node 22.15.0, npm 10.9.2; existing installed dependencies. No install, migration application, seed or external service provisioning. Commands used synthetic `DEBUG=1` settings, a nonproduction secret, accounting start `2026-10-01`, empty Gmail/OAuth/encryption/maintenance/proxy credentials and local app origin. Database target was verified loopback port 5433 with `connect_timeout=3`; pytest targeted newly named disposable `test_clinic_phase0a_20261029`. No private development wrapper or cloud/pilot/production database was used for these tests.

| Command (working directory) | Exit / actual result | Evidence and limits |
|---|---|---|
| `.venv/Scripts/python -m ruff check backend scripts` (root) | 0; all checks passed | Static lint only |
| `.venv/Scripts/python -m ruff format --check backend scripts` (root) | 0; 35 files already formatted | No formatting mutation |
| `python manage.py check` (backend, virtualenv interpreter) | 0; no issues, 0 silenced | Not authorization/accounting acceptance |
| `python manage.py makemigrations --check --dry-run` (backend) | 0; no changes detected, with RuntimeWarning | Database migration-history consistency check failed: connection timeout; not a complete migration validation |
| `python -m pytest --collect-only -q` (backend) | 0; 48 tests collected in 2.44 s | Collection only, not test passes |
| `python -m pytest -q --maxfail=1 --tb=short --junitxml=<ignored private report>` (backend) | 1; 1 setup error, 1 warning, 0 passed; stopped in 7.61 s (9.75 s process wall time) | `test_booking_conflicts_and_cancellation` never reached assertions; `django.db.utils.OperationalError: connection timeout expired` during disposable DB setup. Remaining 47 cases unexecuted. Six historical cached failures remain unreproduced |
| `npm.cmd run check` (frontend) | 0; TypeScript and UI copy passed | 38.09 s process wall time; copy scanner scope is limited |
| `npm.cmd run build` (frontend) | 0; Vite 7.3.7, 1696 modules transformed | 42.97 s process wall time; client JS 380.66 kB, CSS 16.97 kB; no browser/deployed proof |
| `npm.cmd run test:e2e -- --list` (frontend) | 0; six tests in one file | 9.72 s; zero scenarios executed, no visual acceptance |
| `cmd.exe /d /c "../.venv/Scripts/python.exe --version"` (frontend) | 1; `'..' is not recognized as an internal or external command` | Isolated reproduction of current launcher syntax; no server, seed or private config loaded |
| `npm.cmd audit --json --ignore-scripts` (frontend) | 0 after network retry; 0 info/low/moderate/high/critical, 193 dependencies reported | First sandbox request failed DNS resolution; final registry advisory response empty. No dependency changes. This does not audit Python packages or prove package provenance |
| `docker compose ps --format json` (root) | 1; Docker Linux engine named pipe absent | Local database unavailable; no infrastructure startup or cloud fallback |

Initial sandbox DB attempts failed with Windows socket permission error 10013. A bounded retry with network access instead timed out; the final result above is an environment/setup blocker, not a reproduced business assertion. Raw command output/JUnit and manifests remain private in ignored `.private/phase0a/`; summaries here contain no credentials. Existing test/cache artifacts may now reflect the setup error, so the six historical names below are deliberately retained.

## Phase 0A public-repository audit

- Threat boundary reviewed: private bootstrap/configuration and generated artifacts must never cross into the public index/history, PR, issue text, CI logs or browser bundle.
- Enumerated every eligible file before staging; initial inventory 85 UTF-8 files, 884,256 bytes. Inspected settings/templates, migrations, test/demo identities, auth/OAuth/email/proxy code, deployment/CI config, documentation/sanitized sources and dependency manifests/lockfile. No binary patient/diary artifact is eligible.
- Scanned eligible content and the existing one-commit history for credentialed database URLs, private keys, provider token formats, JWT literals and nonsynthetic email literals. Compared against 29 local private contact/name/configuration terms without printing them, and scanned freshly built client assets. No unresolved findings. Two reviewed overlaps were public catalog text and the documented synthetic local database example.
- Synthetic test credentials and loopback-only database examples in `.env.example`, compose and CI were reviewed as nonproduction fixtures. Runtime bootstrap has no shared default password; new accounts use unusable passwords and activation.
- `.private/`, all real `.env` variants, dependency/cache/build/test-output directories and database dumps stay ignored. Added credential-container, SQL/archive and TypeScript metadata exclusions without deleting existing files. `.env.example` alone remains eligible as a placeholder template.
- The existing `scripts/check_public.py` is a narrow tracked-file guard, not the whole audit; staged-tree check, ignore verification, source preservation and final history scan will be recorded after staging/publication. No production security certification or complete dependency/provenance review is claimed. Remaining security/CI evidence is tracked in #4/#10.

## Publication and next work

Checkpoint/push/draft PR and remote CI are pending at this precommit snapshot. Parent #1 is intentionally not closed; final merge requires explicit owner approval. [Backlog](backlog.md) covers all six retained failures and C01-C08. Recommended next: [Phase 0B / #2](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/2), with an available disposable PostgreSQL database and retained full-run evidence. No future issue is implemented by this checkpoint.

## Historical verification before Phase 0A

Consolidated 2026-10-29 (Asia/Kolkata). This documentation audit ran no application tests, builds, migrations, seeds or deployments. Below are historical observed outputs and currently retained artifacts, not fresh test results. HEAD is f08921f; application implementation remains uncommitted, so no implementation revision pins the prior results. Later edits are not covered automatically.

## Observed command-level evidence

| Command/check | Environment | Observed outcome | Limits |
|---|---|---|---|
| Repository remote/status/history and connected metadata | Windows checkout and GitHub connection | Correct public origin and owner admin/push access; original clean README-only main | Service permissions not refreshed in this audit |
| Runtime checks | Windows | Python 3.13.3, Node 22.15.0, npm 10.9.2 | Discovery only |
| pip install and npm install | Local dependencies | Installed; npm reported 122 packages added and zero vulnerabilities | Install-time audit, not comprehensive security evidence |
| Initial makemigrations/migrate --noinput via development wrapper | Isolated Neon development | Accounts/clinic schema, catalog, immutable ledger/audit trigger migrations OK | No production migration; no accounting correctness proof |
| migrate --noinput after local database switch | Docker PostgreSQL 17 | Initial migrations OK | Subsequent seed completion not independently confirmed |
| Docker info / compose status | Local engine/container | Engine available and PostgreSQL healthy on loopback port 5433 | Historical health, not current availability guarantee |
| npm run build | frontend | TypeScript and Vite build succeeded; 1696 modules transformed | Earlier tree state; not deployed/browser verification |
| npm run check | frontend | TypeScript and UI-copy check passed | Scanner scope still needs review against all backend/error/notification copy |
| manage.py check via development wrapper | Backend | System check identified no issues | Not business acceptance or production security proof |
| ruff check backend scripts --fix; ruff format | Backend/scripts | Earlier lint errors; later output reported All checks passed and formatting performed | No final CI or format --check result established |
| .venv/Scripts/python scripts/dev.py -m pytest -q --reuse-db | Isolated PostgreSQL test configuration | Failure progress observed; six names retained in cache | Final count, duration and tracebacks unavailable; no full pass claimed |
| Backend suite with -x after local database switch | Local disposable test configuration | Attempt started after migrations | Completed result unavailable |
| .venv/Scripts/python scripts/browser_tests.py | Windows local app | Initial startup failed because relative executable was interpreted as '..' command; later attempt started | No successful workflow result. Current launcher still has slash-based relative executable syntax; earlier fix claim is not substantiated |

## Retained failure names

Existing backend/.pytest_cache/v/cache/lastfailed records:

1. tests/test_clinic.py::test_group_attendance_and_billing
2. tests/test_clinic.py::test_correction_reversal_and_fee_snapshot
3. tests/test_clinic.py::test_publication_ownership_expiry_and_payload
4. tests/test_clinic.py::test_frequency_and_dues
5. tests/test_clinic.py::test_idempotency_and_staff_boundaries
6. tests/test_clinic.py::test_csrf_and_deactivation

These names establish recorded prior failures, not causes, current reproducibility or final suite totals. Do not guess a fix from a name. Old execution sessions were unavailable when read during this audit. Reproduce and retain tracebacks during the next implementation issue.

frontend/test-results/.last-run.json says status failed, with an empty failedTests array. It proves no scenario passed. No successful screenshot review, complete E2E report or visual acceptance evidence was found during this audit.

## Test source is not pass evidence

Backend tests exist for conflicts/cardinality, seven fees/end boundaries, groups, charge corrections, opening/payment validation, ledger immutability, cutoff/final slot, calendar scope, therapist forbidden APIs, publication ownership/expiry/recipients, reminders, frequency/dues, idempotency, CSRF/deactivation, concurrent booking, outbox and maintenance auth. Test fixtures use a fast test-only hasher; runtime retains secure default hashing.

Browser source covers a reception patient/plan/payment/booking/publication workflow, two laptop layouts, mobile therapist/history isolation, outage screen and admin navigation. Full original browser coverage and all 23 acceptance steps are not established. Editing/cancellation/group/correction, financial concurrency, notification failure/retry and full/empty/mixed/long-name visual cases still need complete proof. Consult source master part 22 and the clause matrix.

## Unverified integration and release gates

- Actual Pages/Render URLs, same-origin proxy, cookies/session renewal, CSRF success/rejection, role scopes, routing, booking and cold-start recovery.
- Gmail cloud/consent setup, correct private sender authorization, durable refresh, actual authorized send/delivery and operational retry/error handling.
- Real roster bootstrap/activation and exact provider ordering; no real invitations confirmed sent.
- Encrypted external backups, retention/failure alerts and successful isolated restore; backend memory/performance measurements.
- Passing CI, complete public-history/client-bundle secret review and independent final review.
- Approved production Starter upgrade, real business scheduler, clinic acceptance and go-live. These are gated, not failed pilot features.

No real patient import is recorded. Verdict: not ready.

## Documentation-only validation

The handoff validates source-block coverage, document links, private contact/name exclusion, ignored private archives and unchanged application-file hashes during the write phase. These checks do not verify product behavior. Final counts/outcomes are recorded in progress.md.
