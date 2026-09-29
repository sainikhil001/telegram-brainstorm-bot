# Telegram Brainstorm Bot

An n8n workflow for a team Telegram group. The bot joins conversations when someone replies to it or uses a command. In normal mode it gives brief, friendly replies. Brainstorm and challenge modes give the team more focused help with business ideas.

**V2 is the supported version.** The earlier prototype is described in [CHANGELOG.md](CHANGELOG.md), but is not offered as a separate installation because V2 fixes its conversation context and adds persistent modes.

## What it does

| Message | Result |
| --- | --- |
| Reply to a bot message | Chat in the current mode |
| `/brainstorm <idea>` | Enter brainstorm mode and explore the idea; replies start with `⚡ Brainstorm` |
| `/challenge <idea>` | Enter critique mode; replies start with `🎯 Challenge` |
| `/summary` | Recap recent conversations with the bot once, marked `📝 Summary`; the current mode stays on |
| `/exit` | Return to short, normal replies |
| `/help` | Show the commands |

`/brainstorm` or `/challenge` without an idea also switches modes. The mode is shared by everyone in the same Telegram group topic. Normal replies are brief; command modes aim for medium length. The bot uses a warm female persona while remaining clear that it is an AI assistant.

The bot **does not read every group message**. It receives commands and messages sent as replies to the bot. Its summary covers only the latest 20 stored messages from those interactions in the same topic.

## How it works

```text
Telegram group message
  → n8n Telegram Trigger
  → Parse command and check the allowed group
  → PostgreSQL: save user message, load mode and recent context
  → direct command reply, or OpenAI request
  → reply in Telegram
  → PostgreSQL: save AI reply
```

The workflow uses [n8n](https://n8n.io/), a Telegram bot created with [BotFather](https://t.me/BotFather), [PostgreSQL](https://www.postgresql.org/) (for example, [Neon](https://neon.tech/)), and an OpenAI API key. The importable file is [workflow.json](workflow.json); the database schema is [schema.sql](schema.sql).

## Set up

Follow [SETUP.md](SETUP.md) in order. In brief:

1. Create a Telegram bot, add it to one team group, and register its commands with BotFather.
2. Run `schema.sql` in your PostgreSQL provider's SQL editor. If you used the V1 schema already, run only [upgrade-mode.sql](upgrade-mode.sql).
3. Import `workflow.json` into n8n and select your Telegram, Postgres, and OpenAI Header Auth credentials in the relevant nodes.
4. In **Parse command**, replace `REPLACE_WITH_BOT_USERNAME` and `REPLACE_WITH_GROUP_CHAT_ID`.
5. Publish the workflow and test `/help`, `/brainstorm`, and `/exit` in the group.

If V1 is already published, unpublish it before publishing V2. One Telegram bot should have one active webhook listener.

## Credentials and privacy

The workflow export contains no API keys, passwords, or n8n credential IDs. Configure those in n8n's credential manager. [`.env.example`](.env.example) is a reference for the values you will need; **the imported workflow does not load a local `.env` file**. If you make a local `.env`, it is ignored by Git. Never commit real tokens or a Neon connection string.

The database stores names, Telegram user IDs, chat IDs, messages sent to the bot, its replies, and the current mode. Team members should know that their interactions with the bot are stored and sent to the configured AI service. Set your own retention policy before using the bot with sensitive discussions. This starter does not include an automatic deletion job.

## Project files

| File | Purpose |
| --- | --- |
| [workflow.json](workflow.json) | Importable V2 n8n workflow |
| [schema.sql](schema.sql) | Fresh PostgreSQL schema |
| [upgrade-mode.sql](upgrade-mode.sql) | V1 database upgrade |
| [SETUP.md](SETUP.md) | Step by step setup and troubleshooting |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute safely |
| [SECURITY.md](SECURITY.md) | Credential and incident guidance |

This project is licensed under the [MIT License](LICENSE).
