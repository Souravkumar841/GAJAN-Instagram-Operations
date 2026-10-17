# Client submission readiness — GAJAN Senior AI Systems Engineer

## Current status
**Local prototype ready for technical review; live acceptance NOT demonstrated.** The client requires one company-authorised real Instagram test account and a 2–3 minute recording. Neither can be truthfully completed without client-provided access and human actions.

## Included and testable
- [x] Runnable Python 3.10+ CLI and SQLite ledger; 5 automated unit tests.
- [x] Idempotent account registration and human task creation; persistent state after restart.
- [x] Human task owner/deadline, reminders/escalation recorded locally (notification delivery not wired).
- [x] 150-character bio validation and vault-reference-only fields.
- [x] Audit findings and follow-up tasks; explicit `unverified` labels.
- [x] Offboarding tasks with pending/blocked status; no false claim of external revocation.
- [x] Neutral HTTPS endpoint health check with bounded retries and timeout.
- [x] Redacted sample reports, decision log, README, and recording storyboard.

## Required before claiming client task complete
- [ ] Obtain brand kit, test company email/phone, vault access, separate Meta Business and approved proxies through company-approved channels.
- [ ] Have authorised human perform Instagram signup and verification and confirm handle availability.
- [ ] Have authorised human enable 2FA and store credentials and backup codes in company vault; store only references here.
- [ ] Have authorised human complete Instagram profile, convert to Business and link Meta assets; verify least-privilege roles.
- [ ] Demonstrate a live audit and offboard a designated **temporary test role** with evidence of actual changes.
- [ ] Integrate the company vault and approved proxy transport, and demonstrate **real controlled proxy rotation/failover on a neutral endpoint**. Current CLI only checks direct HTTPS reachability.
- [ ] Record 2–3 minute real-account walkthrough with handoffs, restart/resume and honest blockers; redact all secrets and recovery details.
- [ ] Validate report/register against real platform state and label each claim `integration-verified`, `human-confirmed`, or `unverified`.

## Do not do
Do not automate real Instagram signup, identity verification, CAPTCHA, rate-limit circumvention or restriction evasion. Do not run optional device automation against Instagram or another social app. Do not insert credentials, recovery codes, OTPs, or unredacted identifiers into recordings, logs, GitHub or chat.

## Suggested client communication
Submit as **prototype with clearly disclosed external blockers**, unless all live items above have actually been completed. Never present sample reports as live evidence.
