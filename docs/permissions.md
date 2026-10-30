# Permissions

This is the intended complete authorization contract, not proof of current enforcement. Cached authorization/credential failures and publication conflicts are recorded in verification.md and decisions.md. The private administrator/reception identities are supplied at bootstrap, not hardcoded exceptions.

| Capability | Admin | Receptionist | Therapist |
|---|---|---|---|
| Daily schedule | All dates | Current month + previous 2; future allowed | Own published days only, until D+1 10:00 IST |
| Appointment writes | All dates | Before 18:00 on appointment date; future allowed | No |
| Publish | Current/next operational day | Current/next operational day | No |
| Completed history | All | Current + previous 2 months | Own current + previous month |
| Patients and frequency plans | Yes | Yes, scoped attendance | No |
| Ledger/payments/adjustments | Cumulative | Cumulative | No |
| Financial markers/notifications | Yes | Yes | No |
| Staff management/audit/OAuth sender | Yes | No | No |
| Own password/logout | Yes | Yes | Yes |

The server applies these policies to list and detail endpoints. Therapist serializers omit special-fee data. Account deactivation is checked by Django authentication on subsequent requests; changing the password invalidates other sessions. Credential setup has hashed single-use expiring tokens. Shared-computer sessions expire when the browser session ends.

## Detailed action matrix

| Action/data | Admin | Receptionist | Therapist | Unauthenticated |
|---|---|---|---|---|
| Login, obtain CSRF, request reset / consume valid setup token | Own eligible account | Own eligible account | Own eligible account | Public auth entry points only, rate-limited/CSRF protected as appropriate |
| Current identity, own logout/password change | Yes | Yes | Yes | Deny |
| All-provider daily grid/drafts | All dates | Current plus two prior months; future unrestricted | Deny | Deny |
| Own published daily assignments/child names/therapy/time/status | Yes through admin grid | Yes through clinic grid | Assigned session only within publication window | Deny |
| Shared Group Therapy details | Yes | Yes within attendance window | Own assigned group, relevant children; no unrelated sessions | Deny |
| Create/edit/move/reassign/cancel/correct appointments | All-time admin correction | Before 18:00 IST on session date; future drafts allowed | Deny | Deny |
| Correct final slot after its 18:15 completion | Yes | Deny | Deny | Deny |
| Publish current/next operational day | Yes | Yes; additional cutoff coupling in current code is unresolved C03 | Deny | Deny |
| Patient list/create/edit/status/profile | Yes | Yes; embedded attendance respects month cutoff | Deny | Deny |
| Patient completed/cancelled histories and category/provider counts | All-time | Current plus previous two calendar months | Deny full-patient access | Deny |
| Therapist histories | All providers/all dates | All providers within current plus previous two months | Own completed sessions in current plus previous month only | Deny |
| Frequency dashboard/expected plans/history | Yes | Yes, with scoped attendance | Deny | Deny |
| Opening balance/payments/manual adjustments/ledger corrections | Yes, audited | Yes, authorized audited entries | Deny | Deny |
| Cumulative balance and supporting old ledger | All-time | All-time as necessary, not limited by attendance window | Deny | Deny |
| Special-fee toggle/amber marker, dues page | Yes | Yes | Deny in UI AND payload | Deny |
| Financial/publication reminders and operational warnings | Yes | Yes | Deny admin/reception notifications | Deny |
| Staff list/add/edit/deactivate/reactivate/reset/resend | Yes; protect last active admin; no deletion/general role escalation | Deny | Deny | Deny |
| Full audit review, sender OAuth setup | Admin only | Deny | Deny | Deny |
| Maintenance trigger | Approved service secret or explicit authorized local operation; not ordinary role-based public access | Same | Same | Deny without valid service authorization |
| Health endpoint | Public lightweight health only | Public | Public | Public, no patient/session data |

Financial adjustments and staff actions remain auditable; operational role permission does not waive explicit owner consent for real invitations, test-email delivery, paid actions or production go-live. Personal profile edits beyond password are optional only when explicitly supported; they never permit role escalation. No public registration or staff deletion endpoint may be added.

## Timing and attack boundaries

Reception's history starts at the first day of the month two months before the current IST month; therapist completed history starts at the first day of the previous month. These are calendar months, not 90/60-day approximations. A therapist's expired daily page must be denied even if the same completed sessions remain visible through permitted own history. No arbitrary future draft exposure.

Published day D is visible upon publication until D+1 10:00 IST, with the original two-day maximum intent kept as unresolved C01. Do not turn that conflict into an undocumented early expiry rule. Reception appointment edits at/after 18:00 are denied for that day, without blocking tomorrow's draft. Administrator retrospective permission does not waive conflict, audit, financial or catalog invariants.

Apply checks to list/detail/nested resources, aggregates, search filters and future reports/exports. Test direct ID/date/provider manipulation, expired/unpublished/other-provider schedules and deactivated existing sessions. Do not serialize sensitive fields then merely hide them with CSS. Permission policy must be enforced by backend, not navigation. Credential setup requires eligible account, unexpired unused token and password validation; username/email changes never grant roles.
