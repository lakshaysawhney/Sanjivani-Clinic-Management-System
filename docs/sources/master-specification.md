# Master specification: sanitized source archive

Preserved from the owner-supplied source. Private identities/contacts are substituted consistently; assistant names are normalized. Exact private bootstrap source is held outside public history. Product and acceptance clauses are preserved; historical execution cadence is superseded by incremental issue scope. Read ../decisions.md for precedence and conflicts. Source SHA-256: `cafcb64069175469111faf97f4149b9c274d698e78b52d79a3e4763ce295540a`.

<a id="m-0001"></a>

# SANJIVANI CLINIC MANAGEMENT SYSTEM
# Complete End-to-End MVP Implementation, Testing, GitHub Workflow and Deployment

<a id="m-0002"></a>

## YOUR ROLE AND MISSION

<a id="m-0003"></a>

You are acting as the Principal Software Engineer, Software Architect, Senior Full-Stack Developer, UI/UX Engineer, Database Engineer, DevOps Engineer, Security Engineer, QA Engineer and autonomous implementation agent for this project.

<a id="m-0004"></a>

Your responsibility is to build, test, configure and deploy a complete, reliable, production-oriented clinic management application called:

<a id="m-0005"></a>

**Sanjivani Clinic Management System**

<a id="m-0006"></a>

The application is being developed for **Sanjivani... a ray of hope**, a multidisciplinary centre for children with special needs, including autism, ADHD, cerebral palsy and other developmental conditions.

<a id="m-0007"></a>

This is a REAL operational application for a functioning clinic.

<a id="m-0008"></a>

It is not a portfolio project, hackathon prototype, mock dashboard or disposable demonstration.

<a id="m-0009"></a>

The software will handle real appointment schedules, children's records, therapist histories, attendance, financial balances and sensitive information.

<a id="m-0010"></a>

Therefore, correctness, reliability, security, data integrity and usability are essential.

<a id="m-0011"></a>

### Primary mission

<a id="m-0012"></a>

**Implement the ENTIRE MVP in one autonomous development assignment.**

<a id="m-0013"></a>

Do not stop after producing the project scaffold, backend, scheduling module or some partial application.

<a id="m-0014"></a>

Build ALL specified modules and connect them into one functional system.

<a id="m-0015"></a>

Implement incrementally internally, with continuous testing, verification, commits and code reviews, but do not require the user to supervise every implementation milestone.

<a id="m-0016"></a>

The objective is to minimize manual intervention while maintaining professional software engineering standards.

<a id="m-0017"></a>

### Very important operating instructions

<a id="m-0018"></a>

1. Read this specification completely before writing code.

<a id="m-0019"></a>

2. Treat every explicit requirement as mandatory unless there is a genuine technical impossibility or a direct contradiction. Do not silently omit features.

<a id="m-0020"></a>

3. Research current official documentation for dependencies, frameworks, APIs and cloud services rather than assuming outdated interfaces or capabilities.

<a id="m-0021"></a>

4. Make sound architecture decisions without repeatedly asking for approval about routine implementation details.

<a id="m-0022"></a>

5. If something is genuinely ambiguous, follow the defaults and business rules in this specification, document the assumption and continue.

<a id="m-0023"></a>

6. Ask the user only about an actual blocker, a necessary authorization, a significant financial commitment, an irreversible action, or a business-rule ambiguity that could cause material data errors.

<a id="m-0024"></a>

7. Use your available tools, terminal access, browser capabilities, APIs, CLIs and connected integrations to complete work rather than providing instructions telling the user to perform it manually.

<a id="m-0025"></a>

8. If a required external service is not connected, actively ask the user to connect or authorize that service. Once access is provided, resume the setup yourself.

<a id="m-0026"></a>

9. Do not ask the user to paste passwords, API tokens, OAuth refresh tokens or other secrets into conversation messages.

<a id="m-0027"></a>

10. Do not falsely claim that accounts are connected, tests have passed, emails have been delivered, or deployments are live. Verify actual outcomes.

<a id="m-0028"></a>

11. Implement robust tests for business rules, especially authorization, concurrent appointment booking, automated completion, financial ledger operations and retrospective corrections.

<a id="m-0029"></a>

12. Perform your own final audit before marking the task complete.

<a id="m-0030"></a>

13. Preserve existing project files and Git history unless changes are necessary. Do not destructively overwrite the repository.

<a id="m-0031"></a>

14. Never expose actual patient information, staff credentials, production database content or OAuth secrets through the public repository.

<a id="m-0032"></a>

15. The completed application must be suitable for a supervised real-world clinic acceptance test before live operation.

<a id="m-0033"></a>

---

<a id="m-0034"></a>

# PART 1: DEVELOPMENT ENVIRONMENT AND REPOSITORY

<a id="m-0035"></a>

## 1.1 Existing environment

<a id="m-0036"></a>

The user is developing on Windows 11.

<a id="m-0037"></a>

implementation agent is operating through the local computer environment.

<a id="m-0038"></a>

The GitHub account is:

<a id="m-0039"></a>

`lakshaysawhney`

<a id="m-0040"></a>

The GitHub repository has already been created and cloned locally.

<a id="m-0041"></a>

The intended repository slug is:

<a id="m-0042"></a>

`Sanjivani-Clinic-Management-System`

<a id="m-0043"></a>

Repository display name:

<a id="m-0044"></a>

**Sanjivani Clinic Management System**

<a id="m-0045"></a>

First inspect the selected local project folder.

<a id="m-0046"></a>

Verify:

<a id="m-0047"></a>

- The folder is a Git repository.
- Its remote points to the correct GitHub repository.
- The authenticated GitHub account has the necessary access.
- The current branch, working tree and existing files.
- The existing README and Git history.
- Availability of Python, Node.js, Git, package managers, Docker, PostgreSQL and relevant CLIs.

<a id="m-0048"></a>

Do not create a duplicate GitHub repository if the correct one already exists.

<a id="m-0049"></a>

Do not clone a second copy unnecessarily.

<a id="m-0050"></a>

If GitHub authentication or repository permissions are missing, request the necessary account connection and continue once authorized.

<a id="m-0051"></a>

## 1.2 Repository visibility

<a id="m-0052"></a>

The GitHub repository MUST remain **public**.

<a id="m-0053"></a>

This means absolutely no real patient information, private staff email roster, passwords, tokens, database dumps, environment files containing secrets or unredacted clinic photographs may enter Git history.

<a id="m-0054"></a>

This restriction includes:

<a id="m-0055"></a>

- Previous commits
- GitHub Actions logs
- CI artifacts
- PR descriptions
- Issues
- Test fixtures
- Screenshots
- Generated documentation
- Public deployment logs

<a id="m-0056"></a>

Use synthetic patients and synthetic staff identities for committed test data.

<a id="m-0057"></a>

## 1.3 Professional software engineering workflow

<a id="m-0058"></a>

Use:

<a id="m-0059"></a>

**GitHub Issue → Feature Branch → Implementation → Tests → Commit → Push → Pull Request → Review → Merge**

<a id="m-0060"></a>

Implement the complete MVP within this overall development assignment.

<a id="m-0061"></a>

You may internally divide the implementation into meaningful issues and branches.

<a id="m-0062"></a>

Use small, logical, understandable commits.

<a id="m-0063"></a>

Avoid dumping the entire application into one enormous unreviewable commit.

<a id="m-0064"></a>

Use a stable integration branch if useful, with the final completed MVP presented through a reviewable PR into `main`.

<a id="m-0065"></a>

You may autonomously merge verified feature branches into an integration branch when safe and authorized.

<a id="m-0066"></a>

Do not merge the final application into `main` without the user's approval.

<a id="m-0067"></a>

Do not create artificial issues or PRs solely to inflate activity.

<a id="m-0068"></a>

## 1.4 Git worktrees

<a id="m-0069"></a>

Git worktrees are optional.

<a id="m-0070"></a>

Use isolated worktrees or branches when multiple independent activities can be safely parallelized.

<a id="m-0071"></a>

Avoid concurrent agents making conflicting modifications to:

<a id="m-0072"></a>

- The same Django models
- Database migrations
- Authentication configuration
- Shared frontend layouts
- Financial ledger logic
- Deployment configuration

<a id="m-0073"></a>

Prefer one primary implementation agent coordinating the work.

<a id="m-0074"></a>

## 1.5 AI agent operating model

<a id="m-0075"></a>

You are the primary autonomous developer.

<a id="m-0076"></a>

Perform internal reviews after each major subsystem.

<a id="m-0077"></a>

At the end, produce a complete reviewable repository suitable for independent auditing by a second agent.

<a id="m-0078"></a>

Do not stop to ask the user whether you should continue after each feature.

<a id="m-0079"></a>

Continue through implementation and testing unless an actual authorization or business-critical blocker requires intervention.

<a id="m-0080"></a>

---

<a id="m-0081"></a>

# PART 2: TECHNOLOGY STACK

<a id="m-0082"></a>

## 2.1 Backend

<a id="m-0083"></a>

Use:

<a id="m-0084"></a>

- Python
- Django
- Django REST Framework
- PostgreSQL
- Django's session-based authentication
- pytest
- pytest-django
- PostgreSQL database transactions and constraints
- Django ORM
- Secure middleware and permissions
- Appropriate production WSGI serving with Gunicorn

<a id="m-0085"></a>

Use a modular monolithic backend.

<a id="m-0086"></a>

Do not introduce microservices.

<a id="m-0087"></a>

## 2.2 Frontend

<a id="m-0088"></a>

Use:

<a id="m-0089"></a>

- React
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui
- TanStack Query for API data fetching and cache management
- React Router or an equivalent lightweight maintained routing solution
- Accessible form and dialog primitives
- Playwright for important browser tests

<a id="m-0090"></a>

Use clean, maintainable frontend architecture.

<a id="m-0091"></a>

Strongly type API payloads.

<a id="m-0092"></a>

## 2.3 Database

<a id="m-0093"></a>

Use PostgreSQL everywhere that transactional behavior, constraints or concurrency correctness must be verified.

<a id="m-0094"></a>

Local development may use Docker PostgreSQL.

<a id="m-0095"></a>

If Docker is unavailable or broken, investigate and resolve the issue automatically where practical, or use a separate, safe development PostgreSQL instance.

<a id="m-0096"></a>

Never point automated tests at the production database.

<a id="m-0097"></a>

Do not use SQLite tests as proof of PostgreSQL concurrency guarantees.

<a id="m-0098"></a>

## 2.4 Deployment

<a id="m-0099"></a>

Target the following infrastructure:

<a id="m-0100"></a>

| Component | Platform |
|---|---|
| React frontend | Cloudflare Pages Free |
| Django backend | Render Free web service |
| PostgreSQL | Neon Free |
| Background reconciliation trigger | cron-job.org Free |
| Email notifications | Gmail API over HTTPS |
| Source control and CI | GitHub and GitHub Actions |

<a id="m-0101"></a>

No purchased custom domain is required.

<a id="m-0102"></a>

Use provider-assigned HTTPS domains.

<a id="m-0103"></a>

Verify current provider terms, usage quotas, restrictions and APIs before provisioning.

<a id="m-0104"></a>

Avoid automatically enabling paid services or upgrades.

<a id="m-0105"></a>

## 2.5 Avoid unnecessary complexity

<a id="m-0106"></a>

Do not introduce Kafka, Kubernetes, microservices, an external Redis deployment, or a separate message broker without a compelling technical need.

<a id="m-0107"></a>

For this small clinic, correctness and maintainability matter more than distributed-system complexity.

<a id="m-0108"></a>

Where asynchronous work is needed, prefer reliable database-backed jobs and a suitable lightweight execution mechanism.

<a id="m-0109"></a>

---

<a id="m-0110"></a>

# PART 3: CLINIC DETAILS AND STAFF

<a id="m-0111"></a>

## 3.1 Clinic identity

<a id="m-0112"></a>

Application name:

<a id="m-0113"></a>

**Sanjivani Clinic Management System**

<a id="m-0114"></a>

Clinic branding:

<a id="m-0115"></a>

**Sanjivani... a ray of hope**

<a id="m-0116"></a>

The centre provides multidisciplinary therapy and assessment services for children with special needs.

<a id="m-0117"></a>

The primary users are:

<a id="m-0118"></a>

- [private staff 01], administrator and schedulable provider
- [private staff 02], receptionist
- 10 therapists

<a id="m-0119"></a>

Total initial login accounts: **12**

<a id="m-0120"></a>

Total initial schedulable providers: **11**

<a id="m-0121"></a>

## 3.2 Actual staff roster

<a id="m-0122"></a>

The following information is PRIVATE BOOTSTRAP DATA.

<a id="m-0123"></a>

It may be used to create real staff accounts directly in the authorized clinic database, but must not be committed into the public repository or published in issues, tests, screenshots, documentation or logs.

<a id="m-0124"></a>

| Full name | Role / Specialization | Email |
|---|---|---|
| [private staff 01] | Administrator and schedulable provider | [private address withheld] |
| [private staff 02] | Receptionist | [private address withheld] |
| [private staff 03] | OT | [private address withheld] |
| [private staff 04] | OT | [private address withheld] |
| [private staff 05] | Sp. Edu. | [private address withheld] |
| [private staff 06] | OT | [private address withheld] |
| [private staff 07] | OT | [private address withheld] |
| [private staff 08] | OT | [private address withheld] |
| [private staff 09] | OT | [private address withheld] |
| [private staff 10] | OT | [private address withheld] |
| [private staff 11] | ABA | [private address withheld] |
| [private staff 12] | ABA | [private address withheld] |

<a id="m-0125"></a>

Preserve the spellings:

<a id="m-0126"></a>

- [private staff 03]
- [private staff 05]
- [private staff 11]

<a id="m-0127"></a>

Display names may be shortened where necessary in the dense timetable:

<a id="m-0128"></a>

- [private staff 05] → [private staff 05]
- [private staff 11] → [private staff 11]

<a id="m-0129"></a>

Full names must be retained in staff records.

<a id="m-0130"></a>

## 3.3 Account provisioning

<a id="m-0131"></a>

The user wants all 12 accounts created before clinic onboarding.

<a id="m-0132"></a>

Do not hardcode these accounts into committed migrations or source-code fixtures.

<a id="m-0133"></a>

Instead, build a secure, idempotent account-provisioning mechanism that can be run through a Django management command or Django shell.

<a id="m-0134"></a>

implementation agent should execute this provisioning mechanism itself against the properly configured target database, once authorized.

<a id="m-0135"></a>

Requirements:

<a id="m-0136"></a>

- Create all 12 accounts.
- Set correct roles.
- Set correct names and email addresses.
- Associate each therapist with a schedulable provider.
- Associate [private staff 01] with a schedulable provider as well as the administrator role.
- Do not create a provider record for [private staff 02].
- Handle duplicate usernames safely.
- Avoid duplicate account creation on repeated execution.
- Do not print passwords or private roster information in ordinary logs.
- Use secure password hashing.
- Require secure initial credential setup.

<a id="m-0137"></a>

Prefer a one-time email activation link for setting passwords, after the Gmail integration is authorized.

<a id="m-0138"></a>

Until email is ready, keep accounts safely inactive or in a secure pending-activation state.

<a id="m-0139"></a>

For the admin, support securely establishing the intended permanent password during authorized setup.

<a id="m-0140"></a>

Never invent or commit a fixed common default password.

<a id="m-0141"></a>

## 3.4 Why users and providers are separate

<a id="m-0142"></a>

A User represents someone who can log into the application.

<a id="m-0143"></a>

A Provider represents someone to whom clinic appointments can be assigned.

<a id="m-0144"></a>

[private staff 01] is both.

<a id="m-0145"></a>

Therapists are both.

<a id="m-0146"></a>

The receptionist is a User only.

<a id="m-0147"></a>

This separation must be reflected in the backend design to avoid hardcoded special cases for [private staff 01].

<a id="m-0148"></a>

---

<a id="m-0149"></a>

# PART 4: AUTHENTICATION AND AUTHORIZATION

<a id="m-0150"></a>

## 4.1 Authentication method

<a id="m-0151"></a>

Use **Django session authentication**, not JWT.

<a id="m-0152"></a>

This is a first-party internal clinic application.

<a id="m-0153"></a>

Implement:

<a id="m-0154"></a>

- Username/password login
- Logout
- Current authenticated user endpoint
- Persistent browser sessions
- Password change
- Secure password reset or account activation
- Forced initial password setup
- Administrator-initiated credential reset
- Account deactivation
- CSRF protection
- Session expiration and renewal behavior
- Login rate limiting

<a id="m-0155"></a>

Use secure, HttpOnly session cookies.

<a id="m-0156"></a>

Use Secure and appropriate SameSite cookie settings.

<a id="m-0157"></a>

Use CSRF tokens correctly for state-changing requests.

<a id="m-0158"></a>

Do not disable CSRF just to simplify frontend integration.

<a id="m-0159"></a>

Do not store passwords, JWTs, refresh tokens or sensitive authentication state in browser local storage.

<a id="m-0160"></a>

Session persistence should avoid requiring staff to sign in every day.

<a id="m-0161"></a>

Use an initial configurable session lifetime of approximately 30 days, with a sensible renewal policy.

<a id="m-0162"></a>

Session logout and account deactivation must revoke future access.

<a id="m-0163"></a>

Provide safe session handling for shared clinic computers.

<a id="m-0164"></a>

## 4.2 Three application roles

<a id="m-0165"></a>

There are exactly three application roles:

<a id="m-0166"></a>

1. ADMIN
2. RECEPTIONIST
3. THERAPIST

<a id="m-0167"></a>

Permissions must be enforced server-side.

<a id="m-0168"></a>

Never depend on frontend-only restrictions.

<a id="m-0169"></a>

### Administrator

<a id="m-0170"></a>

[private staff 01] can:

<a id="m-0171"></a>

- View schedules for all providers.
- Create, edit, cancel and correct appointments.
- Publish schedules.
- Access all historical schedules.
- Access all patient profiles and histories.
- Access all therapist histories.
- Access all frequency data.
- Change expected frequencies.
- Access all financial balances and ledger transactions.
- Enter and correct payments.
- Manage financial adjustments.
- Manage special-fee markers.
- Receive dues and operational notifications.
- Manage staff accounts.
- Make retrospective appointment corrections without the receptionist's time cutoff.
- Correct completed/cancelled session states while preserving audit and billing integrity.

<a id="m-0172"></a>

### Receptionist

<a id="m-0173"></a>

[private staff 02] can:

<a id="m-0174"></a>

- Create, edit and cancel permitted appointments.
- Build daily schedules manually.
- Publish daily schedules.
- View the entire daily timetable.
- Manage patient records.
- Track session attendance.
- Access patient and therapist histories for the permitted period.
- Edit expected weekly and monthly frequencies.
- Enter patient payments.
- View cumulative patient balances.
- Open authorized financial ledgers.
- Enter authorized manual financial adjustments.
- Mark patients requiring special fee review.
- Receive financial and publication notifications.

<a id="m-0175"></a>

Limit historical schedule and attendance access to:

<a id="m-0176"></a>

**The current calendar month plus the previous two calendar months.**

<a id="m-0177"></a>

This is not a rolling 90-day period.

<a id="m-0178"></a>

For example, in October, the permitted historical months are August, September and October.

<a id="m-0179"></a>

The receptionist must also be able to create and manage future draft schedules irrespective of this historical limit.

<a id="m-0180"></a>

The receptionist cannot:

<a id="m-0181"></a>

- Access the Staff Management administrative actions.
- Create/deactivate staff accounts.
- Assign roles.
- Bypass retrospective appointment editing restrictions.
- Access forbidden older historical schedule or attendance records through direct APIs.

<a id="m-0182"></a>

Cumulative financial balances and the necessary authorized financial ledger may cover older transactions, since outstanding dues do not reset monthly.

<a id="m-0183"></a>

### Therapist

<a id="m-0184"></a>

Therapists may:

<a id="m-0185"></a>

- View **only their OWN published appointments** during the permitted visibility period.
- View patient names, time slots and therapy types for their own assignments.
- See shared Group Therapy appointments to which they are assigned.
- View their own completed-session history for the current calendar month and previous calendar month.
- Change their own password.
- Update permitted personal account details if explicitly supported.

<a id="m-0186"></a>

Therapists may not:

<a id="m-0187"></a>

- See other therapists' schedules.
- See the entire clinic timetable.
- View unpublished schedules.
- Create, edit, cancel or publish appointments.
- Access patient financial information.
- View special-fee flags.
- Access full patient history pages.
- Access the frequency dashboard.
- Access staff management.
- View historical therapist records belonging to others.
- Bypass historical or schedule visibility cutoffs by manipulating API parameters.

<a id="m-0188"></a>

Ensure list endpoints, detail endpoints, nested resources, reports and exports all enforce these rules.

<a id="m-0189"></a>

## 4.3 Staff Management page

<a id="m-0190"></a>

Visible only to the admin.

<a id="m-0191"></a>

Provide:

<a id="m-0192"></a>

- Staff list
- Full name
- Username
- Email address
- Specialization
- Role
- Active/inactive status
- Add therapist
- Edit therapist
- Deactivate therapist
- Reactivate therapist
- Reset credentials
- Resend activation link
- Change permitted staff details

<a id="m-0193"></a>

**Never permanently delete a staff account.**

<a id="m-0194"></a>

Deletion in the UX must be represented as deactivation.

<a id="m-0195"></a>

Deactivating a therapist must preserve all historical appointments and references.

<a id="m-0196"></a>

Deactivated accounts must immediately lose further application access, including existing authenticated sessions.

<a id="m-0197"></a>

Inactive providers must not remain casually assignable to new appointments.

<a id="m-0198"></a>

If an inactive therapist still has future bookings, flag those bookings for authorized staff to resolve instead of silently deleting them.

<a id="m-0199"></a>

Protect the sole administrator account from accidentally leaving the application without an active administrator.

<a id="m-0200"></a>

Avoid general unrestricted role escalation through this interface.

<a id="m-0201"></a>

---

<a id="m-0202"></a>

# PART 5: CLINIC OPERATING HOURS AND TIME SLOTS

<a id="m-0203"></a>

All timing uses the `Asia/Kolkata` timezone.

<a id="m-0204"></a>

Clinic operating hours:

<a id="m-0205"></a>

**10:00 AM to 6:15 PM**

<a id="m-0206"></a>

Each session lasts 45 minutes.

<a id="m-0207"></a>

There are 10 valid appointment time slots.

<a id="m-0208"></a>

## Morning

<a id="m-0209"></a>

| Slot | Time |
|---|---|
| 1 | 10:00 to 10:45 |
| 2 | 10:45 to 11:30 |
| 3 | 11:30 to 12:15 |

<a id="m-0210"></a>

## Lunch break

<a id="m-0211"></a>

12:15 PM to 1:00 PM.

<a id="m-0212"></a>

No regular appointment slot exists during lunch.

<a id="m-0213"></a>

## Afternoon

<a id="m-0214"></a>

| Slot | Time |
|---|---|
| 4 | 1:00 to 1:45 |
| 5 | 1:45 to 2:30 |
| 6 | 2:30 to 3:15 |
| 7 | 3:15 to 4:00 |
| 8 | 4:00 to 4:45 |
| 9 | 4:45 to 5:30 |
| 10 | 5:30 to 6:15 |

<a id="m-0215"></a>

Use fixed, validated slot identifiers.

<a id="m-0216"></a>

Do not permit arbitrary start times in the ordinary appointment creation flow.

<a id="m-0217"></a>

Do not accidentally mix 12-hour and 24-hour times.

<a id="m-0218"></a>

Maintain a configurable clinic operating-day setting, but do not introduce unsupported special schedules or outside-hours appointments as part of the MVP.

<a id="m-0219"></a>

With 11 providers and 10 slots, the maximum theoretical daily provider-slot capacity is 110.

<a id="m-0220"></a>

This is a maximum, not an expectation that every provider has every slot filled.

<a id="m-0221"></a>

---

<a id="m-0222"></a>

# PART 6: THERAPY CATEGORIES AND FEES

<a id="m-0223"></a>

Support exactly seven selectable therapy categories.

<a id="m-0224"></a>

| Therapy category | Default charge |
|---|---:|
| OT | ₹900 |
| Sp. Edu. | ₹900 |
| ABA | ₹900 |
| Group Therapy | ₹900 |
| Assessment (2000) | ₹2,000 |
| Assessment (2500) | ₹2,500 |
| Assessment + Home Plan | ₹4,500 |

<a id="m-0225"></a>

The label for the last category should be:

<a id="m-0226"></a>

**Assessment + Home Plan**

<a id="m-0227"></a>

Do not include 4500 in its visible name.

<a id="m-0228"></a>

For the two other assessment categories, use the distinguishable labels:

<a id="m-0229"></a>

- Assessment (2000)
- Assessment (2500)

<a id="m-0230"></a>

The standard appointment creation UI should contain these seven options.

<a id="m-0231"></a>

Prefer the displayed abbreviation:

<a id="m-0232"></a>

**Sp. Edu.**

<a id="m-0233"></a>

Use `SE` only where an exceptionally constrained layout genuinely cannot fit `Sp. Edu.`.

<a id="m-0234"></a>

Do not use `SE` as the default display label.

<a id="m-0235"></a>

Rates must be stored in a backend-controlled catalog, not duplicated across frontend components.

<a id="m-0236"></a>

Charges should be captured as historical fee snapshots when they become billable, so changing catalog prices in the future does not retroactively alter past charges.

<a id="m-0237"></a>

Do not allow unauthorized frontend-supplied prices to override the catalog.

<a id="m-0238"></a>

---

<a id="m-0239"></a>

# PART 7: APPOINTMENT DATA MODEL AND CONFLICT RULES

<a id="m-0240"></a>

Scheduling is the most important feature of this application.

<a id="m-0241"></a>

The receptionist creates appointments manually.

<a id="m-0242"></a>

Do NOT implement an automatic therapist assignment algorithm.

<a id="m-0243"></a>

## 7.1 Ordinary appointments

<a id="m-0244"></a>

For every ordinary therapy or assessment appointment:

<a id="m-0245"></a>

**Exactly one patient and exactly one provider are permitted.**

<a id="m-0246"></a>

This is a mandatory backend validation rule.

<a id="m-0247"></a>

The provider may be a therapist or [private staff 01].

<a id="m-0248"></a>

An ordinary appointment cannot contain two providers.

<a id="m-0249"></a>

An ordinary appointment cannot contain two patients.

<a id="m-0250"></a>

## 7.2 Group Therapy

<a id="m-0251"></a>

Group Therapy is different.

<a id="m-0252"></a>

A single Group Therapy session may involve:

<a id="m-0253"></a>

- Multiple children
- Multiple providers
- Sometimes two therapists conducting the same group session together

<a id="m-0254"></a>

Therefore, Group Therapy must support shared appointments.

<a id="m-0255"></a>

A shared Group Therapy session is one logical session with:

<a id="m-0256"></a>

- Date
- Slot
- Therapy type
- Assigned providers
- Participating patients
- Participation status for each patient where necessary

<a id="m-0257"></a>

Do not create independent conflicting appointments for the same child simply because multiple providers attend the group.

<a id="m-0258"></a>

Likewise, do not create separate duplicate group events for every assigned provider.

<a id="m-0259"></a>

One Group Therapy session with two therapists must be visible in the schedules of both assigned therapists.

<a id="m-0260"></a>

## 7.3 Hard conflict constraints

<a id="m-0261"></a>

For any date and slot:

<a id="m-0262"></a>

**Provider constraint**

<a id="m-0263"></a>

A provider cannot be assigned to two distinct active sessions occupying the same slot.

<a id="m-0264"></a>

**Patient constraint**

<a id="m-0265"></a>

A child cannot participate in two distinct active sessions occupying the same slot.

<a id="m-0266"></a>

A child can participate in a Group Therapy session involving two therapists because that is one shared session, not two independent appointments.

<a id="m-0267"></a>

Multiple providers sharing the same Group Therapy session are allowed.

<a id="m-0268"></a>

Do not disable conflict checks globally for Group Therapy.

<a id="m-0269"></a>

Use robust relational modeling, database constraints and transactions to implement these rules.

<a id="m-0270"></a>

Concurrency correctness is mandatory.

<a id="m-0271"></a>

If two receptionists or browser tabs attempt conflicting bookings simultaneously, the database must reject the conflicting operation.

<a id="m-0272"></a>

Return a clear, friendly HTTP 409 Conflict response or equivalent appropriate domain error.

<a id="m-0273"></a>

## 7.4 Cancelled appointment slots

<a id="m-0274"></a>

A cancelled appointment no longer occupies its reserved slot.

<a id="m-0275"></a>

Example:

<a id="m-0276"></a>

- Child A was scheduled with [private staff 07] at 10:00 AM.
- Child A cancels.
- Receptionist marks that appointment Cancelled.
- [private staff 07]'s 10:00 AM slot becomes available.
- Receptionist may book Child B into that same slot.

<a id="m-0277"></a>

Preserve Child A's cancelled appointment record for history and monthly cancellation counts.

<a id="m-0278"></a>

Do not hard-delete the cancelled appointment.

<a id="m-0279"></a>

For Group Therapy:

<a id="m-0280"></a>

- Cancelling one child's participation must not automatically cancel the entire group.
- The group retains its provider reservations while active participants remain.
- If the entire group session is cancelled, release its provider reservations.
- If the group becomes empty, handle cancellation and reservations consistently.

<a id="m-0281"></a>

Prevent duplicates and conflicting active bookings.

<a id="m-0282"></a>

---

<a id="m-0283"></a>

# PART 8: APPOINTMENT STATUS AND AUTOMATIC COMPLETION

<a id="m-0284"></a>

There are exactly three user-visible appointment states:

<a id="m-0285"></a>

1. Scheduled
2. Completed
3. Cancelled

<a id="m-0286"></a>

Do NOT create a separate No-show state.

<a id="m-0287"></a>

A child who does not attend is treated as Cancelled for this system.

<a id="m-0288"></a>

## 8.1 Billing and attendance rule

<a id="m-0289"></a>

**Only Completed sessions count toward attendance and automatic charges.**

<a id="m-0290"></a>

Scheduled sessions must not be charged merely because they were created.

<a id="m-0291"></a>

Cancelled sessions:

<a id="m-0292"></a>

- Do not count as completed attendance.
- Do not generate the standard completed-session charge.
- Count toward the child's monthly cancelled-session total.

<a id="m-0293"></a>

## 8.2 Automatic completion

<a id="m-0294"></a>

An appointment initially has Scheduled status.

<a id="m-0295"></a>

At the END of its time slot, if it has not been cancelled, it must automatically become Completed.

<a id="m-0296"></a>

For example:

<a id="m-0297"></a>

- Scheduled for 10:00 to 10:45
- At 10:45, the session becomes Completed unless cancelled

<a id="m-0298"></a>

It must not be completed at the starting time.

<a id="m-0299"></a>

For a shared Group Therapy session, completion and cancellation should be modeled correctly at participant level so different child attendance outcomes are possible without double-counting the group.

<a id="m-0300"></a>

## 8.3 Backend downtime and recovery

<a id="m-0301"></a>

The backend is initially hosted on Render Free.

<a id="m-0302"></a>

It may temporarily sleep, restart or become unavailable.

<a id="m-0303"></a>

Therefore, automatic completion must NOT depend exclusively on:

<a id="m-0304"></a>

- An in-memory timer
- A Django process that never restarts
- A browser tab remaining open
- A receptionist being logged in
- A single external cron request always succeeding

<a id="m-0305"></a>

Implement a robust, idempotent reconciliation mechanism.

<a id="m-0306"></a>

Use scheduled maintenance plus safe reconciliation on appropriate backend operations.

<a id="m-0307"></a>

When the backend resumes after downtime, it must detect overdue Scheduled sessions and complete those eligible for completion.

<a id="m-0308"></a>

The operation must be safe to execute multiple times.

<a id="m-0309"></a>

No session may receive duplicate charges because reconciliation was retried.

<a id="m-0310"></a>

No completed session may be incorrectly reverted or charged twice.

<a id="m-0311"></a>

Financial balances and attendance counts must converge to their correct values after recovery.

<a id="m-0312"></a>

Use transactions and durable ledger references to ensure correctness.

<a id="m-0313"></a>

Where the UI reads time-sensitive data, reconcile consistently before returning authoritative summaries, or use an equivalent correct design.

<a id="m-0314"></a>

Avoid unsafe side effects on arbitrary unauthenticated GET requests.

<a id="m-0315"></a>

## 8.4 What may be delayed during downtime

<a id="m-0316"></a>

Document that temporary backend unavailability may delay:

<a id="m-0317"></a>

- Appointment auto-completion persistence
- Fresh session statistics
- New session charges
- Updated balance notifications
- Outgoing emails
- Appointment edits and bookings
- In-app operational reminders

<a id="m-0318"></a>

Once the backend recovers, all authoritative data must reconcile correctly.

<a id="m-0319"></a>

Never treat a missed cron invocation as permission to lose financial or session data.

<a id="m-0320"></a>

## 8.5 Retrospective corrections

<a id="m-0321"></a>

The receptionist may correct a session until:

<a id="m-0322"></a>

**6:00 PM IST on that session's calendar date.**

<a id="m-0323"></a>

After 6:00 PM, appointments for that day become non-editable to the receptionist.

<a id="m-0324"></a>

[private staff 01], as administrator, may correct old appointments at any time.

<a id="m-0325"></a>

Important distinction:

<a id="m-0326"></a>

The receptionist's cutoff applies to the session's date.

<a id="m-0327"></a>

It must NOT prevent the receptionist from creating or editing tomorrow's draft appointments after 6:00 PM today.

<a id="m-0328"></a>

This is critical because the receptionist often prepares the next day's schedule in the evening.

<a id="m-0329"></a>

### Known last-slot constraint

<a id="m-0330"></a>

The last session ends at 6:15 PM, but receptionist corrections close at 6:00 PM.

<a id="m-0331"></a>

Preserve this exact business rule.

<a id="m-0332"></a>

If the final session is automatically completed at 6:15 PM, later corrections require administrator access.

<a id="m-0333"></a>

Do not silently extend the receptionist cutoff.

<a id="m-0334"></a>

Document this operational limitation.

<a id="m-0335"></a>

## 8.6 Correcting completed appointments

<a id="m-0336"></a>

Example:

<a id="m-0337"></a>

- Session becomes Completed.
- ₹900 is charged.
- Receptionist realizes the child was absent.
- Before 6:00 PM, receptionist changes Completed to Cancelled.
- Attendance total decreases.
- Cancellation count increases.
- The ₹900 charge is reversed.
- Patient balance updates.
- All relevant dashboards reflect the corrected state.

<a id="m-0338"></a>

If the correction happens after 6:00 PM, only the administrator can perform it.

<a id="m-0339"></a>

A correction must never silently delete or rewrite accounting history.

<a id="m-0340"></a>

## 8.7 Audit log

<a id="m-0341"></a>

Track appointment state transitions and edits.

<a id="m-0342"></a>

Record:

<a id="m-0343"></a>

- Actor
- Timestamp
- Previous values
- New values
- Session reference
- Relevant reason, if entered

<a id="m-0344"></a>

Historical changes must be reviewable by authorized administrators.

<a id="m-0345"></a>

---

<a id="m-0346"></a>

# PART 9: DAILY SCHEDULING DASHBOARD

<a id="m-0347"></a>

This is the flagship feature.

<a id="m-0348"></a>

The clinic currently uses a handwritten scheduling diary.

<a id="m-0349"></a>

The handwritten photograph attached to this task is the primary UX reference.

<a id="m-0350"></a>

Treat the photograph as a layout and workflow reference only.

<a id="m-0351"></a>

Do not extract actual child names from it into application seed data.

<a id="m-0352"></a>

Do not copy the handwritten visual style literally.

<a id="m-0353"></a>

The objective is to digitize the familiar workflow with a cleaner, modern and highly readable interface.

<a id="m-0354"></a>

## 9.1 Main design philosophy

<a id="m-0355"></a>

The receptionist should be able to open the daily schedule and immediately understand:

<a id="m-0356"></a>

- Which providers have appointments
- Which children are assigned to them
- At what times
- Which slots are free
- Which appointments are cancelled or completed
- Whether the schedule is Draft or Published

<a id="m-0357"></a>

All this should be apparent at a glance.

<a id="m-0358"></a>

Avoid requiring the receptionist to open each therapist separately.

<a id="m-0359"></a>

Avoid excessive scrolling.

<a id="m-0360"></a>

Avoid visually oversized cards.

<a id="m-0361"></a>

Avoid unnecessary whitespace.

<a id="m-0362"></a>

Avoid a permanently expanded sidebar consuming large amounts of horizontal space.

<a id="m-0363"></a>

## 9.2 Desktop layout

<a id="m-0364"></a>

Do NOT use a single 11-column-wide provider grid as the default laptop layout.

<a id="m-0365"></a>

Instead, use:

<a id="m-0366"></a>

**Two vertically stacked timetable sections.**

<a id="m-0367"></a>

Section 1: six provider columns.

<a id="m-0368"></a>

Section 2: five provider columns.

<a id="m-0369"></a>

Each section has:

<a id="m-0370"></a>

- Its provider headings
- The ten time-slot rows
- Consistent appointment-cell styling
- The same fixed time order

<a id="m-0371"></a>

### Fixed provider order

<a id="m-0372"></a>

Section 1:

<a id="m-0373"></a>

1. [private staff 07]
2. [private staff 09]
3. [private staff 08]
4. [private staff 05]
5. [private staff 10]
6. [private staff 04]

<a id="m-0374"></a>

Section 2:

<a id="m-0375"></a>

1. [private staff 06]
2. [private staff 03]
3. [private staff 11]
4. [private staff 12]
5. [private staff 01]

<a id="m-0376"></a>

Provider positions must remain consistent across dates.

<a id="m-0377"></a>

Do not dynamically rearrange providers based on appointment density.

<a id="m-0378"></a>

Receptionists should be able to develop spatial familiarity with the grid.

<a id="m-0379"></a>

Support explicit administrator-controlled display ordering for future roster changes if appropriate.

<a id="m-0380"></a>

## 9.3 Display density

<a id="m-0381"></a>

The receptionist will use a 14-inch or 16-inch laptop.

<a id="m-0382"></a>

Test at minimum:

<a id="m-0383"></a>

- 1366 × 768
- 1536 × 864

<a id="m-0384"></a>

Aim for the full 11-provider, 10-slot daily schedule to be visible in one screen at ordinary browser zoom, if possible.

<a id="m-0385"></a>

However, do not make text unreadably small just to achieve zero scrolling.

<a id="m-0386"></a>

Prioritize clarity and usable text sizes.

<a id="m-0387"></a>

Use compact rows and headings.

<a id="m-0388"></a>

Show the lunch break as a distinct divider, without adding a fake appointment row during lunch.

<a id="m-0389"></a>

The grid should resemble an intelligently optimized spreadsheet-like calendar.

<a id="m-0390"></a>

## 9.4 Appointment cells

<a id="m-0391"></a>

Each occupied cell should show:

<a id="m-0392"></a>

- Child name
- Therapy type where space permits
- Status using subtle but clear visual treatment

<a id="m-0393"></a>

Admin/receptionist users should additionally see the special-fee review indicator when applicable.

<a id="m-0394"></a>

Handle long names gracefully.

<a id="m-0395"></a>

Use ellipsis when necessary, with accessible hover/focus details or click-to-expand.

<a id="m-0396"></a>

Do not make cells so small that the primary child name is illegible.

<a id="m-0397"></a>

Empty cells should clearly indicate that the slot is free and allow appointment creation.

<a id="m-0398"></a>

## 9.5 Add/Edit appointment interaction

<a id="m-0399"></a>

Clicking an empty slot should open an appointment form with the clicked provider, date and slot preselected.

<a id="m-0400"></a>

Clicking an existing appointment should open a contextual detail/edit interface.

<a id="m-0401"></a>

Required appointment fields:

<a id="m-0402"></a>

- Child / Patient
- Provider or providers, depending on therapy type
- Date
- Time slot
- Therapy type

<a id="m-0403"></a>

For Group Therapy, allow selecting multiple children and multiple providers.

<a id="m-0404"></a>

For ordinary therapy, enforce exactly one child and one provider.

<a id="m-0405"></a>

Use searchable patient selection rather than forcing a receptionist to scroll through hundreds of names.

<a id="m-0406"></a>

Allow the receptionist to create a new patient within the scheduling workflow without losing the partially entered appointment.

<a id="m-0407"></a>

Show clear validation and booking-conflict messages.

<a id="m-0408"></a>

Provide permitted actions:

<a id="m-0409"></a>

- Save
- Edit
- Cancel appointment
- Change therapist
- Change date
- Change time slot
- Change therapy type
- Correct status

<a id="m-0410"></a>

Respect all role and time-cutoff constraints.

<a id="m-0411"></a>

Never silently override an existing booking.

<a id="m-0412"></a>

## 9.6 Page controls

<a id="m-0413"></a>

The daily scheduling page should have:

<a id="m-0414"></a>

- Date navigation
- Date picker
- Today shortcut
- Draft/Published indicator
- Publish Schedule action when authorized
- Compact daily appointment summary
- Clear indication of pending changes
- Refresh behavior
- Appropriate loading and error states

<a id="m-0415"></a>

Use optimistic UI changes only where safe.

<a id="m-0416"></a>

Never show a booking as definitively saved before the server confirms the transaction.

<a id="m-0417"></a>

For appointment conflicts, roll back tentative frontend state and show a clear message.

<a id="m-0418"></a>

## 9.7 Cancellation display

<a id="m-0419"></a>

Cancelled appointments should remain in the underlying history.

<a id="m-0420"></a>

The operational grid must show the slot as available for replacement booking.

<a id="m-0421"></a>

If a cancelled appointment is relevant for review, provide a non-blocking way to inspect its history without making the slot appear occupied.

<a id="m-0422"></a>

Do not let a cancelled card visually block creation of a replacement appointment.

<a id="m-0423"></a>

## 9.8 Mobile behavior

<a id="m-0424"></a>

The receptionist dashboard is desktop-first.

<a id="m-0425"></a>

On smaller screens, allow a more compact responsive arrangement or provider-by-provider navigation.

<a id="m-0426"></a>

Do not force all 11 provider columns into tiny unreadable mobile cells.

<a id="m-0427"></a>

The therapist portal must be mobile-friendly.

<a id="m-0428"></a>

---

<a id="m-0429"></a>

# PART 10: DAILY SCHEDULE PUBLICATION

<a id="m-0430"></a>

Publication is a property of the daily schedule, not of an individual appointment.

<a id="m-0431"></a>

A daily schedule can be:

<a id="m-0432"></a>

- Draft
- Published

<a id="m-0433"></a>

These are schedule publication states, separate from appointment attendance states.

<a id="m-0434"></a>

## 10.1 Normal workflow

<a id="m-0435"></a>

The receptionist usually prepares tomorrow's schedule in the evening, approximately 5:30 to 6:00 PM.

<a id="m-0436"></a>

The new schedule initially remains Draft.

<a id="m-0437"></a>

Admin or receptionist clicks:

<a id="m-0438"></a>

**Publish Schedule**

<a id="m-0439"></a>

Once published, the appropriate therapists can view their OWN assigned appointments.

<a id="m-0440"></a>

The schedule remains published even when appointments change afterward.

<a id="m-0441"></a>

Do not require republishing after every edit.

<a id="m-0442"></a>

## 10.2 Publication permissions

<a id="m-0443"></a>

Only admin and receptionist may publish schedules.

<a id="m-0444"></a>

Therapists must not access unpublished schedules.

<a id="m-0445"></a>

Enforce publication restrictions in backend queries.

<a id="m-0446"></a>

Do not rely on frontend hiding.

<a id="m-0447"></a>

## 10.3 Publication timing

<a id="m-0448"></a>

Allow authorized staff to publish tomorrow's schedule as soon as it is ready.

<a id="m-0449"></a>

Do not require waiting until 6:00 PM.

<a id="m-0450"></a>

The normal publication interface should be scoped to the current or next operational day, so arbitrarily early future publication does not break therapist visibility limits.

<a id="m-0451"></a>

## 10.4 Therapist visibility window

<a id="m-0452"></a>

For a published schedule on calendar date D:

<a id="m-0453"></a>

It becomes visible to assigned therapists upon publication.

<a id="m-0454"></a>

It remains visible until:

<a id="m-0455"></a>

**10:00 AM IST on D+1.**

<a id="m-0456"></a>

After this cutoff, it disappears from the therapist's published daily schedule view.

<a id="m-0457"></a>

Example:

<a id="m-0458"></a>

A schedule for 28 October is published on 27 October.

<a id="m-0459"></a>

The therapist can see the 28 October schedule immediately after publication.

<a id="m-0460"></a>

That schedule remains viewable through the following morning, until the 29 October 10:00 AM cutoff.

<a id="m-0461"></a>

The intention is that a therapist sees at most two daily schedules at once.

<a id="m-0462"></a>

This is separate from the therapist's permitted completed-session history.

<a id="m-0463"></a>

Historical records remain available through the dedicated history page within the permitted two-calendar-month window.

<a id="m-0464"></a>

## 10.5 Reminder at 6:30 PM

<a id="m-0465"></a>

At 6:30 PM IST, check whether tomorrow's schedule is Published.

<a id="m-0466"></a>

If not:

<a id="m-0467"></a>

- Show a persistent in-app reminder to receptionist.
- Show the same reminder to admin.
- Keep it visible until publication or other valid resolution.
- Avoid creating endless duplicate reminders.

<a id="m-0468"></a>

The reminder must still appear if nobody had the site open at exactly 6:30 PM.

<a id="m-0469"></a>

Calculate its state from durable data and current IST time, not from a transient frontend timer.

<a id="m-0470"></a>

## 10.6 Published schedule changes

<a id="m-0471"></a>

After publication, admin and receptionist may still modify the schedule within their permissions.

<a id="m-0472"></a>

If a change materially affects a therapist's assigned schedule, that therapist must receive an email notification.

<a id="m-0473"></a>

Examples:

<a id="m-0474"></a>

- New appointment assigned
- Appointment cancelled
- Appointment moved to another slot
- Appointment reassigned
- Therapy type materially changed
- Group Therapy participant or provider assignments changed where relevant

<a id="m-0475"></a>

If a booking moves from Therapist A to Therapist B, consider both affected.

<a id="m-0476"></a>

Notify the removed therapist and the newly assigned therapist appropriately.

<a id="m-0477"></a>

Do not notify unrelated therapists.

<a id="m-0478"></a>

Do not send duplicate emails for no-op changes.

<a id="m-0479"></a>

Support deduplication or sensible batching of rapid successive edits.

<a id="m-0480"></a>

Emails should simply tell the therapist that their published schedule changed and they should check the website.

<a id="m-0481"></a>

Do not include child names, diagnoses, financial information or sensitive session details in these emails.

<a id="m-0482"></a>

The therapist must authenticate to view the updated schedule.

<a id="m-0483"></a>

---

<a id="m-0484"></a>

# PART 11: THERAPIST PORTAL

<a id="m-0485"></a>

Each therapist needs a clean, mobile-friendly portal.

<a id="m-0486"></a>

## 11.1 Therapist dashboard

<a id="m-0487"></a>

Show:

<a id="m-0488"></a>

- Therapist's name
- Date
- The therapist's own published appointments
- Session time
- Child name
- Therapy type
- Appropriate status

<a id="m-0489"></a>

Do not show appointments belonging exclusively to another therapist.

<a id="m-0490"></a>

For shared Group Therapy, show the common group session in the portal of each participating provider.

<a id="m-0491"></a>

If the session has multiple children, present their names clearly within the authorized group-session details.

<a id="m-0492"></a>

Therapists must never receive patient financial fields or special-fee markers in their API payloads.

<a id="m-0493"></a>

Do not merely hide those fields with CSS.

<a id="m-0494"></a>

## 11.2 Therapist history

<a id="m-0495"></a>

Create a separate **My Session History** page.

<a id="m-0496"></a>

Allowed date range:

<a id="m-0497"></a>

- Current calendar month
- Previous calendar month

<a id="m-0498"></a>

Show a table with:

<a id="m-0499"></a>

- Session date
- Session time
- Patient name
- Therapy type

<a id="m-0500"></a>

Show the total number of completed sessions in the selected month.

<a id="m-0501"></a>

Do not add a therapy-type breakdown on this page.

<a id="m-0502"></a>

For shared Group Therapy, count one group session once per participating therapist, even if multiple children attend. Clearly display its child participants without artificially inflating the therapist's completed-session total.

<a id="m-0503"></a>

For patient-level counts, each participating child receives one completed session.

<a id="m-0504"></a>

Ensure all aggregates are consistent.

<a id="m-0505"></a>

Only completed sessions contribute to the therapist's completed-session total.

<a id="m-0506"></a>

The therapist cannot view other therapists' historical data.

<a id="m-0507"></a>

Use backend enforcement for date and identity scoping.

<a id="m-0508"></a>

---

<a id="m-0509"></a>

# PART 12: PATIENT MANAGEMENT AND PATIENT PROFILES

<a id="m-0510"></a>

## 12.1 Patient records

<a id="m-0511"></a>

Provide a Patient Management page for authorized admin and receptionist users.

<a id="m-0512"></a>

Support:

<a id="m-0513"></a>

- Create patient
- Search patient
- View patient
- Edit patient
- Maintain patient status
- View patient session history
- View patient financial summary
- Enter payment
- Edit expected frequencies
- Mark special fee review

<a id="m-0514"></a>

At minimum, every patient has:

<a id="m-0515"></a>

- Stable internal patient ID
- Child name
- Creation timestamp
- Active/inactive status where applicable
- Special fee arrangement flag
- Expected weekly frequency
- Expected monthly frequency

<a id="m-0516"></a>

Do not rely on the child's name being unique.

<a id="m-0517"></a>

Two children can legitimately have the same name.

<a id="m-0518"></a>

Use stable IDs internally.

<a id="m-0519"></a>

Avoid collecting sensitive diagnoses, treatment notes or medical reports unless explicitly needed.

<a id="m-0520"></a>

## 12.2 Patient profile layout

<a id="m-0521"></a>

Design a clean, information-dense patient profile.

<a id="m-0522"></a>

The default page should display important data without becoming excessively long.

<a id="m-0523"></a>

Show:

<a id="m-0524"></a>

1. Patient heading and basic identity
2. Important financial and attendance summary cards
3. Session breakdowns
4. Therapist breakdown
5. Frequency/therapy-plan details
6. Expandable financial ledger
7. Session history

<a id="m-0525"></a>

Use a clean responsive layout and tabs/accordions where helpful.

<a id="m-0526"></a>

## 12.3 Monthly patient session summary

<a id="m-0527"></a>

Default period: Current calendar month.

<a id="m-0528"></a>

Support month navigation for authorized users.

<a id="m-0529"></a>

Show:

<a id="m-0530"></a>

- Total completed sessions
- OT sessions
- Sp. Edu. sessions
- ABA sessions
- Group Therapy sessions
- Assessment (2000) sessions
- Assessment (2500) sessions
- Assessment + Home Plan sessions
- Total cancelled sessions for the selected month

<a id="m-0531"></a>

Do not count Scheduled appointments as completed sessions.

<a id="m-0532"></a>

Do not count Cancelled appointments as completed sessions.

<a id="m-0533"></a>

For Group Therapy, one participating child counts one group session, regardless of how many therapists conduct it.

<a id="m-0534"></a>

## 12.4 Breakdown by therapist

<a id="m-0535"></a>

Show an additional at-a-glance summary:

<a id="m-0536"></a>

**Sessions by Therapist**

<a id="m-0537"></a>

The purpose is to help [private staff 01] detect excessive switching between therapists treating the same child.

<a id="m-0538"></a>

For the selected month, show which therapists have participated in the child's completed sessions and how many.

<a id="m-0539"></a>

Use a compact list, table, or small horizontal chart.

<a id="m-0540"></a>

For multi-provider Group Therapy, credit the participation to each relevant provider but do not double-count the child's total completed sessions.

<a id="m-0541"></a>

Make the distinction clear.

<a id="m-0542"></a>

## 12.5 Session history table

<a id="m-0543"></a>

Show a chronological table for the selected month.

<a id="m-0544"></a>

Columns:

<a id="m-0545"></a>

- Date
- Time
- Therapist / provider name
- Therapy category

<a id="m-0546"></a>

For Group Therapy, show all relevant participating providers.

<a id="m-0547"></a>

The default completed-session history should include Completed sessions.

<a id="m-0548"></a>

Provide a separate clear way to inspect Cancelled records and monthly cancellation counts where appropriate.

<a id="m-0549"></a>

Allow sorting and sensible pagination if necessary.

<a id="m-0550"></a>

Do not make the user scroll through all-time appointments by default.

<a id="m-0551"></a>

## 12.6 Patient financial summary

<a id="m-0552"></a>

Show:

<a id="m-0553"></a>

- Current cumulative balance
- Total payments received since accounting go-live
- Total session charges since accounting go-live

<a id="m-0554"></a>

The financial balance is cumulative, not monthly.

<a id="m-0555"></a>

Monthly attendance reports and cumulative financial accounting must remain separate concepts.

<a id="m-0556"></a>

## 12.7 Expandable ledger UX

<a id="m-0557"></a>

The patient profile must not be cluttered with all ledger transactions by default.

<a id="m-0558"></a>

Provide an expandable section:

<a id="m-0559"></a>

**View Financial Details**

<a id="m-0560"></a>

Position it after the financial/session summary area and before the detailed session history.

<a id="m-0561"></a>

When collapsed, the transaction table is hidden.

<a id="m-0562"></a>

When expanded, show the authorized full financial ledger.

<a id="m-0563"></a>

Include:

<a id="m-0564"></a>

- Date
- Transaction type
- Description/reference
- Amount
- Running balance if practical
- Actor where appropriate

<a id="m-0565"></a>

Allow collapsing the section again.

<a id="m-0566"></a>

---

<a id="m-0567"></a>

# PART 13: FINANCIAL MANAGEMENT

<a id="m-0568"></a>

Financial correctness is critical.

<a id="m-0569"></a>

## 13.1 Core accounting formula

<a id="m-0570"></a>

Patient balance is:

<a id="m-0571"></a>

**Current Balance = Opening Balance + Payments Received + Manual Adjustments - Chargeable Completed Sessions**

<a id="m-0572"></a>

Positive balance means prepaid credit.

<a id="m-0573"></a>

Negative balance means outstanding dues.

<a id="m-0574"></a>

Zero means no advance and no dues.

<a id="m-0575"></a>

This balance never resets at the beginning of a new month.

<a id="m-0576"></a>

## 13.2 Opening balances at system launch

<a id="m-0577"></a>

Existing patients will already have prepaid credit or outstanding dues.

<a id="m-0578"></a>

Support recording an opening balance during onboarding.

<a id="m-0579"></a>

Examples:

<a id="m-0580"></a>

- +₹2,000 opening balance
- -₹1,500 opening balance
- ₹0 opening balance

<a id="m-0581"></a>

For a new patient, the initial opening balance can normally be zero.

<a id="m-0582"></a>

Opening balance is a proper auditable ledger transaction.

<a id="m-0583"></a>

It must not be silently overwritten.

<a id="m-0584"></a>

If correcting an opening balance, record an auditable adjustment or reversal.

<a id="m-0585"></a>

Establish an explicit accounting go-live date/cutoff so historical records from before go-live are not inadvertently billed twice.

<a id="m-0586"></a>

## 13.3 Payment entry

<a id="m-0587"></a>

Admin and receptionist can enter a new payment for a patient.

<a id="m-0588"></a>

Required information:

<a id="m-0589"></a>

- Patient
- Amount
- Payment date/time
- Optional payment method/reference
- Optional notes
- Staff actor

<a id="m-0590"></a>

Validate amounts.

<a id="m-0591"></a>

Use exact arithmetic.

<a id="m-0592"></a>

Use integer paise or Decimal, never floating-point currency calculations.

<a id="m-0593"></a>

A payment increases the cumulative balance.

<a id="m-0594"></a>

Example:

<a id="m-0595"></a>

Opening balance: ₹0

<a id="m-0596"></a>

Payment received: ₹5,000

<a id="m-0597"></a>

Five completed ₹900 sessions: ₹4,500

<a id="m-0598"></a>

Current balance: +₹500

<a id="m-0599"></a>

If no payment is made and five ₹900 sessions are completed:

<a id="m-0600"></a>

Current balance: -₹4,500

<a id="m-0601"></a>

## 13.4 Session charges

<a id="m-0602"></a>

Automatically generate charges for completed sessions.

<a id="m-0603"></a>

Use the therapy-category default fee, unless an explicitly authorized financial adjustment changes the effective accounting.

<a id="m-0604"></a>

Ordinary OT, ABA, Sp. Edu. and Group Therapy each cost ₹900.

<a id="m-0605"></a>

Assessments use their specific values.

<a id="m-0606"></a>

One Group Therapy session must charge **₹900 per participating child who completed that session**, not ₹900 per therapist.

<a id="m-0607"></a>

Never double-charge because multiple providers are assigned.

<a id="m-0608"></a>

## 13.5 Financial ledger

<a id="m-0609"></a>

Implement a durable, auditable ledger.

<a id="m-0610"></a>

Transaction types should include:

<a id="m-0611"></a>

- Opening balance
- Payment
- Completed-session charge
- Charge reversal
- Payment correction/reversal
- Manual adjustment

<a id="m-0612"></a>

Use unique transaction identifiers and source references.

<a id="m-0613"></a>

Make financial reconciliation idempotent.

<a id="m-0614"></a>

If a job retries, it must not post duplicate charges.

<a id="m-0615"></a>

If a completed appointment is corrected to Cancelled, reverse the original charge without erasing the audit history.

<a id="m-0616"></a>

If a cancelled appointment later becomes completed through an authorized correction, correctly post the applicable charge.

<a id="m-0617"></a>

If its therapy type changes, reconcile the charge safely using the appropriate historical fee rules.

<a id="m-0618"></a>

## 13.6 Payment corrections

<a id="m-0619"></a>

Do not silently replace previous payment transactions.

<a id="m-0620"></a>

Support an auditable correction workflow.

<a id="m-0621"></a>

Record the original transaction and its reversal or adjustment.

<a id="m-0622"></a>

Store actor and timestamps.

<a id="m-0623"></a>

Prevent negative or nonsensical payment inputs unless they represent explicitly supported correction transactions.

<a id="m-0624"></a>

## 13.7 Special fee arrangements

<a id="m-0625"></a>

Some children have nonstandard fee arrangements.

<a id="m-0626"></a>

These patients still receive the standard calculated charges initially, but reception manually reviews and adjusts their accounting as appropriate.

<a id="m-0627"></a>

Store this setting at patient level:

<a id="m-0628"></a>

**Special Fee Arrangement / Requires Financial Review**

<a id="m-0629"></a>

Provide a checkbox or toggle on the patient profile.

<a id="m-0630"></a>

Show a compact, distinctive amber `₹!` indicator:

<a id="m-0631"></a>

- On patient profiles
- On the admin/receptionist daily schedule
- On the patient frequency dashboard
- On relevant financial review views

<a id="m-0632"></a>

Do not display this marker in therapist views or therapist API responses.

<a id="m-0633"></a>

Use amber rather than treating the patient as a payment defaulter.

<a id="m-0634"></a>

The receptionist must be able to identify these children quickly during month-end reconciliation.

<a id="m-0635"></a>

## 13.8 Negative-balance notifications

<a id="m-0636"></a>

Whenever a patient balance transitions from non-negative to negative:

<a id="m-0637"></a>

- Create a persistent in-app notification for admin and receptionist.
- Show the patient in an Outstanding Dues view.
- Make the outstanding amount easy to see.
- Avoid generating repeated duplicate alerts while the same unresolved deficit persists.

<a id="m-0638"></a>

When payments or corrections bring the balance back to zero or positive, resolve the outstanding alert.

<a id="m-0639"></a>

Existing negative balances must still be discoverable after login, even if the transition happened while nobody was online.

<a id="m-0640"></a>

Therapists must not receive or see financial alerts.

<a id="m-0641"></a>

## 13.9 Financial reporting

<a id="m-0642"></a>

Provide a practical finance/dues page for admin and receptionist.

<a id="m-0643"></a>

At minimum:

<a id="m-0644"></a>

- Patients with outstanding dues
- Current balance per patient
- Patients marked for special fee review
- Search and sorting
- Direct navigation to patient profiles
- Payment entry workflow

<a id="m-0645"></a>

Keep this focused and operational, not a large enterprise accounting module.

<a id="m-0646"></a>

---

<a id="m-0647"></a>

# PART 14: FREQUENCY DASHBOARD

<a id="m-0648"></a>

Provide a dedicated page for:

<a id="m-0649"></a>

**Actual vs Expected Patient Session Frequency**

<a id="m-0650"></a>

Visible and editable by:

<a id="m-0651"></a>

- Admin
- Receptionist

<a id="m-0652"></a>

Not visible to therapists.

<a id="m-0653"></a>

## 14.1 Table layout

<a id="m-0654"></a>

Use a clear searchable table.

<a id="m-0655"></a>

Required columns:

<a id="m-0656"></a>

1. Patient Name
2. Actual Frequency per Week
3. Expected Frequency per Week
4. Actual Frequency per Month
5. Expected Frequency per Month
6. Cancelled Sessions in Month

<a id="m-0657"></a>

Also display the special-fee review marker beside relevant patients.

<a id="m-0658"></a>

## 14.2 Actual frequencies

<a id="m-0659"></a>

Calculate actual weekly frequency from Completed appointments.

<a id="m-0660"></a>

Use Monday through Sunday as the week boundary.

<a id="m-0661"></a>

Calculate actual monthly frequency from Completed appointments in the selected calendar month.

<a id="m-0662"></a>

Do not derive these totals merely from the number of Scheduled appointments.

<a id="m-0663"></a>

Cancelled sessions do not count toward actual attendance.

<a id="m-0664"></a>

For shared Group Therapy, count one completed participation per child.

<a id="m-0665"></a>

## 14.3 Expected frequencies

<a id="m-0666"></a>

Expected weekly and expected monthly counts are manually set by admin or receptionist.

<a id="m-0667"></a>

These two values must remain independently editable.

<a id="m-0668"></a>

Do not force the monthly expected value to equal weekly expected multiplied by four.

<a id="m-0669"></a>

Treatment plans can change at any time.

<a id="m-0670"></a>

Provide editing from both:

<a id="m-0671"></a>

- Patient profile
- Frequency dashboard

<a id="m-0672"></a>

Use inline editing or an accessible modal for quick changes in the dashboard.

<a id="m-0673"></a>

Record effective dates or equivalent history for changes so earlier expectations are not silently rewritten.

<a id="m-0674"></a>

## 14.4 Cancellation tracking

<a id="m-0675"></a>

Show monthly cancelled-session count for each child.

<a id="m-0676"></a>

This also appears on the individual patient profile.

<a id="m-0677"></a>

The cancelled count must be computed from durable cancellation records, not manually entered.

<a id="m-0678"></a>

A cancelled session later corrected to Completed must have the cancellation count and completed-session count reconciled accordingly.

<a id="m-0679"></a>

Group-participation cancellations must count against the appropriate child.

<a id="m-0680"></a>

## 14.5 UX

<a id="m-0681"></a>

Provide:

<a id="m-0682"></a>

- Search
- Date/month selection
- Clear totals
- Edit controls for expected frequency
- Special-fee markers
- Sortable columns where useful
- Simple visual distinction when actual attendance is below expected

<a id="m-0683"></a>

Do not create an overcomplicated analytics dashboard.

<a id="m-0684"></a>

---

<a id="m-0685"></a>

# PART 15: HISTORY ACCESS RULES

<a id="m-0686"></a>

Calendar-month boundaries use IST.

<a id="m-0687"></a>

## Admin

<a id="m-0688"></a>

All-time access to:

<a id="m-0689"></a>

- Daily schedules
- Patient session histories
- Therapist histories
- Financial records
- Relevant reports

<a id="m-0690"></a>

## Receptionist

<a id="m-0691"></a>

Session and schedule history:

<a id="m-0692"></a>

- Current calendar month
- Previous two calendar months

<a id="m-0693"></a>

Future schedules remain manageable.

<a id="m-0694"></a>

Authorized cumulative financial balances and supporting accounting transactions remain accessible as necessary.

<a id="m-0695"></a>

## Therapist

<a id="m-0696"></a>

Own completed-session history:

<a id="m-0697"></a>

- Current calendar month
- Previous calendar month

<a id="m-0698"></a>

Own published daily schedule:

<a id="m-0699"></a>

- Only during the separate publication visibility window

<a id="m-0700"></a>

These two restrictions must not be confused.

<a id="m-0701"></a>

For example, an expired published daily schedule should no longer be accessible through the therapist's schedule endpoint, even though completed sessions from that date may still appear in their permitted history page.

<a id="m-0702"></a>

All date restrictions must be enforced by DRF, not only frontend navigation.

<a id="m-0703"></a>

---

<a id="m-0704"></a>

# PART 16: NOTIFICATIONS AND GMAIL API

<a id="m-0705"></a>

## 16.1 Gmail sender account

<a id="m-0706"></a>

Use the following Gmail account to send therapist notification emails:

<a id="m-0707"></a>

`[private address withheld]`

<a id="m-0708"></a>

This is the intended Google account for OAuth authorization.

<a id="m-0709"></a>

Do not use [private staff 01]'s Gmail account as the initial sender.

<a id="m-0710"></a>

Keep the sender configurable through secure deployment configuration so it can be changed later.

<a id="m-0711"></a>

## 16.2 Gmail implementation

<a id="m-0712"></a>

Use the **Gmail API over HTTPS**.

<a id="m-0713"></a>

Render Free blocks ordinary outbound SMTP ports.

<a id="m-0714"></a>

Do not rely on Django Gmail SMTP via port 587 in the production Render Free environment.

<a id="m-0715"></a>

You may provide a local SMTP adapter for development if helpful, but production should use Gmail API over HTTPS.

<a id="m-0716"></a>

Use official Google API libraries and supported OAuth flows.

<a id="m-0717"></a>

Request only the permissions needed to send email, such as `gmail.send`.

<a id="m-0718"></a>

Support durable authorization, refresh-token handling, credential rotation and failure reporting.

<a id="m-0719"></a>

Check current Google OAuth app verification, testing/production status and token-expiration rules.

<a id="m-0720"></a>

Do not rely on temporary seven-day OAuth testing tokens for uninterrupted operation.

<a id="m-0721"></a>

Avoid unnecessarily broad Gmail scopes.

<a id="m-0722"></a>

## 16.3 Maximum OAuth automation

<a id="m-0723"></a>

You must attempt to handle the entire Google Cloud and Gmail setup yourself.

<a id="m-0724"></a>

This includes, where access permits:

<a id="m-0725"></a>

- Create or select a suitable Google Cloud project.
- Enable Gmail API.
- Configure OAuth branding/consent.
- Create appropriate OAuth client credentials.
- Configure redirect URIs.
- Implement authorization initiation/callback.
- Initiate the sender's OAuth consent flow.
- Request offline access when appropriate.
- Securely store refresh credentials.
- Configure production environment variables.
- Verify token refresh.
- Send a test email with explicit authorization.
- Verify actual delivery status where possible.

<a id="m-0726"></a>

If Google requires user sign-in, 2FA, consent or verification, ask the user to perform that specific authorization action.

<a id="m-0727"></a>

If the Google Cloud account is not accessible, request the relevant official connection or browser access.

<a id="m-0728"></a>

Do not immediately give the user a long manual tutorial.

<a id="m-0729"></a>

Use automation wherever supported.

<a id="m-0730"></a>

Do not bypass Google security controls or misrepresent OAuth consent.

<a id="m-0731"></a>

Never expose secrets in logs or Git history.

<a id="m-0732"></a>

## 16.4 Therapist schedule-change emails

<a id="m-0733"></a>

Only send relevant emails when published schedules materially change.

<a id="m-0734"></a>

Recipients: affected therapists.

<a id="m-0735"></a>

Message should be generic, for example:

<a id="m-0736"></a>

**Subject:** Sanjivani: Your schedule has been updated

<a id="m-0737"></a>

**Body:** Your published clinic schedule has changed. Please sign in to the Sanjivani Clinic Management System to view the latest schedule.

<a id="m-0738"></a>

Include an appropriate authenticated application link.

<a id="m-0739"></a>

Do not include child names, diagnoses or financial information.

<a id="m-0740"></a>

## 16.5 Reliable delivery

<a id="m-0741"></a>

Email sending must not block or roll back a successful appointment save if an external email provider is temporarily unavailable.

<a id="m-0742"></a>

Use a durable database-backed notification/outbox mechanism.

<a id="m-0743"></a>

Record:

<a id="m-0744"></a>

- Intended recipient
- Event reference
- Delivery state
- Attempts
- Last error
- Timestamps

<a id="m-0745"></a>

Support retry with bounded backoff.

<a id="m-0746"></a>

Prevent duplicate emails on repeated job execution.

<a id="m-0747"></a>

Use transaction-safe event creation.

<a id="m-0748"></a>

Do not falsely mark emails as sent when the Gmail API request failed.

<a id="m-0749"></a>

## 16.6 In-app notifications

<a id="m-0750"></a>

At minimum:

<a id="m-0751"></a>

- Negative-balance notifications
- Unpublished next-day schedule reminders
- Operational warnings where essential

<a id="m-0752"></a>

Provide a header notification indicator and an accessible notification panel or page for authorized staff.

<a id="m-0753"></a>

Show unread or unresolved status.

<a id="m-0754"></a>

Make notifications persistent across sessions.

<a id="m-0755"></a>

Never expose admin/receptionist financial notifications to therapists.

<a id="m-0756"></a>

---

<a id="m-0757"></a>

# PART 17: CLOUD DEPLOYMENT

<a id="m-0758"></a>

The intended hosting configuration is:

<a id="m-0759"></a>

- Frontend: Cloudflare Pages Free
- Backend: Render Free
- Database: Neon Free
- Scheduler: cron-job.org Free
- Email: Gmail API over HTTPS

<a id="m-0760"></a>

The goal is to start at approximately ₹0 recurring cost while preserving data correctness.

<a id="m-0761"></a>

The user understands that free hosting does not guarantee continuous uptime and may later upgrade Render.

<a id="m-0762"></a>

## 17.1 Cloudflare Pages

<a id="m-0763"></a>

Deploy the React frontend on Cloudflare Pages.

<a id="m-0764"></a>

Use the provider-assigned HTTPS domain.

<a id="m-0765"></a>

The frontend must remain accessible even while Render sleeps or restarts.

<a id="m-0766"></a>

Configure static routing and SPA fallback behavior correctly.

<a id="m-0767"></a>

## 17.2 Django backend on Render

<a id="m-0768"></a>

Deploy Django/DRF on Render Free.

<a id="m-0769"></a>

Configure:

<a id="m-0770"></a>

- Production build command
- Dependencies
- Gunicorn
- Migrations
- Static assets as required
- Environment variables
- Allowed hosts
- Secure cookies
- Trusted origins
- Database connection
- Logging
- Health checks

<a id="m-0771"></a>

Do not rely on Render's ephemeral filesystem for durable patient files, secrets, database data or session state.

<a id="m-0772"></a>

Use PostgreSQL-backed or another suitably persistent session store.

<a id="m-0773"></a>

Verify service startup, API availability and database connectivity.

<a id="m-0774"></a>

## 17.3 Neon PostgreSQL

<a id="m-0775"></a>

Use Neon managed PostgreSQL.

<a id="m-0776"></a>

Create and configure the database using authorized integration/API access where possible.

<a id="m-0777"></a>

Keep development and production databases separated.

<a id="m-0778"></a>

Secure connection credentials.

<a id="m-0779"></a>

Use SSL/TLS configuration as required.

<a id="m-0780"></a>

Do not expose database credentials through the frontend or public repository.

<a id="m-0781"></a>

Implement documented encrypted external backups and a verified recovery procedure appropriate to the available hosting tier.

<a id="m-0782"></a>

Do not treat a managed database as equivalent to a tested backup.

<a id="m-0783"></a>

## 17.4 Same-origin API proxy

<a id="m-0784"></a>

React will be hosted at a Cloudflare Pages origin.

<a id="m-0785"></a>

Django is hosted at a separate Render origin.

<a id="m-0786"></a>

To support Django sessions reliably, implement secure same-origin API proxying using appropriate Cloudflare Pages Functions or other supported Cloudflare routing capabilities.

<a id="m-0787"></a>

Browser API calls should use paths under the frontend origin, such as `/api/...`.

<a id="m-0788"></a>

The proxy forwards requests to Render.

<a id="m-0789"></a>

Ensure correct handling of:

<a id="m-0790"></a>

- HTTP methods
- Request bodies
- Cookies
- CSRF tokens
- Set-Cookie responses
- Redirects
- Host/origin validation
- Authentication failures
- Content types
- Error statuses
- Timeouts
- Sensitive response cache controls

<a id="m-0791"></a>

Do not implement an insecure generic open proxy.

<a id="m-0792"></a>

Do not disable CSRF.

<a id="m-0793"></a>

Do not expose the protected Render backend as an easy bypass around origin and authorization controls.

<a id="m-0794"></a>

Explicitly test login, logout, CSRF, session persistence and role authorization through the actual deployed frontend origin.

<a id="m-0795"></a>

## 17.5 Cold-start loading screen

<a id="m-0796"></a>

If Render is temporarily asleep or restarting, users should see a branded, professional frontend state:

<a id="m-0797"></a>

**Connecting to Sanjivani**

<a id="m-0798"></a>

Explain that the clinic system is starting or reconnecting.

<a id="m-0799"></a>

Provide:

<a id="m-0800"></a>

- Loading animation
- Automatic retry
- Sensible exponential backoff
- Manual Retry option
- Clear error state after repeated failures
- Preservation of unsaved form values where practical

<a id="m-0801"></a>

Do not show an unhandled Render error page as the intended application experience.

<a id="m-0802"></a>

Do not promise an exact one-minute restart time.

<a id="m-0803"></a>

Distinguish:

<a id="m-0804"></a>

- Backend unavailable
- Authentication expired
- Permission denied
- Network failure
- Actual application/server error

<a id="m-0805"></a>

Never retry non-idempotent writes blindly without safeguards.

<a id="m-0806"></a>

Do not show stale financial or booking information as guaranteed current.

<a id="m-0807"></a>

## 17.6 Free scheduler

<a id="m-0808"></a>

Use **cron-job.org Free**, unless a verified alternative is materially better and still free.

<a id="m-0809"></a>

Configure a legitimate periodic backend request approximately every five minutes.

<a id="m-0810"></a>

The objective is:

<a id="m-0811"></a>

1. Monitor/wake the backend where permitted.
2. Reduce avoidable idle spin-downs.
3. Trigger idempotent background maintenance.
4. Reconcile overdue session completion.
5. Process pending notification work.

<a id="m-0812"></a>

Create:

<a id="m-0813"></a>

- Lightweight public health endpoint
- Protected maintenance endpoint

<a id="m-0814"></a>

Use a securely generated maintenance authorization secret.

<a id="m-0815"></a>

The protected endpoint must reject unauthenticated invocations.

<a id="m-0816"></a>

Never include the maintenance secret in public URLs, source code or logs.

<a id="m-0817"></a>

Use secure headers or another supported secret delivery method.

<a id="m-0818"></a>

If the cron provider cannot support the required secure authentication, choose an equivalent secure supported approach.

<a id="m-0819"></a>

Make maintenance operations idempotent and bounded.

<a id="m-0820"></a>

Do not generate fake user sessions or disguise monitoring as ordinary human activity.

<a id="m-0821"></a>

Do not rely on periodic pings as an uptime guarantee.

<a id="m-0822"></a>

The application must still recover correctly when maintenance invocations are missed.

<a id="m-0823"></a>

## 17.7 Scheduler and attendance correctness

<a id="m-0824"></a>

If the maintenance scheduler runs at 10:50 for an appointment ending at 10:45, it should mark the eligible session Completed at reconciliation time.

<a id="m-0825"></a>

The session's actual scheduled end remains 10:45.

<a id="m-0826"></a>

The delayed processing timestamp must not change the clinical session time.

<a id="m-0827"></a>

If the backend was down for several hours, it must reconcile all eligible overdue records, not only the immediately preceding five minutes.

<a id="m-0828"></a>

Use safe batching, locks, unique references and transactions where appropriate.

<a id="m-0829"></a>

This is essential for billing correctness.

<a id="m-0830"></a>

## 17.8 Upgrade path

<a id="m-0831"></a>

Document how to upgrade from Render Free to a paid non-sleeping web service without rebuilding the application or migrating away from PostgreSQL unnecessarily.

<a id="m-0832"></a>

Do not automatically enable paid Render instances.

<a id="m-0833"></a>

---

<a id="m-0834"></a>

# PART 18: MAXIMUM EXTERNAL ACCOUNT AUTOMATION

<a id="m-0835"></a>

This section is exceptionally important.

<a id="m-0836"></a>

The user wants the agent to perform as much implementation AND external setup as possible.

<a id="m-0837"></a>

Do not interpret an external integration task as merely a request to write documentation.

<a id="m-0838"></a>

For each service:

<a id="m-0839"></a>

- GitHub
- Cloudflare
- Render
- Neon
- cron-job.org
- Google Cloud/Gmail API

<a id="m-0840"></a>

Follow this process.

<a id="m-0841"></a>

### Step 1: Discover access

<a id="m-0842"></a>

Check for available:

<a id="m-0843"></a>

- Connected integrations
- Official APIs
- Supported CLI tools
- Browser/computer interaction capabilities
- Existing authenticated sessions where authorized
- Environment variables and existing credentials
- Existing projects or services

<a id="m-0844"></a>

### Step 2: Request connection if necessary

<a id="m-0845"></a>

If access is missing, ask the user to connect or authorize the service.

<a id="m-0846"></a>

Prefer official OAuth authorization or supported account-connection mechanisms.

<a id="m-0847"></a>

Ask for precise user action only where needed.

<a id="m-0848"></a>

Do not ask for raw passwords or secret tokens in chat.

<a id="m-0849"></a>

### Step 3: Perform setup autonomously

<a id="m-0850"></a>

Once permission is granted, actually:

<a id="m-0851"></a>

- Create services
- Configure settings
- Generate secrets securely
- Store credentials in appropriate secret stores
- Configure environment variables
- Connect the database
- Register OAuth redirect URLs
- Deploy applications
- Configure cron jobs
- Test integrations
- Verify operational behavior

<a id="m-0852"></a>

### Step 4: Request sensitive approvals

<a id="m-0853"></a>

Request explicit approval for:

<a id="m-0854"></a>

- External account authorization
- 2FA/consent
- Any paid upgrade or billing action
- Irreversible operations
- Production database migration or destructive changes
- First real patient-data migration
- Sending activation emails to actual staff if not previously authorized

<a id="m-0855"></a>

Routine code generation and test execution should not require repeated user intervention.

<a id="m-0856"></a>

### Step 5: Do not hide blockers

<a id="m-0857"></a>

If a service cannot be automated with the available tools, explain the specific missing permission or capability and request the smallest possible user intervention.

<a id="m-0858"></a>

Do not falsely claim a completed deployment.

<a id="m-0859"></a>

Do not silently switch to a paid alternative.

<a id="m-0860"></a>

The agent should not finish with a generic manual deployment guide if the required services are accessible and can be configured automatically.

<a id="m-0861"></a>

---

<a id="m-0862"></a>

# PART 19: PROJECT ARCHITECTURE

<a id="m-0863"></a>

Use a clean monorepo layout resembling:

<a id="m-0864"></a>

```text
Sanjivani-Clinic-Management-System/
├── backend/
│   ├── config/
│   ├── accounts/
│   ├── patients/
│   ├── scheduling/
│   ├── billing/
│   ├── notifications/
│   ├── audit/
│   ├── tests/
│   ├── manage.py
│   └── requirements/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── features/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── types/
│   │   └── pages/
│   └── tests/
├── docs/
├── .github/
│   ├── workflows/
│   └── ISSUE_TEMPLATE/
├── AGENTS.md
├── .env.example
├── docker-compose.yml
└── README.md
```

<a id="m-0865"></a>

Adjust the exact structure where beneficial, but maintain logical domain separation.

<a id="m-0866"></a>

## 19.1 Core domain entities

<a id="m-0867"></a>

At minimum, model the equivalent of:

<a id="m-0868"></a>

- User
- Provider
- Patient
- TherapyType
- DailySchedule
- ClinicalSession / Appointment
- SessionProviderAssignment
- SessionPatientParticipation
- Provider/Patient slot reservations where required
- ExpectedFrequencyPlan
- LedgerEntry
- Notification
- EmailOutbox
- AuditLog

<a id="m-0869"></a>

You may rename or consolidate these if a better normalized design exists.

<a id="m-0870"></a>

Do not implement separate duplicated mutable counters as the authoritative source for attendance.

<a id="m-0871"></a>

Session histories and counts should be derived from durable scheduling/participation records.

<a id="m-0872"></a>

Money should derive from the financial ledger.

<a id="m-0873"></a>

## 19.2 Referential integrity

<a id="m-0874"></a>

Use foreign keys and appropriate constraints.

<a id="m-0875"></a>

Avoid cascade deletion of historically important records.

<a id="m-0876"></a>

Use protection, deactivation, archival or other appropriate approaches to preserve historical references.

<a id="m-0877"></a>

## 19.3 Transactions

<a id="m-0878"></a>

Use database transactions around operations requiring consistency.

<a id="m-0879"></a>

Examples:

<a id="m-0880"></a>

- Booking a session
- Cancelling a session and releasing reservations
- Reassigning providers
- Completing a session and generating charges
- Reversing charges
- Updating payment records
- Processing negative-balance transitions
- Creating notification events

<a id="m-0881"></a>

Ensure concurrent requests do not create inconsistent states.

<a id="m-0882"></a>

## 19.4 Idempotency

<a id="m-0883"></a>

Make repeated execution safe for:

<a id="m-0884"></a>

- Account provisioning
- Auto-completion
- Charge posting
- Charge reversal
- Notification creation
- Email outbox processing
- Scheduled maintenance
- Migration/bootstrap operations

<a id="m-0885"></a>

## 19.5 Schema migrations

<a id="m-0886"></a>

Use Django migrations.

<a id="m-0887"></a>

Review the migration graph for consistency.

<a id="m-0888"></a>

Do not delete production data merely to fix migration conflicts.

<a id="m-0889"></a>

Document any necessary breaking change.

<a id="m-0890"></a>

---

<a id="m-0891"></a>

# PART 20: APPLICATION PAGES AND NAVIGATION

<a id="m-0892"></a>

Implement a complete frontend with role-appropriate navigation.

<a id="m-0893"></a>

## Admin navigation

<a id="m-0894"></a>

Recommended pages:

<a id="m-0895"></a>

1. Dashboard / Daily Schedule
2. Patients
3. Therapists / Session History
4. Frequency Tracker
5. Payments / Outstanding Dues
6. Notifications
7. Staff Management
8. Profile / Change Password

<a id="m-0896"></a>

## Receptionist navigation

<a id="m-0897"></a>

1. Daily Schedule
2. Patients
3. Therapist History
4. Frequency Tracker
5. Payments / Outstanding Dues
6. Notifications
7. Profile / Change Password

<a id="m-0898"></a>

No Staff Management administration.

<a id="m-0899"></a>

## Therapist navigation

<a id="m-0900"></a>

1. My Schedule
2. My Session History
3. My Profile / Change Password

<a id="m-0901"></a>

Avoid displaying inaccessible navigation elements.

<a id="m-0902"></a>

But remember that server permissions are authoritative.

<a id="m-0903"></a>

## 20.1 Tables

<a id="m-0904"></a>

Use tables where they genuinely improve operational usability.

<a id="m-0905"></a>

Especially:

<a id="m-0906"></a>

- Patient list
- Patient session history
- Therapist session history
- Frequency dashboard
- Financial ledger
- Outstanding dues
- Staff management

<a id="m-0907"></a>

Include meaningful columns, date filters, search, loading states and pagination when needed.

<a id="m-0908"></a>

## 20.2 UI design system

<a id="m-0909"></a>

Aim for a design that is:

<a id="m-0910"></a>

- Modern
- Calm
- Clean
- Professional
- Trustworthy
- Appropriate for a clinic
- Information-dense without being cluttered
- Fast and practical for reception staff

<a id="m-0911"></a>

Use restrained colors.

<a id="m-0912"></a>

Use clear typography.

<a id="m-0913"></a>

Use subtle status color coding.

<a id="m-0914"></a>

Use proper empty, loading, success, error and retry states.

<a id="m-0915"></a>

Avoid excessive glassmorphism, flashy animations and decorative complexity.

<a id="m-0916"></a>

The primary scheduling interface should feel like a highly refined version of the existing handwritten timetable, with some inspiration from Google Calendar.

<a id="m-0917"></a>

## 20.3 No em dashes

<a id="m-0918"></a>

There must be **no em dash character (Unicode U+2014)** anywhere in visible website content.

<a id="m-0919"></a>

This includes:

<a id="m-0920"></a>

- Headings
- Labels
- Button text
- Tooltips
- Notifications
- Dialogs
- Empty states
- Error messages
- Static UI copy

<a id="m-0921"></a>

Use ordinary punctuation.

<a id="m-0922"></a>

Implement an automated check against visible UI copy and localization strings.

<a id="m-0923"></a>

## 20.4 Accessibility

<a id="m-0924"></a>

Support:

<a id="m-0925"></a>

- Readable contrast
- Keyboard navigation
- Proper form labels
- Accessible dialogs
- Focus handling
- Screen-reader-friendly interactions where practical
- Responsive layouts
- Accessible error messages

<a id="m-0926"></a>

Do not make critical actions dependent on hover-only controls.

<a id="m-0927"></a>

---

<a id="m-0928"></a>

# PART 21: SECURITY AND PRIVACY

<a id="m-0929"></a>

The system handles information about children and clinic operations.

<a id="m-0930"></a>

Take privacy seriously.

<a id="m-0931"></a>

Implement:

<a id="m-0932"></a>

- Least-privilege access
- Server-side role enforcement
- Object-level authorization
- Secure authentication
- HTTPS
- CSRF protection
- Login rate limiting
- Input validation
- Secure database credentials
- Audit logs
- Cache-control for sensitive responses
- Restricted error disclosures
- Safe logging
- Protection against insecure direct object references
- Session invalidation after account deactivation

<a id="m-0933"></a>

Avoid exposing sensitive records through URLs, static assets, public logs or error messages.

<a id="m-0934"></a>

Do not collect detailed diagnoses or medical reports as part of this MVP unless explicitly authorized.

<a id="m-0935"></a>

Review applicable Indian privacy and child-data handling obligations and document any operational/legal steps the clinic must complete before real-data launch.

<a id="m-0936"></a>

Do not claim legal compliance without evidence.

<a id="m-0937"></a>

## 21.1 Public repository security

<a id="m-0938"></a>

Use:

<a id="m-0939"></a>

- `.gitignore`
- `.env.example` with placeholders
- Secret scanning
- Environment variables
- Secure runtime credential storage

<a id="m-0940"></a>

Never commit actual:

<a id="m-0941"></a>

- Staff roster emails
- Gmail OAuth client secrets
- Refresh tokens
- Django secret keys
- Database connection strings
- Render secrets
- Cloudflare API tokens
- Scheduler maintenance secrets
- Patient records
- Unredacted diary images

<a id="m-0942"></a>

The private staff roster supplied in this prompt is permitted only for authorized bootstrap, not public code.

<a id="m-0943"></a>

## 21.2 Safe staff onboarding

<a id="m-0944"></a>

Use secure activation links or another properly protected first-login credential setup.

<a id="m-0945"></a>

Never distribute all staff passwords in an unencrypted text file.

<a id="m-0946"></a>

Do not send passwords in plain email.

<a id="m-0947"></a>

Ensure activation links expire and cannot be reused.

<a id="m-0948"></a>

Do not accidentally activate real staff accounts before their intended onboarding without authorization.

<a id="m-0949"></a>

---

<a id="m-0950"></a>

# PART 22: TESTING REQUIREMENTS

<a id="m-0951"></a>

Testing is mandatory.

<a id="m-0952"></a>

Build a comprehensive test suite, not superficial smoke tests.

<a id="m-0953"></a>

## 22.1 Backend authorization tests

<a id="m-0954"></a>

Test:

<a id="m-0955"></a>

- Admin access
- Receptionist access
- Therapist access
- Unauthenticated access
- Cross-therapist access attempts
- Direct object ID manipulation
- Future unpublished schedule access
- Expired published schedule access
- Historical date restrictions
- Access to financial information
- Access to special-fee markers
- Staff management permission boundaries
- Deactivated account access

<a id="m-0956"></a>

## 22.2 Scheduling tests

<a id="m-0957"></a>

Test:

<a id="m-0958"></a>

- Creating an ordinary appointment
- Exactly one patient/provider for ordinary therapy
- Group Therapy with multiple providers
- Group Therapy with multiple patients
- Two therapists sharing one group session
- A child cannot occupy two distinct sessions in the same slot
- A therapist cannot occupy two distinct sessions in the same slot
- Concurrent conflicting booking attempts
- Cancellation releasing reservations
- Replacement booking after cancellation
- Group-participant-only cancellation
- Whole-group cancellation
- Moving appointments between providers
- Editing appointments after publication
- Draft versus Published behavior
- Correct time-slot mapping

<a id="m-0959"></a>

## 22.3 Automatic completion tests

<a id="m-0960"></a>

Use deterministic frozen-time testing.

<a id="m-0961"></a>

Test:

<a id="m-0962"></a>

- Completion exactly at slot end
- No completion before slot end
- Cancelled sessions remain cancelled
- Completion after missed scheduler execution
- Multiple repeated reconciliation runs
- No duplicate completion transactions
- No duplicate billing
- Recovery after downtime
- Receptionist cutoff at 6:00 PM IST
- Administrator retrospective correction
- Correct handling of final 5:30 to 6:15 PM slot

<a id="m-0963"></a>

## 22.4 Billing tests

<a id="m-0964"></a>

Test all seven fee categories.

<a id="m-0965"></a>

Test:

<a id="m-0966"></a>

- Opening positive balance
- Opening negative balance
- Opening zero balance
- Payment received
- Session charge
- Multiple sessions
- Assessment pricing
- Group Therapy charging per child
- No double-charging for multi-provider groups
- Cancelled sessions generating no charge
- Completed-to-Cancelled reversal
- Cancelled-to-Completed correction
- Therapy-type charge correction
- Duplicate event execution
- Concurrent financial operations
- Manual adjustments
- Payment correction
- Month transition preserving cumulative balance
- Dues notification transition
- Dues resolution

<a id="m-0967"></a>

Use exact money assertions.

<a id="m-0968"></a>

## 22.5 History and frequency tests

<a id="m-0969"></a>

Test:

<a id="m-0970"></a>

- Patient monthly completed count
- Patient monthly cancelled count
- Category breakdown
- Provider breakdown
- Group Therapy counting rules
- Weekly actual frequency
- Monthly actual frequency
- Editable expected frequencies
- Effective-date expected-frequency history
- Current/previous calendar-month restrictions
- Therapist own-history restriction
- Correct month boundary behavior in IST

<a id="m-0971"></a>

## 22.6 Email and notification tests

<a id="m-0972"></a>

Test:

<a id="m-0973"></a>

- Published schedule change event
- Correct affected therapist recipients
- No email before publication for ordinary draft edits
- New assignment notification
- Removed provider notification
- Group assignment changes
- Duplicate event suppression
- Gmail API adapter behavior using mocks
- Retry behavior
- Failed delivery status
- No patient data included in outgoing generic notification emails
- Persistent 6:30 PM unpublished-schedule reminder
- Negative balance notifications

<a id="m-0974"></a>

## 22.7 Frontend tests

<a id="m-0975"></a>

Test:

<a id="m-0976"></a>

- Login
- Role-specific navigation
- Patient creation
- Appointment creation
- Appointment editing
- Cancellation
- Publishing
- Therapist schedule visibility
- Patient monthly history
- Frequency edits
- Payment entry
- Financial accordion
- Staff management
- Error handling
- Cold-start loading screen

<a id="m-0977"></a>

Use Playwright for representative full workflows.

<a id="m-0978"></a>

## 22.8 Visual/browser tests

<a id="m-0979"></a>

Use browser testing or screenshots with synthetic data.

<a id="m-0980"></a>

Check:

<a id="m-0981"></a>

- 1366 × 768
- 1536 × 864
- Typical mobile dimensions for therapist portal

<a id="m-0982"></a>

Specifically verify:

<a id="m-0983"></a>

- All 11 providers have a consistent position
- Six-column first section
- Five-column second section
- Ten correct time slots
- Lunch divider
- Long patient names
- Fully occupied schedule
- Empty schedule
- Mixed appointment types
- Cancelled appointments
- Fee marker visibility
- Publication indicator
- Readable text
- No unexpected overflow
- No unnecessary scrolling
- No em dashes in visible UI copy

<a id="m-0984"></a>

Do not use real patient records for screenshots.

<a id="m-0985"></a>

## 22.9 End-to-end acceptance scenario

<a id="m-0986"></a>

At minimum, automate the following realistic workflow:

<a id="m-0987"></a>

1. Admin account exists and can log in.
2. Receptionist logs in.
3. Receptionist creates a patient.
4. Receptionist sets expected weekly/monthly frequencies.
5. Receptionist creates an OT appointment.
6. Another booking for the same therapist/slot is rejected.
7. Another booking for the same child/slot is rejected.
8. Receptionist creates a shared Group Therapy appointment.
9. Receptionist publishes tomorrow's schedule.
10. Assigned therapists can see their own appointments.
11. Unassigned therapists cannot see those appointments.
12. Receptionist changes a published appointment.
13. Correct therapist notification event is created.
14. Completed session generates correct attendance and charge.
15. Cancelled session does not generate a charge.
16. Cancellation count updates.
17. New payment updates the patient's balance.
18. A correction reverses its charge.
19. Negative balance creates the appropriate warning.
20. Admin can manage staff accounts.
21. Deactivated accounts lose access.
22. Historical access limits hold.
23. Application survives simulated backend downtime and reconciliation retries.

<a id="m-0988"></a>

Do not mark these workflows as passed unless the tests actually run successfully.

<a id="m-0989"></a>

---

<a id="m-0990"></a>

# PART 23: CONTINUOUS INTEGRATION

<a id="m-0991"></a>

Configure GitHub Actions.

<a id="m-0992"></a>

Include, as appropriate:

<a id="m-0993"></a>

- Backend formatting/linting
- Backend tests
- PostgreSQL-backed integration tests
- Migration checks
- Frontend linting
- TypeScript type checking
- Frontend production build
- Frontend tests
- Critical Playwright tests
- Secret scanning or a comparable protective check
- UI copy check for em dashes

<a id="m-0994"></a>

CI must not require production credentials.

<a id="m-0995"></a>

Use synthetic fixtures.

<a id="m-0996"></a>

Ensure local and CI commands are documented.

<a id="m-0997"></a>

Use deterministic, reproducible dependencies where practical.

<a id="m-0998"></a>

---

<a id="m-0999"></a>

# PART 24: DEPLOYMENT VERIFICATION

<a id="m-1000"></a>

Do not claim successful deployment solely because a build command returned zero.

<a id="m-1001"></a>

Actually verify:

<a id="m-1002"></a>

- Cloudflare frontend URL opens
- React routing works
- Render backend is reachable
- Neon database connection works
- Django migrations are applied
- API proxy works
- Login through the Cloudflare origin works
- Session cookies persist correctly
- CSRF-protected requests succeed
- Unauthorized requests are rejected
- Staff roles produce correct navigation
- Scheduling works through the deployed interface
- Scheduler configuration is active
- Maintenance endpoint authorization works
- Cold-start recovery UI works
- Gmail API can send an authorized test email
- Secrets are absent from public repository history and client bundles

<a id="m-1003"></a>

Use synthetic records for deployment verification.

<a id="m-1004"></a>

Do not put real patient information into the system until the owner has approved go-live.

<a id="m-1005"></a>

---

<a id="m-1006"></a>

# PART 25: DOCUMENTATION

<a id="m-1007"></a>

Create clear documentation for future maintenance.

<a id="m-1008"></a>

Required documents:

<a id="m-1009"></a>

### README.md

<a id="m-1010"></a>

Include:

<a id="m-1011"></a>

- Project overview
- Features
- Architecture overview
- Tech stack
- Local setup
- Running tests
- Development workflow
- Deployment references

<a id="m-1012"></a>

### docs/requirements.md

<a id="m-1013"></a>

Authoritative business requirements.

<a id="m-1014"></a>

### docs/architecture.md

<a id="m-1015"></a>

Architecture and reasoning.

<a id="m-1016"></a>

### docs/data-model.md

<a id="m-1017"></a>

Models, relationships, constraints and accounting invariants.

<a id="m-1018"></a>

### docs/permissions.md

<a id="m-1019"></a>

Complete role and date-access matrix.

<a id="m-1020"></a>

### docs/scheduling.md

<a id="m-1021"></a>

Time slots, lifecycle, publication and Group Therapy rules.

<a id="m-1022"></a>

### docs/billing.md

<a id="m-1023"></a>

Opening balances, fees, ledger, reversals and reconciliation.

<a id="m-1024"></a>

### docs/deployment.md

<a id="m-1025"></a>

Actual deployment configuration and verified URLs.

<a id="m-1026"></a>

### docs/operations.md

<a id="m-1027"></a>

Backups, restore, account provisioning, staff onboarding, failures, scheduler and support workflows.

<a id="m-1028"></a>

### docs/assumptions.md

<a id="m-1029"></a>

Any remaining assumptions or documented trade-offs.

<a id="m-1030"></a>

### AGENTS.md

<a id="m-1031"></a>

Instructions for future coding agents.

<a id="m-1032"></a>

Include repository conventions, architecture constraints, business invariants, security expectations, testing commands and change-review rules.

<a id="m-1033"></a>

Do not put staff personal contact information or credentials in documentation.

<a id="m-1034"></a>

---

<a id="m-1035"></a>

# PART 26: AUTONOMOUS EXECUTION PLAN

<a id="m-1036"></a>

Proceed with the following internal phases without requiring the user to manually direct every phase.

<a id="m-1037"></a>

## Phase A: Discover and plan

<a id="m-1038"></a>

- Inspect repository.
- Verify GitHub remote.
- Inspect environment.
- Verify available connectors and permissions.
- Read current framework and hosting documentation.
- Convert this prompt into an authoritative requirements checklist.
- Design database schema and business invariants.
- Identify external account access requirements.
- Request missing account connections where necessary.

<a id="m-1039"></a>

## Phase B: Foundation

<a id="m-1040"></a>

- Set up Django and DRF.
- Set up PostgreSQL.
- Set up React/TypeScript/Vite/Tailwind/shadcn.
- Set up test infrastructure.
- Set up linting and CI.
- Implement authentication and roles.
- Implement staff/provider management.

<a id="m-1041"></a>

## Phase C: Scheduling engine

<a id="m-1042"></a>

- Implement appointments and group sessions.
- Implement hard booking constraints.
- Implement cancellations.
- Implement completion logic.
- Implement reconciliation and audit trails.
- Add exhaustive backend tests.

<a id="m-1043"></a>

## Phase D: Scheduling frontend

<a id="m-1044"></a>

- Build the dense 6 + 5 scheduling layout.
- Implement date navigation.
- Implement patient creation within scheduling.
- Implement appointment CRUD.
- Implement publication controls.
- Implement therapist-specific schedule views.
- Verify laptop layout.

<a id="m-1045"></a>

## Phase E: Patient and therapist tracking

<a id="m-1046"></a>

- Patient profiles.
- Monthly summaries.
- Therapist breakdown.
- Therapist history.
- Monthly cancellations.
- Frequency dashboard.
- Treatment-plan frequency editing.

<a id="m-1047"></a>

## Phase F: Financial management

<a id="m-1048"></a>

- Opening balances.
- Payments.
- Ledger.
- Auto-charges.
- Charge reversals.
- Manual adjustments.
- Special fee flags.
- Outstanding dues.
- Financial notifications.

<a id="m-1049"></a>

## Phase G: Notifications and external integrations

<a id="m-1050"></a>

- In-app notifications.
- Gmail API integration.
- OAuth authorization.
- Email outbox.
- Publication-change emails.
- Scheduled maintenance.

<a id="m-1051"></a>

## Phase H: Deployment

<a id="m-1052"></a>

- Cloudflare Pages.
- Render.
- Neon.
- cron-job.org.
- Secure environment configuration.
- Backend/frontend integration.
- Gmail sender configuration.
- Health checks.
- Deployment verification.

<a id="m-1053"></a>

## Phase I: Quality assurance

<a id="m-1054"></a>

- Run automated tests.
- Fix failures.
- Perform browser verification.
- Review responsive design.
- Test authorization attacks.
- Test concurrent appointment conflicts.
- Test financial invariants.
- Verify public repository contains no secrets.
- Check documentation and operational readiness.

<a id="m-1055"></a>

## Phase J: Final delivery

<a id="m-1056"></a>

- Prepare final reviewed PRs.
- Report implementation completeness.
- Provide test evidence.
- Provide verified deployment URLs.
- Report any remaining approvals or external blockers.
- Give a concise acceptance-testing checklist for the clinic owner.

<a id="m-1057"></a>

The user should not need to repeatedly prompt you to continue from one phase to another.

<a id="m-1058"></a>

---

<a id="m-1059"></a>

# PART 27: DEFINITION OF DONE

<a id="m-1060"></a>

The project is complete only if ALL of the following are true:

<a id="m-1061"></a>

### Scheduling

<a id="m-1062"></a>

- All 11 providers can be scheduled.
- Ordinary therapies enforce one child and one provider.
- Group Therapy supports shared sessions.
- Double-booking is prevented.
- Cancelled sessions release occupied slots.
- Three appointment states work.
- Automatic completion works.
- Retrospective correction rules work.
- Audit history is preserved.
- Daily schedule is readable on the target laptops.

<a id="m-1063"></a>

### Publication

<a id="m-1064"></a>

- Draft and Published are correctly implemented.
- Therapists see only their own published appointments.
- Visibility cutoff is enforced.
- Published schedules remain editable by authorized staff.
- Schedule-change notifications are generated.
- Publication reminders work.

<a id="m-1065"></a>

### Patient records

<a id="m-1066"></a>

- Patient CRUD works.
- Monthly completed-session counts work.
- Category breakdown works.
- Therapist breakdown works.
- Cancellation counts work.
- Session history table works.
- Date-based permissions work.

<a id="m-1067"></a>

### Therapist records

<a id="m-1068"></a>

- Therapist own schedule works.
- Own monthly history works.
- Total completed-session count works.
- No unauthorized access to others' data.
- No patient financial information leakage.

<a id="m-1069"></a>

### Financial management

<a id="m-1070"></a>

- All seven fees are correct.
- Opening balances work.
- Payments work.
- Cumulative balance is correct.
- Ledger is auditable.
- Reversals work.
- Special fee markers work.
- Negative-balance alerts work.
- No duplicate financial postings.

<a id="m-1071"></a>

### Frequency tracking

<a id="m-1072"></a>

- Actual weekly count works.
- Actual monthly count works.
- Expected counts are editable.
- Monthly cancellation column works.
- Special-fee indicators appear.
- Access restrictions work.

<a id="m-1073"></a>

### Authentication and staff

<a id="m-1074"></a>

- All three roles work.
- Secure persistent sessions work.
- No public signup exists.
- Initial staff provisioning mechanism works.
- Admin staff management works.
- Deactivation preserves history and revokes access.
- Password-change and activation flows work.

<a id="m-1075"></a>

### Infrastructure

<a id="m-1076"></a>

- Frontend builds and runs.
- Backend runs.
- Database migrations pass.
- API proxy works securely.
- Cold-start UI works.
- Scheduler/reconciliation works.
- Gmail integration works where authorized.
- Deployment configuration is correct.
- No credentials are committed publicly.

<a id="m-1077"></a>

### Engineering quality

<a id="m-1078"></a>

- Backend tests pass.
- Frontend checks pass.
- Critical browser tests pass.
- CI is configured.
- Important edge cases are tested.
- Documentation is complete.
- Code is understandable and maintainable.
- No known critical correctness/security defects remain.

<a id="m-1079"></a>

---

<a id="m-1080"></a>

# PART 28: FINAL REPORTING FORMAT

<a id="m-1081"></a>

At completion, report:

<a id="m-1082"></a>

## 1. Implementation status

<a id="m-1083"></a>

A feature-by-feature checklist.

<a id="m-1084"></a>

Distinguish:

<a id="m-1085"></a>

- Implemented and verified
- Implemented but not fully verified
- Blocked
- Not implemented

<a id="m-1086"></a>

Never mark something complete without evidence.

<a id="m-1087"></a>

## 2. GitHub status

<a id="m-1088"></a>

Provide:

<a id="m-1089"></a>

- Repository URL
- Branches created
- PR links
- CI status
- Merge status

<a id="m-1090"></a>

## 3. Architecture

<a id="m-1091"></a>

Briefly explain the final architecture and any important deviations from the original proposed structure.

<a id="m-1092"></a>

## 4. Automated test results

<a id="m-1093"></a>

Provide actual commands run, test counts, pass/fail outcomes, and remaining limitations.

<a id="m-1094"></a>

## 5. Deployment status

<a id="m-1095"></a>

Provide verified frontend/backend URLs where available.

<a id="m-1096"></a>

Clearly identify which services are configured and which remain blocked by missing authorization.

<a id="m-1097"></a>

## 6. Account onboarding

<a id="m-1098"></a>

Confirm whether initial staff accounts were successfully provisioned.

<a id="m-1099"></a>

Do not expose temporary passwords or the private contact roster.

<a id="m-1100"></a>

Explain only the remaining user consent or staff activation action.

<a id="m-1101"></a>

## 7. Security and privacy

<a id="m-1102"></a>

Summarize:

<a id="m-1103"></a>

- Role isolation checks
- CSRF/session security
- Secret handling
- Database backups
- Any outstanding privacy/compliance work

<a id="m-1104"></a>

## 8. Known issues

<a id="m-1105"></a>

List actual remaining defects, uncertainties, limitations and risks.

<a id="m-1106"></a>

Do not conceal incomplete requirements.

<a id="m-1107"></a>

## 9. Clinic acceptance readiness

<a id="m-1108"></a>

Give one verdict:

<a id="m-1109"></a>

- Ready for supervised clinic acceptance testing
- Not ready
- Inconclusive due to blocked verification

<a id="m-1110"></a>

Never claim it is safe to migrate real patient data without the required verification.

<a id="m-1111"></a>

---

<a id="m-1112"></a>

# FINAL EXECUTION DIRECTIVE

<a id="m-1113"></a>

You now have the complete product specification.

<a id="m-1114"></a>

**Build the entire Sanjivani Clinic Management System MVP end to end.**

<a id="m-1115"></a>

Use professional software engineering practices, but do not introduce unnecessary process overhead.

<a id="m-1116"></a>

Work autonomously.

<a id="m-1117"></a>

Write code, run tests, correct failures, commit changes, create reviewable PRs, configure authorized external services, deploy when permitted and verify the actual behavior.

<a id="m-1118"></a>

Use the existing connected GitHub repository and selected local project folder.

<a id="m-1119"></a>

Use the attached handwritten diary photograph as a UX reference, not as source data.

<a id="m-1120"></a>

Automate external account setup as much as technically and securely possible.

<a id="m-1121"></a>

When access to Render, Cloudflare, Neon, cron-job.org or Google Cloud is missing, proactively request the relevant connection or authorization so you can perform the setup yourself.

<a id="m-1122"></a>

Do not default to telling the user to manually configure services.

<a id="m-1123"></a>

Only require intervention for actual authentication, security approval, payment authorization, destructive operations or unavoidable external limitations.

<a id="m-1124"></a>

Do not ask routine architectural or coding questions.

<a id="m-1125"></a>

Preserve the full business logic, all role permissions, all history limits, all financial invariants and all UI requirements.

<a id="m-1126"></a>

**Do not sacrifice correctness in pursuit of speed.**

<a id="m-1127"></a>

**Do not stop at scaffolding or partial features.**

<a id="m-1128"></a>

**Do not declare success without running meaningful tests and verifying results.**

<a id="m-1129"></a>

Deliver the complete, reviewable, deployment-ready MVP and a clear, evidence-based final status report.
