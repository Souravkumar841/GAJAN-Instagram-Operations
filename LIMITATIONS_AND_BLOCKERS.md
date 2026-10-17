# Limitations, blockers, and completion evidence

**Project:** GAJAN Instagram Operations — Senior AI Systems Engineer build task  
**Review date:** 17 October 2026  
**Scope:** One company-authorised real Instagram test brand; compliant human-in-the-loop operations.

## Executive status

**Working local prototype; not a completed live Instagram deployment.** The package includes a Python CLI, local browser interface, SQLite account/task/event tracking, audit and offboarding task generation, a neutral-endpoint health check, documentation, and tests. The final-clean project was reported to pass 10 automated tests; this is not proof of live integrations. No real Instagram account has been verified through this prototype, and no 2–3 minute live walkthrough is included in the clean package.

The client's assignment describes a supplied brand kit, test company email and phone, vault, separate Meta Business environment, and approved proxies. **Those credentials/resources have not been supplied in the project materials available for this review.** Their availability to the operator outside this project is **not confirmed**; do not describe them as definitively withheld by the client.

## Requirements and blocker register

| Requirement | Evidence in this package | Status | Dependency / next action |
|---|---|---|---|
| Candidate handles and Instagram availability | Candidate handle can be stored locally; no official availability lookup | Partial | Human checks candidates on Instagram; record result |
| Company email alias and reserved phone | Local register fields; no provisioning integration | Pending | Confirm approved company email/phone and assign through authorised personnel |
| Real signup and identity verification | Owned/deadline human tasks; no real-platform signup | Blocked / not demonstrated | Authorised human performs steps on real test account; attach redacted evidence |
| Reminders, escalation and restart recovery | Local reminder/escalation state, persisted tasks, idempotent creation | Partial | Demonstrate restart/retry; configure actual outbound notification delivery |
| 2FA, password and backup-code vault storage | Vault references only; no vault API | Blocked / not demonstrated | Human enables 2FA; store secrets only in company vault; verify references |
| Profile, Business conversion, Meta linking and least-privilege roles | Local register and guided procedure; no Meta integration | Blocked / not demonstrated | Complete authorised human steps and confirm roles with evidence |
| Account register | SQLite register and JSON export | Implemented locally | Populate verified real-account fields and last verification date |
| Weekly audit and verification labels | Local audit and follow-up tasks; findings currently `unverified` | Partial | Configure weekly scheduler; verify company ownership, backup codes and stale roles; record human/integration evidence |
| Offboarding of temporary test member | Generates pending tasks and report | Partial | Human removes actual roles, rotates exposed credentials and backup codes; record completed/pending/blocked separately |
| Proxy checks, retries and session management | Neutral HTTPS health check with timeout/bounded attempts | Partial | Integrate approved proxy and vault; demonstrate sticky session and neutral-endpoint rotation/failover |
| Device fleet automation | Not implemented | Optional / intentionally skipped | Explain 20–50 device scaling, operations and monthly cost assumptions in decision log if required |
| Redacted run log, register, audit and offboarding reports | Local report generation command | Available, must regenerate | Run workflows then export and inspect all artifacts for sensitive information |
| 2–3 minute live account screen recording | Recording instructions, but no qualifying final video | Not completed | Record authorised real-account workflow; if access unavailable, clearly label local-only demo as incomplete |
| One-page decision log and AI disclosure | `DECISION_LOG.md` included | Included | Check consistency with final evidence and state AI tools used |

## Boundaries and safe operation

- Never automate Instagram account signup or identity verification. Do not bypass CAPTCHA, rate limits, restrictions or platform enforcement.
- Use only supported integrations or tracked, authorised human actions. Pause for human review on security challenges.
- Never enter passwords, OTPs, backup codes or proxy credentials into task notes, source code, screenshots, logs or reports. Use approved vault storage; keep only non-secret references in the application.
- Proxy rotation is for approved resilience tests on neutral endpoints, not evasion. Preserve connections during active sessions.
- If optional device testing is added, use only a neutral sample app, not Instagram or another social app.

## Evidence and technical limitations

1. **Local evidence is not platform verification.** Account/task rows, completed task notes and sample reports do not establish a real account or verified Meta roles. Record the evidence source as `integration-verified`, `human-confirmed` or `unverified`; current audit findings remain `unverified` until supported evidence exists.
2. **Security controls are prototype-level.** Basic note filtering and export redaction reduce risk but cannot guarantee that arbitrary sensitive text is removed. Review all artifacts before sharing; protect the SQLite database and do not commit secrets or private data.
3. **Notification delivery and weekly scheduling are not hosted.** The `remind` command updates local state; cron/Task Scheduler and an approved delivery channel still need configuration.
4. **Offboarding is coordination, not execution.** No real Meta role revocation or vault credential rotation occurs automatically.
5. **Proxy checks are not proxy integration.** The shipped health command tests a neutral HTTPS URL directly; it does not establish proxy authentication, sticky sessions or failover.
6. **Test results are local only.** Unit-test success does not establish browser usability on the client's machine, live Instagram acceptance, or production readiness.

## How work resumes when access is approved

1. Obtain written authorisation, test brand kit, designated human owner, email/phone, vault permissions, Meta Business access and approved proxies through secure channels.
2. Record candidate handle and open the signup/verification task with owner and deadline. Have the human complete the official Instagram workflow; record blockers and redacted evidence. Retry the local workflow using the same account/task IDs to avoid duplicates.
3. Human enables 2FA, stores credentials and backup codes in vault, completes the profile, converts to Business, links Meta and assigns least-privilege roles. Independently confirm completion before updating register status and verification date.
4. Run audit; triage and label findings by evidence type. Run temporary-role offboarding and distinguish pending actions from completed platform changes.
5. Configure approved proxy adapter, test neutral-endpoint health/rotation/failover, and retain redacted logs. Configure recurring weekly audit and notification delivery.
6. Generate fresh redacted reports and record a 2–3 minute real-account walkthrough including interruption recovery and unresolved blockers.

## Commands for local evidence

From `gajan_instagram_ops`:

```bash
python -m unittest discover -s tests -v
python -m app.cli init
python -m app.cli remind
python -m app.cli audit
python -m app.cli report --folder artifacts
```

For offboarding, substitute a **real local account ID** and the designated test member:

```bash
python -m app.cli offboard --account 1 --person temporary_test_member
python -m app.cli report --folder artifacts
```

These commands only operate on local records. Inspect generated JSON files before sending them; do not treat demonstration data as live evidence.

## Submission statement

> This submission demonstrates a runnable, compliant local prototype for coordinating Instagram account operations with human approval, persistent task tracking, audit and offboarding workflows, and basic neutral-endpoint health checks. Live Instagram account verification, Meta Business linking, actual vault and proxy integration, outbound reminders, and the requested live walkthrough remain pending authorised access, implementation and/or evidence. No platform-enforcement bypass was attempted.
