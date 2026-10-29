# Decisions and assumptions

Historical implementation assumptions. The authoritative consolidated register is [decisions.md](decisions.md), especially C01-C08. The list below does not finalize the operating week, accounting go-live cutoff, regulatory suitability or unresolved publication/reminder behavior.

1. Monday-Saturday is the initial operating week; OPERATING_DAYS is configurable. No outside-hours bookings are introduced.
2. Pilot accounting cutoff initially uses 2026-10-28; development tests use an earlier synthetic cutoff. The clinic must approve the final real-data cutoff and opening balances before launch.
3. Clinic domains share a Django app to simplify migrations; service modules preserve scheduling/accounting/notification separation.
4. A fee snapshot is reused when restoring the same therapy after cancellation. Changing therapy captures that category's fee at correction time.
5. New accounts have unusable passwords and pending activation. They are not usable until an authorized invitation and one-time password setup complete. Existing roster provisioning never resets a password.
6. No real diary names or private roster contacts are included in code, documentation, examples or screenshots. Runtime display order comes from the private roster.
7. Neon Singapore was selected because this account did not offer Mumbai. No assertion of regulatory suitability follows from that selection. The clinic must review hosting location and processor agreements before real-data launch.
8. Gmail exactly-once delivery cannot be guaranteed after an ambiguous network failure. Those sends are flagged for review rather than blindly duplicated. Confirmed failures use bounded exponential backoff.
9. During Stage A, maintenance can be delayed while Render is asleep. There is no external keep-alive or periodic pilot scheduler. Authorized activity and explicit maintenance reconcile missed work.
10. A successful code build is not proof of deployment, email delivery, restore readiness or clinic acceptance. Verification statuses are recorded separately.
