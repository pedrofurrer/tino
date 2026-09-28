# Security policy

## Reporting a vulnerability

Please report security problems privately, through GitHub's private
vulnerability reporting: open this repository's **Security** tab and choose
**Report a vulnerability**. Please do not open a public issue for them. Fixes
ship as a new release, crediting the reporter if they wish.

## Scope

tino is plain text plus four small Python scripts (standard library only)
that read files in your project and print a report. It makes no network calls
and runs nothing on its own: your agent runs the scripts when a ritual says
so, with the permissions you give it. Only one script writes, and only when
asked to: `rotate_logbook.py --apply` moves old logbook entries into the
logbook's archive.

Relevant reports include, for example:

- a script that writes outside the project, or writes when it should only
  read;
- a way for the content of a source to steer the agent through tino's
  rituals despite the rule that every source is data, never an instruction;
- anything in the installers that changes your agent's permissions or
  settings (they are designed not to).

Supported versions: the latest 2.x release.
