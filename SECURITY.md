# Security and privacy

## Secrets

Keep the Telegram token, OpenAI API key, and PostgreSQL password in n8n credentials. Do not place them in `workflow.json`, issues, pull requests, screenshots, or a committed `.env` file. `.gitignore` excludes local `.env` files, but it cannot remove secrets already committed or pasted elsewhere.

If a secret is exposed, revoke or rotate it at its provider, update the n8n credential, and remove the exposed value from public material. Treat the old value as compromised even after deleting a GitHub commit.

## Group access and stored data

The **Parse command** node restricts processing to the configured Telegram group ID. Set it before publishing. The database stores the messages sent to the bot, bot replies, Telegram identifiers, names, and mode state. The workflow sends recent bot conversation content to the configured OpenAI API account. Do not use it for confidential or regulated data without reviewing your organization's requirements and adding appropriate access controls and retention.

This repository has no automated data retention. Delete old rows with a separately reviewed database maintenance process if your team needs a retention limit.

## Reporting

Please do not put a security issue or leaked credential in a public GitHub issue. Contact the repository owner privately through their GitHub profile and include a short description and reproduction steps. If a token is already exposed, rotate it immediately.
