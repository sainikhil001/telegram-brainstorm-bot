#!/usr/bin/env python3
"""Check the public n8n export and its schema before sharing it."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
workflow = json.loads((ROOT / "workflow.json").read_text(encoding="utf-8"))
schema = (ROOT / "schema.sql").read_text(encoding="utf-8")
upgrade = (ROOT / "upgrade-mode.sql").read_text(encoding="utf-8")
nodes = {node["name"]: node for node in workflow["nodes"]}
errors = []


def check(condition, message):
    if not condition:
        errors.append(message)


required_nodes = {
    "Telegram Trigger",
    "Parse command",
    "Save user and load context",
    "Needs AI?",
    "Build AI request",
    "Ask AI",
    "Extract AI reply",
    "Reply in Telegram",
    "Save bot reply",
    "Prepare direct reply",
    "Send direct reply",
}
check(required_nodes <= nodes.keys(), "A required V2 node is missing")
check(not workflow.get("active"), "Public export should not be active")
check(not workflow.get("pinData"), "Remove pinned execution data before publishing")
check(
    all(not node.get("credentials") for node in workflow["nodes"]),
    "Remove attached n8n credential IDs from the export",
)

connections = workflow.get("connections", {})
for source, outputs in connections.items():
    check(source in nodes, f"Connection source does not exist: {source}")
    for branch in outputs.get("main", []):
        for target in branch:
            check(target["node"] in nodes, f"Connection target does not exist: {target['node']}")

if "Parse command" in nodes:
    parser = nodes["Parse command"]["parameters"]["jsCode"]
    check("REPLACE_WITH_BOT_USERNAME" in parser, "Restore the public bot username placeholder")
    check("REPLACE_WITH_GROUP_CHAT_ID" in parser, "Restore the public group ID placeholder")
    for command in ("brainstorm", "challenge", "summary", "exit", "help"):
        check(f"'{command}'" in parser, f"Parser is missing /{command}")

if "Save user and load context" in nodes:
    query = nodes["Save user and load context"]["parameters"]["query"]
    check("$1::bigint" in query and "$8" in query, "Context query lost its bound parameters")
    check("message_id <> $4::bigint" in query, "History may duplicate the current user message")

if "Build AI request" in nodes:
    builder = nodes["Build AI request"]["parameters"]["jsCode"]
    check("messages.push({role: 'user'" in builder, "AI request is missing the current user message")

for table in ("brainstorm_messages", "brainstorm_mode"):
    check(f"CREATE TABLE IF NOT EXISTS {table}" in schema, f"Fresh schema is missing {table}")
check("CREATE TABLE IF NOT EXISTS brainstorm_mode" in upgrade, "V1 upgrade is missing the mode table")

if errors:
    raise SystemExit("Validation failed:\n- " + "\n- ".join(errors))

print(f"Validated {len(nodes)} nodes, connections, placeholders, and database schema.")
