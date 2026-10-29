# Decisions, precedence and open conflicts

## Authority

Latest user scope controls the current issue. Phase 0A authorizes baseline inspection, public-source audit, bounded checks, branch rename, checkpoint publication, a draft PR and prioritized issues. Future implementation proceeds incrementally; no unrelated fixes or deployment are authorized by baseline preservation. The original complete product scope remains mandatory. The Final Deployment Requirement Update overrides conflicting master hosting/scheduler instructions. Complete sanitized sources and clause coverage are retained under sources/ and requirements-coverage.md. Code is implementation evidence, not authority to change a business rule.

## Finalized product decisions

| ID | Decision |
|---|---|
| D01 | Exactly three roles; separate users/providers; initial 12 logins/11 providers. Admin is schedulable, reception is not. Exact private spellings/aliases/order come from secure bootstrap. |
| D02 | Manual ordinary assignment: one child/provider. A shared group is one session with multiple child/provider assignments, per-child attendance, one provider-history count per group, one patient charge/count per completed child. |
| D03 | Exactly seven catalog fees/labels; backend owns prices and snapshots. Special-fee flag requires explicit review/adjustment, never an implicit discount. |
| D04 | IST fixed slots and lunch, exact 18:00 same-date reception cutoff, 18:15 final-slot end. Tomorrow's drafts remain editable after today's cutoff. |
| D05 | Only Completed attendance bills/counts. Cancelled history remains; reservations release appropriately; charges reverse audibly. No No-show state. |
| D06 | Append-only exact-money ledger; opening balance and explicit accounting cutoff; cumulative balance, auditable reversals, transactions/concurrency/idempotency. |
| D07 | Calendar-month history windows, not rolling days. Published daily visibility and completed-history scope are distinct. |
| D08 | Publication is day-level and persists after edits; material changes notify old/new affected therapists using generic authenticated-link email without child/financial details. |
| D09 | Persistent dues/publication reminders, missed-event recovery and durable retry outbox. Successful saves must not depend on email-provider availability. |
| D10 | Session authentication with CSRF/secure cookies; no public signup/JWT/local-storage secrets. Deactivation blocks access and preserves historical references. |
| D11 | Two stacked sections with six then five stable provider columns, ten rows each, lunch divider, compact readable laptop layout and mobile therapist portal. Diary is a layout/workflow reference only. |
| D12 | Free sleeping pilot with no synthetic keep-alive/paid upgrade. Approved production requires Starter, real maintenance scheduler, backups/restore, security/performance/clinic acceptance. Master §17.6 wake/reduce-spin-down and five-minute pilot traffic instructions are superseded. |
| D13 | Public repository with synthetic committed data only. Private roster/sender contacts, patient data, credentials, dumps and diary image never enter public history/artifacts/logs. |
| D14 | Phase 0A explicitly preserves the inherited uncommitted application and complete authoritative docs as one unverified checkpoint, followed by a publication/evidence commit. This preservation exception does not represent completed MVP acceptance or authorize large future feature commits. Issue #1 stays open; draft review and CI cannot authorize a main merge. Future issues require explanatory comments/docstrings for business invariants and complex choices. |

## Implementation choices and provisional assumptions

- Accounts plus clinic service modules implement the modular monolith, rather than one app per domain. PostgreSQL unique reservations, locks, ledger/audit immutability triggers and stored mutation responses are chosen mechanisms.
- React/TypeScript/Vite/Tailwind, TanStack Query, router and Radix dialog composition are present. Exact shadcn/ui adherence, accessibility and all browser behavior remain review work.
- A fixed Cloudflare Pages Function supplies a backend secret. Secure deployed cookies/CSRF are unverified.
- Monday-Saturday is a configurable initial operating-week assumption, not an original fixed requirement.
- 2026-10-28 is a provisional accounting setting, not owner approval of real-data cutoff/opening balances.
- Same-therapy restoration reuses the snapshot; category changes capture that category's fee at correction time. Test this documented interpretation.
- Neon Singapore was selected after Mumbai was unavailable for the account. This does not establish real-data hosting/legal suitability.
- Ambiguous email sends use uncertain/sending states rather than blind duplication. Complete investigation/recovery/alert handling remains incomplete.

## Open conflicts and static audit findings

| ID | Finding | Next treatment |
|---|---|---|
| C01 | Master §10.4 promises each day until D+1 10:00 and intends at most two days. Publishing tomorrow before 10:00 can expose yesterday/today/tomorrow. Current `therapist_visible` suppresses the oldest when two newer published dates exist, potentially expiring it early. | Preserve both statements. Obtain a focused business decision before altering this edge case; current choice is not approved policy. |
| C02 | Reminder says tomorrow's calendar date at 18:30; code uses next operating day and also checks today's missing schedule. Closed-day target/resolution is not finalized. | Test missed-evening recovery; clarify closed-day semantics where material. |
| C03 | `publish` calls appointment `editable`, potentially forbidding reception from publishing today's schedule after 18:00. Original cutoff explicitly concerns appointment corrections. | Review this coupling; do not treat it as a finalized publication restriction. |
| C04 | Earlier conversation claimed Windows browser launcher corrected. Current file still has slash-based relative executable syntax; Phase 0A isolated executable probe reproduced the Windows failure. | Repository controls current status. Tracked in #7; no application change during baseline preservation. |
| C05 | No dynamic unresolved header notification indicator found; navigation/page alone does not prove §16.6. Pending-change indication, list controls and visual cases remain incomplete/unverified. | Explicit UI acceptance backlog after backend stabilization. |
| C06 | Removed children remain cancelled, serializer returns all participations. Ordinary child replacement may produce several children on re-edit; date/category edits may alter retained cancellation reporting. | Static concern requiring meaningful regression tests, not a reproduced failure. |
| C07 | Frequency API checks Monday against history floor, potentially denying a permitted month-boundary week. All six cached backend failures were reproduced in Phase 0A PostgreSQL CI (42 passed, 6 failed). | Trace summaries are in verification.md and issues #2-#6; diagnose before fixing, and test C07 separately. |
| C08 | Session lifetime is hardcoded at approximately 30 days instead of configurable; operational delivery recovery/alerts, some table controls and full original test coverage are incomplete. | Keep explicit coverage gaps; no silent waiver. |

## Process override and final delivery

Original phases/reporting are preserved as scope/history, not authorization to deploy during baseline preservation. Final delivery must still report feature statuses, actual test commands/counts, Git/CI/deployment/onboarding/security evidence, known issues and clinic-acceptance verdict. Current verdict: **not ready**. All C01-C08 have explicit follow-up issues in [backlog](backlog.md); no policy is resolved merely by creating an issue.
