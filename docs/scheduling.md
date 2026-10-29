# Scheduling

Time zone is Asia/Kolkata. Slot starts: 10:00, 10:45, 11:30, 13:00, 13:45, 14:30, 15:15, 16:00, 16:45, 17:30. Each lasts 45 minutes. Lunch is a visual divider, not a slot. The default operating week is Monday-Saturday and is configurable.

Reception builds schedules manually. Shared groups are one session with several providers and children. Cancelling a child releases that child's reservation and reverses that child's charge if needed. If all children are cancelled, providers become available. Replacement bookings never delete cancellations.

Only completed participation counts or bills. Reconciliation persists completion at/after the ending time. It is bounded and retry-safe; read operations catch up before returning authoritative summaries. A session's effective end is preserved after sleep/restart.

Reception editing closes exactly 18:00 on the session date. Tomorrow remains editable that evening. The final slot ends 18:15, so only the administrator can correct it after completion. The interface must explain this operational restriction.

Publication applies to the day. Material changes create generic outbox notifications for both removed and newly assigned providers. No-op saves create no notification. Published state survives edits. Expired daily views are distinct from the permitted completed-history views.

Private provisioning supplies the requested provider display order; public fixtures use eleven synthetic provider names. Two tables show the first six and remaining five positions consistently across dates.
