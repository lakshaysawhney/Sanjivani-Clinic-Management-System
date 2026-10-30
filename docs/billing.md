# Billing invariants

Balance = opening balance + payments + manual adjustments - completed session charges, including corrective reversal entries. Positive is prepaid credit; negative is dues. Values are integer paise. Balances do not reset by month.

Catalog fees: OT, Sp. Edu., ABA and Group Therapy INR 900; Assessment (2000) INR 2000; Assessment (2500) INR 2500; Assessment + Home Plan INR 4500. Group charges apply once per completed child, independent of provider count.

The first billable completion captures a fee snapshot. Cancellation reverses the old charge, retaining the snapshot for restoration of the same therapy. A therapy change reverses the previous amount and captures the new category's price, even when both categories cost the same. A completed date/slot move reverses the old charge and posts the retained fee at the corrected effective end time. A date before ACCOUNTING_START_DATE is not billable. This cutoff must be approved before opening balances/live import.

Opening balances are recorded once. Payment corrections append a reversal and then, where needed, a new payment. Adjustments require a reason. Posted entries cannot be edited/deleted. Patient-level locks serialize concurrent adjustments, completion charges and payments. Source keys and idempotency records prevent retries posting duplicates.

The special-fee marker never changes automatic prices; authorized staff make explicit adjustments. Dues warnings are resolved when the ledger reaches zero or positive. Financial summaries show gross payments/charges; the ledger exposes all corrections and the cumulative balance.
