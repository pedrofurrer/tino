# Optional guardrails for Claude Code

tino works fully without these. They turn three rules into configuration,
so they no longer depend on the agent remembering them. Claude Code's own
documentation says its instruction files are context, not enforced
configuration.

tino's installers do not write them. If you want them, add them yourself
to `.claude/settings.json`, which is versioned and applies to everyone on
the project, or to `.claude/settings.local.json`, which applies only on
your machine. If the file already exists, merge the keys; do not replace
the file. Check Claude Code's current documentation on permissions and
hooks when you set them up, because both change over time.

Paths below assume the scripts live in `scripts/`. With the Spanish set,
use the Spanish names: `BITACORA-archivo.md`, `lint_continuidad.py`,
`lint_indice.py` and `conocimiento`.

## 1. The logbook archive cannot be edited (continuity)

A `deny` rule for `Edit` blocks the agent's file tools, and the terminal
commands Claude Code recognizes, from editing the archive. It does not
stop a script that opens the file on its own, so the rotator keeps
working.

```json
{
  "permissions": {
    "deny": ["Edit(/LOGBOOK-archive.md)"]
  }
}
```

## 2. Resume with the thread (continuity)

On resuming a session or after compacting the context, a hook re-shows
the PLAN's "where we left off" and 🔄 lines. Those lines are what gets lost
first in a compaction.

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "resume|compact",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"${CLAUDE_PROJECT_DIR}/scripts/lint_continuity.py\" --root \"${CLAUDE_PROJECT_DIR}\" --resume"
          }
        ]
      }
    ]
  }
}
```

## 3. Raw sources are immutable (brain)

Before each edit with the agent's file tools, the index verifier runs in
guard mode and checks the target. If the target already exists in the
wiki's `sources/` folder, it blocks the edit and tells the agent why.

- Creating new raw files stays allowed, and so does the `sources/clips/`
  inbox.
- When in doubt, for example with input it does not understand, the guard
  lets the edit through.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"${CLAUDE_PROJECT_DIR}/scripts/lint_index.py\" --guard knowledge"
          }
        ]
      }
    ]
  }
}
```

## Limits

These rules protect against edits made with the agent's tools. They are
not a sandbox: a terminal command or a script could still write. To remove
a guardrail, delete its keys from the settings file.

A future, separate tino plugin may ship these as opt-in hooks.
