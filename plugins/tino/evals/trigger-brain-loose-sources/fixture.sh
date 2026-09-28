#!/usr/bin/env bash
# Seeds the empty workspace with the project this case needs.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../../.." && pwd)"
SRC="$REPO/tests/fixtures/bakery-base-en"
cp -R "$SRC/." .
git init -q -b main
git config user.name "Owner"
git config user.email "owner@example.com"
git add -A
git commit -q -m "Project before tino"
