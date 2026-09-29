# Contributing

Contributions that improve the workflow, setup instructions, or privacy controls are welcome.

1. Open an issue describing the problem or proposed change.
2. Make the change in `workflow.json` or the documentation and explain how you tested it.
3. Run `python3 scripts/validate_workflow.py` before opening a pull request.
4. Export n8n workflows without credentials, pinned execution data, chat history, tokens, or personal group IDs.

Keep `schema.sql` suitable for a fresh installation. Put changes needed by existing installations in a separate upgrade script and document when to run it. Never add destructive SQL to the fresh schema or upgrade scripts without explaining the migration.

The public workflow uses placeholders for the Telegram username and allowed group ID. Keep those placeholders in shared exports. Do not submit `.env`, real database connection strings, API keys, or screenshots showing secrets.
