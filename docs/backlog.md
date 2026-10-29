# Prioritized issue backlog

Created 2026-10-29 for Phase 0A, linked to parent [#1](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/1). The baseline is unverified and not a completed MVP. Priorities are sequencing guidance, not verification claims. Detailed acceptance criteria live in the issues.

| Priority | Issue | Scope / dependencies |
|---|---|---|
| P0 | [#2: Phase 0B: reproduce and stabilize the PostgreSQL backend baseline](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/2) | Recommended Phase 0B; restore disposable PostgreSQL and capture/fix all six cached backend failures. |
| P0 | [#3: Verify group billing, corrections and cancelled participation history](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/3) | After reproduction; group accounting, fee snapshots, reversals, cancellation/re-edit C06. |
| P0 | [#4: Verify session security, staff boundaries and mutation idempotency](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/4) | After reproduction; cached idempotency/staff and CSRF/deactivation failures; session lifetime C08. |
| P1 | [#5: Resolve publication visibility, reminder and correction-cutoff policies](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/5) | Owner policy resolution for C01-C03; cached publication/ownership failure. |
| P1 | [#6: Verify frequency and calendar-month boundary scopes](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/6) | Cached frequency/dues failure and month-boundary C07. |
| P1 | [#7: Repair Windows browser startup and isolate synthetic E2E data](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/7) | Windows launcher C04, disposable E2E setup, six existing scenarios. |
| P1 | [#8: Complete operational UI, header notifications and visual acceptance](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/8) | After browser harness; header indicator C05, pending forms/tables C08, laptop/mobile visuals. |
| P1 | [#9: Complete durable reconciliation and outbox recovery evidence](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/9) | Recovery/alerts C08; bounded reconciliation, generic outbox, uncertain sends. |
| P1 | [#10: Establish complete acceptance coverage and trustworthy CI](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/10) | All 23 acceptance steps, PostgreSQL concurrency, CI and independent review. |
| P2 | [#11: Verify free pilot deployment and actual-origin security](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/11) | After stabilization/access; actual-origin free sleeping pilot verification. |
| P2 | [#12: Verify private roster onboarding and Gmail OAuth delivery](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/12) | Private inputs/access plus applicable explicit invitation/test-email authorization. |
| P2 | [#13: Validate encrypted external backups, isolated restore and performance](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/13) | Encrypted storage/retention agreement, isolated synthetic restoration, measured performance. |
| P3 | [#14: Production readiness and owner-approved launch](https://github.com/lakshaysawhney/Sanjivani-Clinic-Management-System/issues/14) | All prior evidence plus separate paid-upgrade, merge and real-data go-live approvals. |

The six retained failure names are all tracked in #2: `test_group_attendance_and_billing` and `test_correction_reversal_and_fee_snapshot` also map to #3; `test_publication_ownership_expiry_and_payload` to #5; `test_frequency_and_dues` to #6; `test_idempotency_and_staff_boundaries` and `test_csrf_and_deactivation` to #4. They are historical cached failures, not six reproduced Phase 0A assertions. C01-C08 remain open in [decisions](decisions.md).

Each issue follows Issue → Branch → Tests/Implementation → Conventional Commits → Push → PR → CI → Review → Merge. Keep changes focused, preserve existing work, document business invariants and complex choices with meaningful comments/docstrings, and update progress/verification/clause coverage/relevant decisions at completion. No main merge without explicit owner approval. Phase 0A authorizes baseline preservation only; the backlog does not authorize executing later phases now.
