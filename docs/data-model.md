# Data model

User has one of three roles. Provider optionally belongs to one User; reception has no Provider. Patient names are not unique. FrequencyPlan records independent expected counts and their effective dates.

DailySchedule has a unique date and publication actor/time. Session references the day, fixed slot, catalog therapy, scheduled end and edit version. Assignment links providers. Participation links each patient once with Scheduled/Completed/Cancelled attendance, fee snapshot and billing revision.

ProviderReservation and PatientReservation have unique (resource, date, slot) keys. Cancelled participations have no patient reservation. Providers retain reservations while at least one participation remains active. Sessions and participations remain historical records.

LedgerEntry stores signed integer paise, effective/recording time, source, optional participation and unique reversal target. PostgreSQL triggers reject UPDATE/DELETE on ledger and audit records. Transactions append corrective entries. Patient locks serialize ledger changes with attendance corrections. Derived balances and counts are not cached mutable counters.

Notification keys identify unresolved dues or publication tasks. EmailOutbox event keys deduplicate delivery events, with encrypted activation payloads. IntegrationSecret holds encrypted OAuth refresh credentials. IdempotencyRecord binds actor, UUID key, payload digest and response. Historical foreign keys use PROTECT.
