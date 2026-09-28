---
type: regex
target:
  source: file
  path: "CLAUDE.md"
pattern: '^#{1,6} [^\n]*(closing ritual|save progress)'
match: not_contains
flags: im
---
