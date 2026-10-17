#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export OPS_DB="${OPS_DB:-$(mktemp -u /tmp/gajan-demo-XXXXXX.db)}"
python -m app.cli init
python -m app.cli register --brand DEMO_BRAND --owner test-ops --handle demo_brand_candidate
python -m app.cli task --account 1 --kind instagram_signup_verification --owner test-ops --days 1
python -m app.cli register --brand DEMO_BRAND --owner test-ops --handle demo_brand_candidate
python -m app.cli remind
python -m app.cli audit
python -m app.cli offboard --account 1 --person designated_temporary_test_member
python -m app.cli report --folder demo_output
python -m unittest discover -s tests -v
printf 'Demo complete. Local-only ledger: %s; reports: demo_output/\n' "$OPS_DB"
