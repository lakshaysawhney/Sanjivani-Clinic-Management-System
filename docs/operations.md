# Operations and launch gates

## Onboarding

Run `python manage.py provision_staff /secure/path/roster.json` using a private roster. Each row has username, full_name, email, role, optional specialization, display_name and display_order. The command is transactional/idempotent, avoids duplicate usernames and preserves existing credentials. Never commit the real roster. New users remain pending with unusable passwords. Staff invitations and test emails require owner authorization before sending to real addresses.

Configure the Gmail API, OAuth web client and exact callback `/api/auth/gmail/callback/`. Use gmail.send only, offline consent and the privately configured sender. The admin's Profile page starts OAuth. TOKEN_ENCRYPTION_KEY must be a separately stored Fernet key. Losing that key requires renewed sender consent. Google's external Testing consent mode normally expires Gmail refresh credentials in seven days; verify production publishing/verification requirements before uninterrupted operation. [Official OAuth policy](https://developers.google.com/identity/protocols/oauth2/).

## Recovery

`python manage.py maintain` or the protected maintenance POST performs bounded reconciliation and outbox work. Repeat until backlog is exhausted. No-op retries must not duplicate ledger entries. Pending outbox rows retry with bounded backoff. `uncertain`/stale `sending` rows need delivery investigation; do not reset them automatically without checking Gmail acceptance.

Deactivated providers' future appointments remain visible as operational warnings. Reception/admin reassign them explicitly. No staff deletion is supported. Inspect audit logs as administrator for retrospective corrections.

## Backup and restoration

Managed storage is not a tested backup. Before real-data launch, configure encrypted external PostgreSQL dumps with restricted access, retention and monitored failure alerts. Keep the encryption key in a different secret store. A restore drill must use a separate database, apply matching migrations, and compare account/provider counts, session participations, ledger totals and constraints. Verify that restored application authentication and reconciliation work. Do not test restoration against the live database.

A backup destination, retention agreement and actual successful restore evidence are still launch gates. Never publish backups, SQL dumps, screenshots containing real records, or secrets as CI artifacts. Neon branch history does not replace an independently retained backup.

## Privacy and clinic acceptance

Before collecting real children's data, the clinic must establish its legal basis and any required guardian consent, notices, access/retention/deletion processes, staff confidentiality controls, breach response, processor contracts and hosting-location review. Review commencement dates and applicable healthcare exemptions with qualified local advice; this software does not certify compliance. Consult [MeitY's DPDP Rules 2025 publication](https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa?pageTitle=Digital-Personal-Data-Protection-Rules-2025).

Owner acceptance must exercise normal/group bookings, replacement after cancellation, published reassignment, late corrections, opening balance/payment reversals, historical cutoffs, staff deactivation, final-slot administration, downtime recovery and notification delivery. Paid always-on compute, scheduler, restore drill and explicit go-live approval are mandatory before real patient import.
