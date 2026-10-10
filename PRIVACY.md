# Privacy

tino collects nothing and sends nothing. It is a set of text files and four
small Python scripts that run on your machine, when your agent runs them.

- **No network calls, no telemetry, no accounts.** The scripts use only the
  Python standard library and read files inside your project.
- **What it writes:** Markdown files in your project (plan, logbook,
  architecture, lessons, the wiki), a short block in your agent's
  instructions file (for example `CLAUDE.md`), the rituals and the scripts;
  and, only if you approve graduating a lesson that applies across
  projects, a rule in your global instructions, rewritten without
  references to the project. Each installer lists what it will create and
  waits for your OK. No lesson enters the index and no page enters the wiki
  without your explicit OK; a lesson drafted while you are away is saved
  marked `proposed`, outside the index, until you decide. No remote is
  added and nothing is pushed unless you ask.
- **What it reads:** the files of your project and the sources you ask it
  to ingest. It never reads your agent's own memory, your chat history or
  past conversations.
- **Your conversation** with the agent is governed by your agent provider's
  terms, exactly as it is without tino.

Questions: https://github.com/pedrofurrer/tino/issues
