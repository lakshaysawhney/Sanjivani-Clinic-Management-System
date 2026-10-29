# Development progress and handoff

## Phase 0A: baseline preservation, 2026-10-29 (Asia/Kolkata)

Current acceptance verdict: **not ready**. This is an **unverified baseline, not a completed MVP**. The owner authorized safe GitHub publication and bounded checks only. Application source was preserved, not regenerated or repaired. All 61 backend/frontend/script files in the initial candidate manifest remain byte-for-byte unchanged. Generated build metadata, private inputs, dependencies and reports stay ignored and on disk.

- Public origin and connected owner admin/push access refreshed and confirmed.
- Branch renamed in place to `feat/1-initial-mvp`, preserving the entire working tree. Starting HEAD: `f08921f`.
- Parent [issue #1](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/1) remains open. Checkpoint commit/push/draft PR are the next publication steps; actual identifiers will be recorded in the follow-up evidence commit.
- [Prioritized backlog](backlog.md): 13 issues, #2-#14, cover all six cached backend failures and C01-C08, acceptance/CI, deployment, private onboarding, backups and approved launch.
- Publication audit inspected all 85 initial eligible files (884,256 bytes), the sole historical README blob, private-source identity/credential overlap and the built client assets. No private/credential findings remained; public catalog text and the documented synthetic local database example were reviewed false positives. Ignore rules now also exclude build metadata, key containers and SQL/archive exports. Final staged-tree audit remains required before commit.
- Fresh lint/format/system/type/copy/build checks passed. npm audit completed with zero known vulnerabilities after a network-permission retry. Full application security and Python dependency vulnerability acceptance remain open.
- Backend: 48 collected; bounded run stopped with one database setup error, zero passed. Local Docker engine unavailable; PostgreSQL loopback target timed out after retry outside the sandbox. Migration drift check says no changes, but database history consistency is unverified.
- Browser: six scenarios listed, zero workflows executed. An isolated executable probe reproduced the current Windows launcher error (`'..' is not recognized`). No seed/server was launched against the existing development data.
- No merge, deployment, paid action, real invitation/email or production data operation occurred. CI and independent review remain publication/release gates.

Recommended **Phase 0B: [#2](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/2)**. Restore disposable PostgreSQL, reproduce all six cached failures with tracebacks, make focused fixes/regressions and retain a full final run at an exact revision. Keep publication business decisions separate.

See [verification](verification.md) for reproducible command/settings evidence and limitations. Private raw reports are retained under ignored `.private/phase0a/`; only sanitized summaries enter public history.

## Earlier consolidation snapshot (historical)

Snapshot: 2026-10-29, Asia/Kolkata. Current phase: documentation consolidation and incremental recovery planning. Broad MVP code exists. Current acceptance verdict: **not ready**. No application work is authorized by this documentation-only handoff.

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
