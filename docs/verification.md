# Verification evidence and failure register

## Phase 0B: PostgreSQL stabilization, 2026-10-29 (Asia/Kolkata)

Scope is [#2](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/2) on `feat/1-initial-mvp`, updating [Draft PR #15](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/pull/15). Complete clinic acceptance remains **not ready**. The Phase 0A results below are historical and are not the current backend verdict.

### Diagnosis and retained regressions

| Original failure | Established root cause | Resolution / evidence |
|---|---|---|
| `test_group_attendance_and_billing` | Client omitted the trusted-proxy header while pytest forced DEBUG=False; middleware returned 403 before history/profile logic | Model the proxy in API tests; original group history, per-provider count and per-child billing assertions now pass |
| `test_correction_reversal_and_fee_snapshot` | `order_by('-created_at').first()` could choose an already-reversed charge when creation times tied; the unique reversal link correctly rejected a second reversal | Select the participation's unreversed charge, retaining the constraint. Original snapshot/category-change test and new repeated ordinary/group correction cases pass |
| `test_publication_ownership_expiry_and_payload` | Same missing-header setup rejected even the authorized published schedule before visibility/ownership code | Original ownership, payload omission and exact D+1 expiry assertions now execute and pass; C01 policy remains unresolved |
| `test_frequency_and_dues` | Same proxy rejection returned Django JsonResponse, so `.data` failed before frequency assertions | Original actual/expected counts and dues-resolution assertions now pass; C07 month-boundary scope remains open |
| `test_idempotency_and_staff_boundaries` | Same proxy rejection prevented mutation processing | Original repeated-key, changed-payload conflict and staff denial assertions now pass; new concurrent same-key requests return the identical response with one audit/mutation record |
| `test_csrf_and_deactivation` | Same proxy rejection blocked CSRF-token acquisition; the initial 403 had not proved CSRF rejection | Trusted-proxy requests now exercise CSRF and session deactivation. Added real-session appointment-write CSRF rejection/success and no idempotency record on CSRF failure |

Production proxy/authentication code was not weakened to satisfy tests. New negative proxy cases reject missing, empty, incorrect or unconfigured credentials with DEBUG=False. Synthetic-test-only MD5 hashing speeds fixture creation; runtime settings retain Django's secure hashers. New financial tests compare original ledger rows unchanged, verify each reversal's participation and opposite amount, preserve the unaffected group child, and prove retries add no rows. Concurrent payment reversals append once and reject the second correction. The existing concurrent conflicting-booking test remains in the full suite.

### Local environment and commands

Windows PowerShell / CPython 3.13.3 / installed project dependencies; PostgreSQL 17 in a new `clinic-phase0b-postgres` container. Restricted-shell `docker info` could not see the Linux-engine pipe; `docker desktop start` also looked in an unavailable registry path. A host-level check instead showed Docker Desktop running and server 29.8.1. No engine reset, clinic-volume deletion or development-configuration change was necessary.

The container uses `postgres:17`, synthetic credentials, database `clinic_phase0b`, loopback `127.0.0.1:55432`, and no host/clinic volume. Tests use separately named disposable `test_clinic_phase0b_20261029` and `test_clinic_phase0b_regressions`. Configuration is explicit, never loaded from the private development wrapper: DEBUG=1 (pytest itself defaults to False), synthetic Django secret, accounting start 2026-10-01, local app origin, and empty Gmail/OAuth/encryption/maintenance/proxy environment values. API test fixtures set their own synthetic proxy secret. No cloud database or external email is contacted. Raw local JUnit reports and helper scripts stay ignored under `.private/phase0b/`.

| Command | Actual outcome |
|---|---|
| `python -m pytest -q --tb=short --junitxml=<private report>` in backend, after proxy test correction/new regressions but before production fix | **54 passed, 3 failed, 18 warnings in 188.18 s**; original correction test and both new repeated-correction cases fail with the unique reversal constraint |
| Same complete command after the billing fix | **57 passed, 0 failed, 18 warnings in 258.37 s**; includes all original 48 cases and nine added cases |
| Same complete command after the CI-origin regressions | **60 passed, 0 failed, 21 warnings in 180.93 s**; includes all original 48 cases and twelve added cases |
| `.venv/Scripts/python -m ruff check backend scripts` | Exit 0, all checks passed |
| `.venv/Scripts/python -m ruff format --check backend scripts` | Exit 0, 37 files already formatted |
| `python manage.py check` with disposable configuration | Exit 0, no issues (0 silenced) |
| `python manage.py makemigrations --check --dry-run` with disposable configuration | Initial 3-second connection-timeout warning is retained as incomplete evidence. Retry with 15-second timeout: exit 0, no changes detected, no migration-history warning |
| `git diff --check` | Passed; Windows line-ending conversion notices are not whitespace errors |

After local verification, `docker stop clinic-phase0b-postgres` stopped only this task's disposable container. It is retained for explicit restart with `docker start clinic-phase0b-postgres`; existing development volumes/configuration and cloud services are untouched.

The final 21 pytest warnings concern absent `backend/staticfiles/`; they are not suppressed. Backend tests apply migrations to disposable databases and exercise PostgreSQL immutability/uniqueness and transactions. They do not verify the deployed proxy, HTTPS cookies, Gmail delivery, backups, performance or all 23 acceptance steps. No SQLite substitution. No unrelated frontend implementation or local browser rerun is included.

### Repository protection

GitHub API creation/read-back confirmed active [ruleset 26135607](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/rules/26135607), matching only `refs/heads/main`. It requires a PR and an up-to-date `verify` check from GitHub Actions integration 15368, blocks deletion and non-fast-forward updates, requires zero approving reviews, and has no required reviewers/code-owner/last-push approval or bypass actors (`current_user_can_bypass=never`). The check name and app ID were inspected from existing check runs and `.github/workflows/ci.yml`; neither is invented. Feature-branch effective rules returned an empty list. The workflow now also runs Django system checks. Protection does not authorize a merge; owner approval is still required and PR #15 remains draft/unmerged. No automatic merge was enabled.

### Revisions, CI and review

- `cbf85c926a3fcee9ea71f83dae6e5325fc4007da`: trusted-proxy API test setup, explicit rejection/session/CSRF/deactivation regressions, synthetic-only fast hashing and scope documentation.
- `9c0e25a4313745a5c89bae38f93124ce9798f33d`: unreversed-charge lookup, financial/concurrency regressions and reservation invariant documentation.
- `048d02635a823dd6d92db470f0db12b010db64b0`: Django system checks in the existing CI job. The complete local 57-case passing worktree matches these committed backend files.
- `dbd59acbed43d5a1ad5878429f2fe3e11b8a6d9e`: CI browser-origin alignment and three additional accepted/rejected-origin cases. The complete final local run matches these backend files: **60 passed, 21 warnings in 180.93 s**.
- [CI run 40911705816](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/actions/runs/40911705816), job 123581104880, tested the PR merge checkout containing that exact pushed head on Ubuntu / Python 3.13.17 / disposable PostgreSQL 17.11. **57 passed, 18 warnings in 3.50 s**. Lint, formatting, Django system check, migration drift, frontend type/copy/build, public-source scan, disposable schema/seed and browser installation passed. Browser execution then reported **1 passed, 5 failed in 32.0 s**: login was correctly rejected because the browser Origin `http://127.0.0.1:5173` did not match the default trusted `http://localhost:5173`. This run is a failed overall workflow, not a green check.
- The corrective CI configuration explicitly sets APP_ORIGIN to Playwright's actual `127.0.0.1:5173` base URL. Three additional backend cases accept the configured browser origin and reject both localhost and a foreign origin; CSRF enforcement is retained. This is verification configuration, with no frontend feature implementation.
- [CI run 40913224430](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/actions/runs/40913224430), job 123586475933, is **fully green** for source head `dbd59acbed43d5a1ad5878429f2fe3e11b8a6d9e` against unchanged main `f08921f2fd8866058dee81eb94c53f017be125f4` (PR merge checkout `2a73bd33940b73909f5045741722fbd28ea1a08c`). Ubuntu / Python 3.13.17 / disposable PostgreSQL 17.11: **60 passed, 21 warnings in 3.38 s**. All 37 Python files pass formatting, lint passes, Django reports no issues, migration drift reports no changes, and disposable schema application succeeds. npm installation, type/copy/build, source scan and all **six Playwright scenarios in 9.1 s** pass. These limited browser scenarios are not the complete acceptance inventory or an independent screenshot/visual review. No deployed-origin, real email or backup verification is inferred.
- An independent read-only review found no actionable correctness, security, locking, architecture or regression-test issues in the scoped backend changes. The reviewer did not rerun tests independently; passing evidence comes from the executed local/CI runs.
- Follow-up review of the origin correction and its three cases also found no actionable issue; rejected origins remain unauthenticated despite a valid CSRF token. Public-source scan and whitespace validation passed. Documentation validation preserved all **1,156 unique clause IDs**, updated 27 targeted coverage rows and checked **1,232 local Markdown link targets** across the repository; 88 tracked files contain no private/environment entries.
- The initial local attempt using the unmodified baseline and secure hashing was interrupted before its final summary after the complete pre-fix and post-fix runs finished. No complete count or passing claim is inferred from that attempt. Baseline six-failure tracebacks are retained in the exact-revision Phase 0A CI evidence below; the later complete local red run separately reproduced the financial defect and both added regressions.

## Phase 0A bounded baseline checks, 2026-10-29 (Asia/Kolkata)

Verdict: **unverified baseline; not a completed MVP; not ready for clinic use**. The application/source checks below apply to the unchanged implementation preserved by Phase 0A checkpoint `9af1ee287807f13d04f517cc179e0d20f64d67db` on [feat/1-initial-mvp](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/tree/feat/1-initial-mvp) (parent `f08921f`). [Draft PR #15](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/pull/15) is open against main, unmerged; parent #1 remains open. Documentation-only publication follow-up does not change the application under test. Local source preservation comparison: 61 implementation files checked, zero changed/missing.

Environment: Windows PowerShell, Python 3.13.3, Node 22.15.0, npm 10.9.2; existing installed dependencies. No install, migration application, seed or external service provisioning. Commands used synthetic `DEBUG=1` settings, a nonproduction secret, accounting start `2026-10-01`, empty Gmail/OAuth/encryption/maintenance/proxy credentials and local app origin. Database target was verified loopback port 5433 with `connect_timeout=3`; pytest targeted newly named disposable `test_clinic_phase0a_20261029`. No private development wrapper or cloud/pilot/production database was used for these tests.

| Command (working directory) | Exit / actual result | Evidence and limits |
|---|---|---|
| `.venv/Scripts/python -m ruff check backend scripts` (root) | 0; all checks passed | Static lint only |
| `.venv/Scripts/python -m ruff format --check backend scripts` (root) | 0; 35 files already formatted | No formatting mutation |
| `python manage.py check` (backend, virtualenv interpreter) | 0; no issues, 0 silenced | Not authorization/accounting acceptance |
| `python manage.py makemigrations --check --dry-run` (backend) | 0; no changes detected, with RuntimeWarning | Database migration-history consistency check failed: connection timeout; not a complete migration validation |
| `python -m pytest --collect-only -q` (backend) | 0; 48 tests collected in 2.44 s | Collection only, not test passes |
| `python -m pytest -q --maxfail=1 --tb=short --junitxml=<ignored private report>` (backend) | 1; 1 setup error, 1 warning, 0 passed; stopped in 7.61 s (9.75 s process wall time) | `test_booking_conflicts_and_cancellation` never reached assertions; `django.db.utils.OperationalError: connection timeout expired` during disposable DB setup. Remaining 47 cases unexecuted. Six historical failures were reproduced separately in remote CI below |
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
- The existing `scripts/check_public.py` is a narrow tracked-file guard, not the whole audit; final index validation passed for 86 staged files, 13 ignore sentinels, 61 unchanged implementation files, 1,156 unique mapped clauses and 19 Markdown files/1,201 relative links. `git diff --cached --check` passed after correcting one added-document EOF blank line; the tracked-source guard passed. A post-checkpoint history scan checked 87 file revisions with zero findings. No production security certification or complete dependency/provenance review is claimed. Remaining security/CI evidence is tracked in #4/#10.

Final documentation follow-up validation also passed: 86 indexed files, 61 unchanged implementation files, 1,156 unique clause mappings, 19 Markdown files, 1,202 relative links and 13 ignore sentinels. No private/generated entries were indexed; application files match the checkpoint exactly.

## Publication and next work

Checkpoint `9af1ee287807f13d04f517cc179e0d20f64d67db` was committed and pushed; [draft PR #15](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/pull/15) targets main. Remote main is unchanged at `f08921f2fd8866058dee81eb94c53f017be125f4`. The working tree was clean immediately after checkpoint/push; publication evidence is a subsequent documentation-only commit. [CI run 40898371225](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/actions/runs/40898371225) completed with failure; exact job evidence is recorded below. A documentation-only follow-up does not alter the tested application, and its automatic CI status must be inspected separately rather than inferred from this run. Parent #1 is intentionally not closed; final merge requires explicit owner approval. [Backlog](backlog.md) covers all six retained failures and C01-C08. Recommended next: [Phase 0B / #2](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/2), with an available disposable PostgreSQL database and retained full-run evidence. No future issue is implemented by this checkpoint.

## Checkpoint CI: complete backend run, failed

[Clinic verification run 40898371225](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/actions/runs/40898371225), job [123533600467](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/actions/runs/40898371225/job/123533600467), tested checkpoint `9af1ee287807f13d04f517cc179e0d20f64d67db` for draft PR #15. Ubuntu runner, CPython 3.13.17, disposable PostgreSQL 17.11 with synthetic CI configuration; no private roster or production credentials. Completed 2026-10-29 at approximately 20:38 IST.

- Dependency installation, backend lint, formatting and migration dry-run passed.
- `pytest -q`: **6 failed, 42 passed, 12 warnings in 27.19 s**, exit 1. All six retained historical failures are now reproduced on a committed revision. This supersedes the earlier lack of trusted counts/tracebacks; local setup remained blocked independently.
- The 12 warnings report missing `backend/staticfiles/` in the test environment. No browser/visual acceptance follows from backend passes.
- Workflow stopped at pytest. Node setup, npm install/check/build, public-source guard, development schema/seed and Playwright install/scenarios were **skipped**, not passed. Local frontend checks/audit remain separate evidence.

| Reproduced failing test | Observed failure at this revision | Follow-up |
|---|---|---|
| `test_group_attendance_and_billing` | HTTP 403 where 200 expected in history API assertion | #2/#3; inspect API/proxy test boundary |
| `test_correction_reversal_and_fee_snapshot` | `IntegrityError`: duplicate key violates `clinic_ledgerentry_reverses_id_key` while creating a charge reversal | #2/#3; diagnose reversal/snapshot history |
| `test_publication_ownership_expiry_and_payload` | HTTP 403 where 200 expected | #2/#5; preserve C01-C03 policy questions |
| `test_frequency_and_dues` | `AttributeError`: `JsonResponse` has no attribute `data`, after forbidden API response | #2/#6; distinct from untested C07 boundary |
| `test_idempotency_and_staff_boundaries` | Session mutation returned HTTP 403 where 200 expected | #2/#4 |
| `test_csrf_and_deactivation` | `AttributeError`: `JsonResponse` has no attribute `data` for forbidden CSRF response | #2/#4 |

These are observed symptoms, not final root-cause diagnoses or authorization to weaken runtime security. No application fixes were made. Full CI job output is also retained locally in ignored `.private/phase0a/ci-checkpoint.txt`; only the above sanitized trace summary is committed. Passing the remaining 42 tests does not complete the original acceptance inventory. Phase 0B is #2.

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
