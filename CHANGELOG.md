# Changelog

## V2 — conversation modes (current)

- Added group-topic modes: normal, `/brainstorm`, and `/challenge`, with `/exit` to reset.
- Added visible mode labels and a one-shot `/summary` command.
- Made normal chat concise and the active idea modes more proactive.
- Stored mode in PostgreSQL so it survives new messages and workflow runs.
- Fixed conversation context so the current user message is included in the AI request once.
- Kept credentials outside the workflow export.

## V1 — initial prototype

- Added Telegram command handling, OpenAI replies, and PostgreSQL conversation history.
- Superseded by V2. The original export is intentionally not distributed as an installable version because it had a conversation-context issue.

There are no automated database migrations or version tags yet. For an existing V1 database, run `upgrade-mode.sql` before switching to V2. For a new database, run `schema.sql`.
