# Final deployment amendment: sanitized source archive

Preserved from the owner-supplied source. Private identities/contacts are substituted consistently; assistant names are normalized. Exact private bootstrap source is held outside public history. Product and acceptance clauses are preserved; historical execution cadence is superseded by incremental issue scope. Read ../decisions.md for precedence and conflicts. Source SHA-256: `c26b184cc34d1f0e8d8b5f05f8a53aa109485683c1401a177717a6993a9ca33b`.

<a id="a-0001"></a>

# FINAL DEPLOYMENT REQUIREMENT UPDATE
## Supersedes all conflicting instructions in the master specification

<a id="a-0002"></a>

IMPORTANT: The deployment strategy has changed. Treat the instructions in this section as authoritative wherever they conflict with the earlier specification.

<a id="a-0003"></a>

### 1. Two-stage hosting strategy

<a id="a-0004"></a>

STAGE A: Development, testing and supervised pilot

<a id="a-0005"></a>

- Deploy the frontend to Cloudflare Pages Free.
- Deploy Django/DRF to a Render Free web service.
- Use Neon Free PostgreSQL.
- Use Gmail API over HTTPS for notification emails.
- Do not upgrade to any paid hosting service during development or pilot testing.
- Do not create any synthetic keep-alive mechanism.
- Do not configure UptimeRobot, cron-job.org, GitHub Actions or any other service to periodically ping Render merely to prevent its 15-minute idle shutdown.
- Do not attempt to disguise automated traffic as real users.
- Allow Render Free to sleep normally during inactivity.
- Preserve the branded "Connecting to Sanjivani" loading interface, automatic backend retry and manual Retry functionality.
- Ensure unsuccessful or interrupted requests do not cause duplicate bookings, payments or charges.

<a id="a-0006"></a>

STAGE B: Actual clinic production launch

<a id="a-0007"></a>

- Before live operations begin, request explicit approval to upgrade the existing Render backend from Free to the paid Starter compute plan.
- The expected baseline cost is $7/month at current published pricing, subject to verification when upgrading.
- The upgrade should be performed by implementation agent automatically through authorized Render access, after the user approves the paid action.
- Do not require the user to manually recreate the backend service.
- Preserve the existing application configuration, database connections, secrets and deployment URLs wherever possible.
- Verify successful operation after upgrading.
- Do not automatically upgrade to Render Pro or a more expensive compute tier.
- If the Starter instance is insufficient under measured load, report evidence and request approval before increasing costs.

<a id="a-0008"></a>

### 2. Background task scheduling

<a id="a-0009"></a>

The application still requires reliable automatic processing of:

<a id="a-0010"></a>

- Scheduled session completion after each session's ending time
- Completed-session charge creation
- Attendance and billing reconciliation
- Delayed email notification delivery
- Pending notification retries
- Operational reminders

<a id="a-0011"></a>

During development and pilot:

<a id="a-0012"></a>

- Do not run recurring external traffic solely to keep Render awake.
- Implement correct idempotent reconciliation triggered by authorized application activity.
- Support explicit maintenance execution for development and testing.
- Accept that automatic background processing can be delayed while Render Free is asleep.
- Document this limitation clearly for pilot testers.
- Preserve correct effective session times, statuses and financial outcomes following reconciliation.

<a id="a-0013"></a>

During paid production:

<a id="a-0014"></a>

- Configure a legitimate scheduler such as cron-job.org Free, using its supported API and secure authentication.
- Schedule actual business maintenance operations at an appropriate interval, preferably one minute if supported and reliable.
- The scheduler must perform genuine operational work rather than artificial uptime maintenance.
- It should call a protected, idempotent maintenance endpoint.
- Configure bounded processing, retries, failure logging and appropriate alerts.
- Do not assume a paid always-on web service automatically executes scheduled jobs.
- Preserve reconciliation-on-read/write or an equivalent fallback so missed jobs cannot permanently corrupt attendance and accounting.

<a id="a-0015"></a>

### 3. Production readiness

<a id="a-0016"></a>

Before using real clinic patient records:

<a id="a-0017"></a>

- The user must explicitly approve production go-live.
- Render must be upgraded to an appropriate paid, non-sleeping compute instance.
- Verify backend performance and memory usage.
- Verify secure authentication and role permissions.
- Verify appointment and financial correctness.
- Verify background scheduling and notifications.
- Verify PostgreSQL backups and successful restoration.
- Verify the clinic's operational acceptance tests.

<a id="a-0018"></a>

Do not migrate real patient data or enable live clinic operations merely because development deployment succeeded.

<a id="a-0019"></a>

### 4. External automation

<a id="a-0020"></a>

Continue to maximize automation of Cloudflare, Render, Neon, Gmail API, GitHub and other integrations.

<a id="a-0021"></a>

When access is unavailable, ask the user to connect or authorize the required service instead of defaulting to manual setup instructions.

<a id="a-0022"></a>

Ask the user to approve only genuinely sensitive, privileged, destructive or paid operations.

<a id="a-0023"></a>

implementation agent should perform the actual Render Free deployment autonomously during development and prepare the Starter upgrade procedure and configuration for eventual production.

<a id="a-0024"></a>

The paid upgrade must NOT be executed until explicitly authorized.

<a id="a-0025"></a>

### 5. All other requirements

<a id="a-0026"></a>

Every other functional requirement, UI design decision, staff account rule, permission boundary, financial invariant, test requirement and GitHub workflow specified in the original master prompt remains unchanged.

<a id="a-0027"></a>

Do not omit, reinterpret or weaken any existing requirements because of this deployment amendment.
