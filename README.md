# GAJAN Instagram Operations

## Senior AI Systems Engineer – Build Task

A Python-based prototype for secure Instagram account provisioning and operations management, developed for the GAJAN Group Holdings technical assessment.

## Features

- Instagram account provisioning coordination
- Human approval and verification workflows
- Task reminders, escalation, and interruption recovery
- Two-factor authentication status tracking
- Security audits and account register management
- Employee offboarding and access revocation workflows
- Proxy health checks, retries, and connection management
- Redacted operational reports and audit logs

## Technology Stack

- Python
- SQLite
- REST/HTTPS health checks
- Python unittest

## Project Structure

The `gajan_instagram_ops/` directory contains the application source code, tests, documentation, and sample reports.

## Installation and Setup

```bash
cd gajan_instagram_ops
python -m app.cli init
python -m unittest discover -s tests -v
bash demo.sh
```

Python 3.10 or later is recommended.

## Security and Compliance

This prototype uses human-controlled workflows for Instagram signup and verification. It does not bypass CAPTCHA, account restrictions, rate limits, or Meta security controls.

Passwords, recovery codes, and proxy credentials must be stored in an approved vault rather than in source code.

## Current Limitations

The client-authorized Instagram test account, Meta Business access, vault, and approved proxies have not yet been provided. Therefore, live Instagram provisioning and integration verification remain pending.

Demonstration reports are sample outputs, not evidence of completed live operations.

## Author

Saurav Kumar  
Senior AI Systems Engineer – Technical Assessment

## AI Tools Used

ChatGPT was used to assist with code development, documentation, testing guidance, and project structure.
