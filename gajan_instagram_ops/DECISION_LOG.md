# Decision log — GAJAN take-home (one page)

**Scope:** One authorized Instagram test brand. Build local orchestration and records first; human performs unsupported real-platform actions. No account creation was performed here because company test access was not supplied.

**Built:** Python stdlib CLI + SQLite persistent account/task/event register; idempotent account and task creation; human task ownership/deadlines/completion; overdue escalation state; weekly audit logic; offboarding action queue; neutral HTTPS endpoint health check with timeout/bounded retries; redacted JSON artifacts; unit tests.

**Skipped / pending:** Actual Instagram signup and verification (human only), actual 2FA/Meta linking, vault SDK, approved proxy routing/failover, notification delivery, and screen recording (all require client access). Optional 2-device sample-app automation deferred because mandatory secure path has higher evaluation value.

**Failures / recovery:** Process interruption retains state in SQLite; re-running register/task does not duplicate. Network health failures return a bounded unhealthy result. Human verification blockers remain tasks. Reminder delivery is not implemented and must not be claimed. No bypass of platform security challenges.

**Evidence integrity:** Reports contain local state only. Audit findings labelled `unverified` until supported verification. Offboarding remains pending until human action. No actual platform or proxy integration is claimed.

**Next day:** Integrate company vault SDK and notification service; build explicit evidence attachments and approval gates; wire supported Meta Graph API capabilities where authorized; implement approved proxy transport with sticky session and neutral-endpoint rotation tests; add secure UI and centralized scheduler.

**AI tools:** OpenAI ChatGPT used for architecture, Python implementation, documentation and test design. Operator review and live walkthrough still required.
