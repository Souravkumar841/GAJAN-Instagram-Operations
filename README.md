# GAJAN Instagram Operations — compliant human-in-loop prototype

**Status:** runnable local prototype; NOT a completed live Instagram account. No Instagram or Meta credentials or brand kit were provided in this conversation. Real-world steps are tracked for a company-authorized human. No emulator-only claim.

## Project status
This package is a **local demonstration only**; it does not meet the live-account acceptance requirement. See `LIMITATIONS_AND_BLOCKERS.md` and `CLIENT_SUBMISSION_CHECKLIST.md`.

## Setup
Python 3.10+; standard library only. From repository root:

```bash
python -m app.cli init
python -m app.cli register --brand "TEST_BRAND" --owner "company-ops" --handle "test_brand_candidate"
python -m app.cli task --account 1 --kind instagram_signup_verification --owner company-ops --days 1
python -m app.cli remind
python -m app.cli complete --task 1 --notes "Human-confirmed on approved test account"
python -m app.cli update --account 1 --field status --value waiting_human
python -m app.cli audit
python -m app.cli offboard --account 1 --person temporary_test_member
python -m app.cli health --url https://example.com
python -m app.cli report --folder artifacts
python -m unittest discover -s tests -v
```

Use `OPS_DB=/secure/location/ops.db` to configure database location. Protect database file with restrictive OS permissions and disk encryption. SQLite is suitable for a single-instance demo, not distributed concurrent processing.

## Real-account guided runbook
1. Obtain written authorization and company-provided test brand kit, email alias, reserved phone, vault, approved proxy and separate Meta Business access. Never paste passwords, OTPs or backup codes into this application.
2. Suggest 2–3 candidate handles; a human checks availability in the official Instagram app/site (handle availability is not API-verified).
3. Register brand in local ledger (NOT Instagram). Create task `instagram_signup_verification` with owner and deadline. Human performs signup and identity verification directly on Instagram; if blocked, log the blocker and wait. `register` and `task` are idempotent.
4. Human enables authenticator-based 2FA, stores password and backup codes in company vault, and records **only** references (`vault://path/to/item`). Record recovery email and phone locally only if approved, never in shared reports.
5. Human completes name, bio (150 characters max), website, category, image; switches to Business and links to the provided Meta Business Suite/Business Manager, assigns least-privilege people roles. Update ledger fields and add human-confirmed notes to task completions.
6. Human verifies actual state, records `last_verified` in ISO 8601 UTC, and sets status `verified` only after checking each requested item. This CLI does not validate external evidence or automatically gate status changes; use review procedures.
7. Run audit and inspect findings. Each finding is `unverified` until human or supported integration evidence is recorded. Complete tasks after checking.
8. For temporary team member offboarding, create tracked actions and perform actual removal/rotation manually in Meta/vault. Never represent pending actions as completed.

## Proxy handling
`health` checks a **neutral HTTPS test endpoint** with bounded attempts, explicit timeout and no credential logging. Approved proxy endpoints and secret refs must remain in company vault. For a real proxy deployment, supply an approved transport adapter that fetches secrets at runtime; none is shipped here. Keep one proxy sticky during a session, rotate only between sessions or after verified network failure, pause for manual review on any platform challenge; do not rotate to evade restrictions. No actual proxy failover is claimed by this prototype.

## Operational reminders
`remind` records reminders/escalations but **does not send email/SMS**. Schedule it with cron or a company scheduler and connect an approved notification service. Overdue tasks become `escalated`; task identity and completion persist across process restarts. Weekly audit example: `0 9 * * 1 cd /path/to/project && python -m app.cli audit` (scheduler timezone applies).

## Evidence and limitations
- Reports are generated from local sample/test ledger; do not confuse `unverified` findings with integration-verified evidence.
- No supported Instagram signup automation or verification automation; no bypass of CAPTCHA, rate limits, enforcement or identity checks.
- No Meta API integration, actual vault SDK, real proxy adapter, notification delivery, device automation, or live-account walkthrough without client credentials and explicit authorization.
- Task notes reject common credential assignment patterns; do not enter secrets. Generated reports redact task notes, recovery email, phone and vault references. This is defense in depth, not a guarantee against arbitrary sensitive text. Vault references are non-secret identifiers but should still be treated as internal metadata.
- `offboard` creates pending actions, does not revoke real permissions. Audit tasks are idempotent. For production: add RBAC, encrypted DB, audit evidence links, reliable scheduler, notifications, proper proxy connector, and transaction isolation.

## 2–3 minute screen recording storyboard
0:00–0:25 show client-authorized real Instagram test account and company authorization context without exposing secrets; 0:25–0:55 show `register`, signup task and human handoff; 0:55–1:25 show completed verification and Meta/2FA screens redacted; 1:25–1:50 restart CLI and show same account/task IDs (no duplicate); 1:50–2:15 show audit/offboarding; 2:15–2:40 show proxy health and logs; 2:40–3:00 state blockers and honest limitations. **A short legacy local dashboard clip may be present, but it does not meet the requested 2–3 minute live account recording. Operator must record the required evidence.**

## AI disclosure
Implementation drafted with OpenAI ChatGPT (code, tests, documentation, architecture suggestions). Human operator must validate behavior and complete all platform steps.
