# Development progress and handoff

## Issue #3: participation history and financial correctness, completed 2026-10-30 (Asia/Kolkata)

Scope: [issue #3](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/3), continuing `feat/1-initial-mvp` and [Draft PR #15](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/pull/15). Clinic-use verdict remains **not ready**. No later backlog issue is authorized by this work.

- Reproduced and fixed C06: ordinary replacement serialized retired children back into the edit form; cancellation reporting followed the mutable session's date/time/category/providers. Membership now distinguishes retired cancellations, and cancellation context plus attendance date survive later shell edits. Daily and patient histories and monthly cancellation counts use that context. Restoration reuses the participation and reconciles the old cancellation count.
- Reproduced and fixed equally priced category corrections leaving the original charge active, and completed moves retaining the old effective charge time. Corrections append exact reversals and replacement charges even when the amount is unchanged. Same-therapy restoration retains the historical fee; no immutable ledger or audit row is overwritten.
- Reproduced and fixed reception restoring a retired cancellation after its original cutoff by using a future session shell. Both the current appointment and the original cancellation date are checked. Tomorrow's ordinary drafts remain editable; final-slot completed corrections require admin.
- Added PostgreSQL coverage for ordinary replacement/re-edit, group membership/counts/charges, released reservations and failed-restoration rollback, repeated cancellation moves/restoration, exact paise/accounting cutoff, effective-time/category lineage, real correction writes at 17:59:59/18:00/18:15, concurrent ordinary/group corrections/payments/retries and a legacy-schema migration. Existing tests are preserved. Added two real-browser scenarios; no working module was rewritten. The final interrupted chronology regression also reproduced incorrect ordering after a cancellation move; history now sorts by frozen attendance date/slot.
- Migration `0003_participation_history` backfills only context still stored in legacy rows. It cannot reconstruct already-overwritten cancellations or infer every old removed group member; ambiguous legacy data needs owner review before any operational migration. Only disposable synthetic PostgreSQL databases are used here.
- Final local PostgreSQL: **84/84 passed**; GitHub Actions [41062087073](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/actions/runs/41062087073) is green on `8a7643c18e5a512a1326c6708f994c1892948113`, with **84 backend tests and all eight browser scenarios passing**. Windows default browser run passed six scenarios and failed two login waits; these failures are retained separately.
- Exact executed counts, revisions, failures, CI and review evidence are in [verification](verification.md). C06 is addressed for subsequent writes; C01-C05/C07-C08, Windows launcher #7, full original acceptance, deployed security, email and backups remain separate work. No merge, deployment, paid service, real invitation/email or operational data operation occurred.

## Phase 0B: backend stabilization and repository protection, 2026-10-29 (Asia/Kolkata)

Scope: [issue #2](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/2), continuing `feat/1-initial-mvp` and [Draft PR #15](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/pull/15). The application is preserved. Clinic-use verdict remains **not ready**; backend stabilization is separate from complete acceptance and deployment.

- Five baseline API failures came from incorrect test setup: pytest disables DEBUG, so the production proxy boundary rejected requests without its shared header before role, object, frequency, CSRF or mutation logic ran. Tests now model the trusted proxy and separately prove untrusted requests are rejected. Production authentication and proxy enforcement were not relaxed.
- The financial defect selected a previous charge using timestamp order. Identical timestamps could select an already-reversed charge and violate the one-reversal constraint. Reconciliation now selects the unreversed charge; immutable history, historical snapshots, revision source keys and session/patient locking remain intact.
- Added twelve cases covering missing/invalid/unconfigured proxy credentials, session CSRF for login and appointment writes, accepted/rejected browser origins, deactivation, repeated ordinary/group corrections with tied timestamps, concurrent identical mutations and concurrent payment reversals. Runtime password hashing remains secure; synthetic tests explicitly use fast hashing.
- Restored disposable PostgreSQL 17 through host-level Docker access. Restricted-shell Docker metadata/pipe failures were an environment boundary, not proof the engine was stopped. A separate loopback-only container on port 55432 has no mounted clinic volume and uses synthetic data. No Neon/pilot/production database was used.
- Complete final local run: **60 passed, 0 failed, 21 warnings in 180.93 s**. Earlier post-fix run: **57 passed in 258.37 s**. Pre-fix expanded run: **54 passed, 3 failed in 188.18 s**, isolating the original financial failure and both new correction regressions after the proxy fixture correction. Lint, formatting (37 files), Django system check and migration drift/history retry passed. Exact commands, limitations and revision evidence are in [verification](verification.md).
- Pushed source/configuration revision `dbd59acbed43d5a1ad5878429f2fe3e11b8a6d9e`. [CI run 40913224430](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/actions/runs/40913224430) is fully green: **60 backend cases in 3.38 s** and **six browser scenarios in 9.1 s**, plus lint/format/system/migration/type/copy/build/source checks. The preceding CI run passed 57 backend cases but exposed a browser CSRF origin mismatch; setting CI APP_ORIGIN to Playwright's actual loopback origin resolved it without relaxing security. Independent read-only reviews found no actionable issues. Main remains `f08921f2fd8866058dee81eb94c53f017be125f4`.
- Active [main ruleset 26135607](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/rules/26135607): PR required; GitHub Actions `verify` required and up to date; zero approvals; force pushes/deletion blocked; no bypass actors. Feature branch has no effective rules. No automatic merge was enabled.
- C01-C03 and C06-C08 remain open; passing the baseline publication/frequency cases does not settle their edge cases. The Windows browser launcher and full UI/deployed-origin/email/backup acceptance remain separate issues. Recommended next: [#3](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/3), focusing on cancelled-participant re-edit/history C06 and the remaining financial acceptance inventory.

No merge, deployment, paid service, real staff invitation/email or operational data change is part of this issue. The historical snapshots below remain evidence of their own revisions.

## Phase 0A: baseline preservation, 2026-10-29 (Asia/Kolkata)

Current acceptance verdict: **not ready**. This is an **unverified baseline, not a completed MVP**. The owner authorized safe GitHub publication and bounded checks only. Application source was preserved, not regenerated or repaired. All 61 backend/frontend/script files in the initial candidate manifest remain byte-for-byte unchanged. Generated build metadata, private inputs, dependencies and reports stay ignored and on disk.

- Public origin and connected owner admin/push access refreshed and confirmed.
- Branch renamed in place to `feat/1-initial-mvp`, preserving the entire working tree. Starting HEAD: `f08921f`.
- Parent [issue #1](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/1) remains open. Checkpoint `9af1ee287807f13d04f517cc179e0d20f64d67db` is committed and pushed on [feat/1-initial-mvp](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/tree/feat/1-initial-mvp); [draft PR #15](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/pull/15) targets main. The PR is open, draft and unmerged. Main remains `f08921f2fd8866058dee81eb94c53f017be125f4`; no history rewrite occurred. Publication evidence is maintained in a documentation-only follow-up on the same branch.
- [Prioritized backlog](backlog.md): 13 issues, #2-#14, cover all six cached backend failures and C01-C08, acceptance/CI, deployment, private onboarding, backups and approved launch.
- Publication audit inspected all 85 initial eligible files (884,256 bytes), the sole historical README blob, private-source identity/credential overlap and the built client assets. No private/credential findings remained; public catalog text and the documented synthetic local database example were reviewed false positives. Ignore rules now also exclude build metadata, key containers and SQL/archive exports. Final index validation passed: 86 files, zero private/generated entries, 13 ignore sentinels, 19 Markdown files/1,201 relative links, and all 1,156 unique source clauses mapped. `git diff --cached --check` and the tracked-source guard passed; post-checkpoint history scan covered 87 file revisions with zero findings.
- Fresh lint/format/system/type/copy/build checks passed. npm audit completed with zero known vulnerabilities after a network-permission retry. Full application security and Python dependency vulnerability acceptance remain open.
- Local backend: 48 collected; bounded run stopped with one database setup error, zero passed. Separately, remote disposable-PostgreSQL CI executed all 48 cases: 42 passed, 6 failed. Local Docker engine unavailable; PostgreSQL loopback target timed out after retry outside the sandbox. Migration drift check says no changes, but database history consistency is unverified.
- Browser: six scenarios listed, zero workflows executed. An isolated executable probe reproduced the current Windows launcher error (`'..' is not recognized`). No seed/server was launched against the existing development data.
- No merge, deployment, paid action, real invitation/email or production data operation occurred. [CI run 40898371225](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/actions/runs/40898371225) completed with failure against the checkpoint on Ubuntu/Python 3.13.17/PostgreSQL 17.11: **42 passed, 6 failed, 12 warnings in 27.19 s**. All six cached failures were reproduced; lint/format/migration drift passed. Later frontend/browser/source-scan steps were skipped. The documentation-only follow-up may trigger another CI run; this result is pinned to the application checkpoint. Independent review and passing acceptance remain open.

Recommended **Phase 0B: [#2](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/2)**. Restore local disposable PostgreSQL, diagnose the six failures now reproduced in CI, make focused fixes/regressions and retain a full final run at an exact revision. Keep publication business decisions separate.

See [verification](verification.md) for reproducible command/settings evidence and limitations. Private raw reports are retained under ignored `.private/phase0a/`; only sanitized summaries enter public history.

## Earlier consolidation snapshot (historical)

Snapshot: 2026-10-29, Asia/Kolkata. Historical phase: documentation consolidation and incremental recovery planning. Broad MVP code exists. Current acceptance verdict: **not ready**. No application work is authorized by this documentation-only handoff.

## Implemented and verified within limited evidence

- Prior session verified correct public repository/remote and connected owner admin/push permissions.
- Dependencies installed; initial schema/catalog/immutability migrations applied to isolated Neon development and local PostgreSQL 17.
- Earlier frontend production build, TypeScript/copy checks and Django system check passed. Backend lint later reported all checks passed. These prove those command outcomes, not every feature or the latest working tree.
- Neon Free pilot/development branches created; Docker PostgreSQL reached healthy state. No production readiness follows from this.

## Implemented but unverified or partial

Backend code covers session/CSRF/roles, activation/reset, staff/provider management, patient/frequency records, reservations, ordinary/shared groups, cancellation, completion/reconciliation, publication/date scopes, ledger/audit, dues, idempotency, Gmail OAuth/outbox and maintenance.

Frontend code covers role navigation, account screens, 6+5 timetable, inline patient creation, appointment/group/status editing, publication, therapist portal/history, patient summaries/ledger, payments/reversals, frequency/dues/notifications/staff and cold-start retry. Readability, accessibility, pending changes, dense schedules and all workflows remain unverified.

Proxy, security headers, Render Free blueprint, CI workflow and scan scripts exist as configuration, not verified deployments or successful CI.

## Missing/incomplete features and deliverables

- Passing full backend suite with retained reports and original comprehensive coverage, including all 23 acceptance steps.
- Working/passing Windows browser harness and visual evidence for target laptops/mobile, full/empty/mixed/cancelled/long-name schedules.
- Verified header notification indicator, configurable session lifetime and remaining table/error/pending-change requirements; see C05/C08.
- Sender cloud setup, durable OAuth/refresh verification and authorized actual delivery.
- Cloudflare/Render deployment and actual-origin cookie/CSRF/role/sleep-recovery verification.
- Real 12-account/11-provider bootstrap with exact private display order and authorized activation; no real staff invitations confirmed.
- Encrypted external backups, storage/retention agreement and successful separate-database restoration.
- Logical implementation commits, push, PR, CI and final review.
- Production Starter upgrade/scheduler and real-data go-live are intentionally approval-gated.

## Known failures and concerns

Six backend test names are marked failed in the retained pytest cache; verification.md lists them. No final trusted count/traceback was retained. Browser last-run says failed; observed startup error concerns Windows executable paths. Current file does not substantiate the earlier correction claim.

Read decisions C01-C08 before policy-sensitive fixes. Visibility cutoff versus two-day limit, reminder target, publication cutoff coupling and cancelled-participant re-edit behavior need explicit treatment. Static concerns are not presented as reproduced failures.

## External authorization blockers

Neon connected/configured previously. Render connection requested but unconfirmed. Prior discovery found no matching Cloudflare integration; signed-in authorized browser setup is needed. Owner said they would sign in and then allow setup, without recorded completion confirmation. Google Cloud/Gmail sender setup/consent remain unconfirmed; a chat email connection would not itself authorize the application's OAuth client. Scheduler access is needed only when production scheduling is in scope. No external setup performed in this audit.

## Current Git state

- Origin: https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System.git
- HEAD `f08921f` (initial commit); no implementation commits in local history.
- Current inherited implementation branch: retrieve exact historical name with `git branch --show-current`. Its assistant-name prefix must not be adopted as a future project naming convention. No branch rename in this audit.
- Before handoff: README modified; application/tests/config/scripts/docs/AGENTS untracked. Private files/dependencies ignored.
- Issue: https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/1
- No implementation push, PR, merge or CI result confirmed. No staging/commit/branch mutation in this task. Untracked/ignored local files do not travel to a fresh clone.

## Latest testing results

See verification.md for commands/outcomes. This audit only inspected source/artifacts; no tests, builds, seeds, migrations or database calls were run. Old execution sessions are unavailable. Test source is not pass evidence. Reproduce failures against disposable PostgreSQL and retain output during the next authorized implementation issue.

## Next recommended task

Open a focused backend stabilization issue: reproduce/capture the six cached failures using isolated PostgreSQL, diagnose/fix with meaningful regressions, and retain a full final run with counts/revision. Keep C01's business ambiguity separate from routine debugging. Next, repair Windows browser startup in a small issue, run workflows and review laptop/mobile layouts. Close coverage gaps before deployment setup.

Review privacy exclusions and split the inherited working tree into logical conventional commits and PRs when Git publication is in scope. This documentation audit does not stage/commit unrelated code.

## Milestone history

| Milestone | Outcome |
|---|---|
| Discovery | README-only repository and owner access verified; issue and inherited implementation branch created. |
| Foundation | Python/pip repaired, dependencies installed, Neon pilot/development in Singapore, Docker PostgreSQL started. |
| Implementation | Broad backend/frontend/CI/deployment code written; not accepted as a complete MVP. |
| Initial verification | Specific migration/build/type/copy/system/lint commands passed; backend failures/browser startup remained. |
| Review edits | Reminder recovery and visibility code changed without complete final verification; launcher-fix claim conflicts with current file. |
| Summary checkpoint | Owner requested status; no completed deployment/readiness claimed. |
| Handoff 2026-10-29 | Sanitized complete sources, clause coverage, decisions/conflicts, failure names and incremental workflow consolidated. No application changes. |

## Handoff validation evidence

- Preserved and mapped 1,129 master source blocks and 27 deployment amendment blocks: 1,156 unique clause IDs, with no missing/duplicate source-to-matrix mapping.
- Checked 18 public Markdown documents for relative link/anchor resolution and supplied private contact/assistant-name exclusions; no issues found at validation.
- Exact private source copies are excluded by Git ignore rules. Public sources use stable identity substitutions rather than exposing bootstrap contacts.
- Snapshotted 62 application/test/script files for a final unchanged-content comparison. No implementation or database validation was run as part of this audit.
- `git diff --check` passed for tracked changes. Most application and documentation files remain untracked; this check alone does not cover their contents. Dedicated document validation also checked their structure/privacy/links.
- Documentation remains local and uncommitted. No push/PR/merge/deploy/data changes were performed.
