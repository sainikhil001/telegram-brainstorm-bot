# Telegram business brainstorm bot

The importable V2 n8n workflow is `workflow.json`. It starts in normal chat mode. `/brainstorm` and `/challenge` switch the whole group topic into a persistent, more proactive mode; `/exit` returns it to normal. `/summary` gives a one-time recap without changing the active mode. Text replies to the bot continue the conversation in whichever mode is active. The bot does not read unrelated group messages. For a project overview, see [README.md](README.md).

## 1. Create the Telegram bot

1. Open [@BotFather](https://t.me/BotFather) in Telegram and send `/newbot`.
2. Choose a name and username. Save the token privately; do not paste it into the workflow JSON.
3. Send `/setcommands` to BotFather, choose your bot, and paste:

   ```text
   brainstorm - Generate ideas and quick tests
   challenge - Find risks and weak assumptions
   summary - Summarize recent bot discussions
   exit - Return to normal conversation
   help - Show commands
   ```

4. Add the bot to your team group. Keep BotFather's default group privacy setting enabled. Members can call commands or reply to the bot. A command menu only displays commands; the n8n workflow implements them.

## 2. Prepare PostgreSQL

**What these terms mean:** PostgreSQL is the database software that stores the bot's conversation history. A *provider* is a company that runs that database for you. `schema.sql` is a small text file containing the instructions to create the table the workflow expects. You do not need to install PostgreSQL on your computer for the hosted option below.

### Easiest hosted option: Neon

1. Create an account at [Neon](https://console.neon.tech/) and create a new **project** named, for example, `telegram-brainstorm`. Neon creates a PostgreSQL database as part of the project; its default database is commonly named `neondb`. You do not need to create another database inside it.
2. Open the project's **SQL Editor**. Open [`schema.sql`](schema.sql) on your computer, copy **all** its contents, paste them into the SQL Editor, and click **Run**. This creates the conversation table and the mode table. The file is run **once**; the workflow then updates them automatically. If you already ran an earlier version of `schema.sql`, run only [`upgrade-mode.sql`](upgrade-mode.sql) to add the mode table.
3. To check that it worked, run this in the SQL Editor:

   ```sql
   SELECT to_regclass('public.brainstorm_messages');
   ```

   The result should say `brainstorm_messages`. If it says `null`, make sure the SQL Editor is connected to the database you just created, then run the contents of `schema.sql` again. The script uses `IF NOT EXISTS`, so rerunning it is safe.
4. On the Neon project dashboard, click **Connect** and view its connection details. Keep the password and complete connection string private. You will enter the separate values into n8n:

   | Neon connection detail | n8n Postgres credential field |
   | --- | --- |
   | Host, such as `ep-example.region.aws.neon.tech` | **Host** |
   | Database, often `neondb` | **Database** |
   | User / role | **User** |
   | Password | **Password** |
   | Port, normally `5432` | **Port** |
   | `sslmode=require` | **SSL → Require** |

   Neon may show one **Connection string** instead of separate fields. Read it as
   `postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require...`:
   **User** is before the colon, **Password** is between the colon and `@`, **Host** is between `@` and the next `/`, and **Database** is after that `/` and before `?`. Neon also shows the database and role in separate dropdowns above the string. Click **Show password** to reveal the password for entering into n8n; do not share it in screenshots or chat. If the host wraps onto two lines on screen, copy the whole host as one continuous value. The `-pooler` part of the host is expected when **Connection pooling** is on.

5. In n8n, create a **Postgres** credential with those values. Leave **Ignore SSL Issues** off. Test and save the credential, then select it in both Postgres nodes in the workflow.

If you already have PostgreSQL with another host, use that host's SQL Editor and connection details instead. The bot's table can live in the same database as other tables, although keeping a separate database for this bot is easier to manage. If n8n runs in Docker, `localhost` refers to the n8n container; use a reachable database host. For n8n Cloud, the database must be reachable from n8n Cloud.

## 3. Import and connect the workflow

1. In n8n, choose **Import from File** and select `workflow.json`.
2. Create a **Telegram** credential using the BotFather token. Select it in **Telegram Trigger**, **Reply in Telegram**, and **Send direct reply**.
3. Select your Postgres credential in **Save user and load context** and **Save bot reply**.
4. Create an n8n **Header Auth** credential for the **Ask AI** HTTP Request node. Set header name to `Authorization` and value to `Bearer YOUR_OPENAI_API_KEY`. Select it in that node. Keep the API key in the credential, not the workflow JSON.
5. In **Parse command**, replace `REPLACE_WITH_BOT_USERNAME` with the bot username **without** `@`.
6. Find the group ID: test **Telegram Trigger**, send a message in the group, and read `message.chat.id` in its output. Replace `REPLACE_WITH_GROUP_CHAT_ID` in **Parse command** with that number, including its leading minus sign.
7. Save and **Publish** the workflow. In n8n versions that use an **Active** switch instead, activate it. The n8n instance must have a public HTTPS webhook that Telegram can reach. The bot will not keep listening after a manual test ends unless the workflow is published or active.

The workflow uses `gpt-4.1-mini` in **Build AI request**. Change that model there if your API account uses another compatible Chat Completions model.

## 4. Test in the group

Send `/help`, then `/brainstorm How could we validate demand for pet sitting in our neighborhood?`. The bot's messages now show `⚡ Brainstorm` while that mode is on. Reply directly to a bot message to continue. Try `/challenge Pet sitting subscription` to switch to `🎯 Challenge`, and `/exit` to return to short normal replies. `/summary` gives a one-time recap marked `📝 Summary`. In a group with several bots, use `/brainstorm@YourBotUsername` to address this one explicitly.

The current mode is shared by everyone in the same Telegram group topic. `/summary` can only use the latest 20 stored messages from interactions with this bot in that topic. It cannot summarize earlier or unrelated group chat. For longer-term business-plan memory, add a separate table of confirmed decisions and experiments; chat history alone is not a reliable source of truth.

### Replacing an already published older workflow

If the earlier bot workflow is already published, **Unpublish** it first. Run `upgrade-mode.sql` in the same database if you have not already done so. Then import this new `workflow.json` as a new workflow, select the credentials again, and replace the two placeholders at the top of **Parse command** with your bot username and group ID. Publish only the new workflow. Telegram has one webhook per bot, so keeping both workflows published can prevent messages from reaching the intended one.

## Troubleshooting

- **No Telegram Trigger event:** Check that the bot is in the group, that the workflow is active, and that n8n has a reachable HTTPS webhook. Telegram permits one webhook per bot, so avoid running a test listener and production listener for the same bot at once.
- **Trigger event but no reply:** Check the exact bot username and group ID in **Parse command**, then inspect the workflow execution for a credential or database error.
- **Postgres connection refused:** Confirm that the database host is reachable from n8n and that SSL, user, password, and firewall rules match your database provider.
- **AI request unauthorized:** Check the Header Auth credential, especially the `Bearer ` prefix and API key.
- **Command missing from Telegram menu:** Repeat `/setcommands` in BotFather. Menu registration does not affect the workflow's command parser.
