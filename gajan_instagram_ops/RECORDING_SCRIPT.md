# 2–3 minute walkthrough script (record only after live access)

**0:00–0:20** Show repository and README. Say: “This is a compliant human-in-the-loop account operations prototype for one authorised test brand.”

**0:20–0:45** Show the authorised test Instagram account on the real site/app (mask recovery identifiers). Explain that signup and verification were completed by an authorised human, not automation. If not done, show the blocker and say so.

**0:45–1:10** Show `python -m app.cli register ...` and `task ...`. Show owner and deadline, then the human-confirmed task completion only if evidence exists.

**1:10–1:35** Show 2FA enabled, Business account and Meta roles on official screens without revealing secrets; if blocked, show tracked blocker instead.

**1:35–1:55** Restart the CLI and repeat registration; show unchanged account ID. Run `remind` and show escalation semantics (delivery is local-only).

**1:55–2:20** Run `audit` and `offboard`; show open tasks and evidence labels. Do not claim actual revocation unless the authorised operator performed it.

**2:20–2:40** Run `health --url https://example.com`; explain that it is a direct neutral endpoint check, **not a demonstration of proxy rotation**. If approved proxy integration is added, show the actual controlled failover separately.

**2:40–3:00** Open decision log and disclose incomplete integrations and missing client access. End with the exact next action and owner.

Screen recording is **not included**. Use Loom or another approved tool. Redact secrets, recovery data, access tokens, phone numbers, emails, and internal vault paths.
