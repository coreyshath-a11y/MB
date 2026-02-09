#!/usr/bin/env python3
"""Fetch Discord channel messages for puzzle analysis."""
import json
import os
import sys
import time
import urllib.request
import urllib.error

TOKEN = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("DISCORD_TOKEN", "")
if not TOKEN:
    print("Usage: python3 fetch_discord.py <discord_token>")
    sys.exit(1)

CHANNELS = {
    "1470536551174901996": "general-or-meta",
    "1470505751029219422": "channel-12",
    "1470505671492632871": "channel-11",
    "1470505662210638038": "channel-10",
    "1470505652953551101": "channel-9",
    "1470505641607958540": "channel-8",
    "1470505629054664778": "channel-7",
    "1470505618493411339": "channel-6",
    "1470505599320981656": "channel-5",
    "1470505564508389419": "channel-3",
    "1470505546946838659": "channel-1-2",
}

OUTPUT_DIR = "analysis/discord"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def fetch_messages(channel_id, limit=100, before=None):
    """Fetch messages from a Discord channel."""
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages?limit={limit}"
    if before:
        url += f"&before={before}"

    req = urllib.request.Request(url)
    req.add_header("Authorization", TOKEN)
    req.add_header("User-Agent", "PuzzleAnalyzer/1.0")

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  HTTP Error {e.code}: {e.reason}")
        if e.code == 429:
            retry_after = float(e.headers.get("Retry-After", 5))
            print(f"  Rate limited, waiting {retry_after}s...")
            time.sleep(retry_after)
            return fetch_messages(channel_id, limit, before)
        return []


def fetch_channel_name(channel_id):
    """Fetch channel info to get the real name."""
    url = f"https://discord.com/api/v10/channels/{channel_id}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", TOKEN)
    req.add_header("User-Agent", "PuzzleAnalyzer/1.0")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            return data.get("name", "unknown")
    except Exception:
        return "unknown"


def fetch_all_messages(channel_id, max_messages=500):
    """Fetch all messages from a channel (up to max)."""
    all_messages = []
    before = None
    while len(all_messages) < max_messages:
        msgs = fetch_messages(channel_id, 100, before)
        if not msgs:
            break
        all_messages.extend(msgs)
        before = msgs[-1]["id"]
        if len(msgs) < 100:
            break
        time.sleep(0.5)  # rate limit courtesy
    return all_messages


print(f"Fetching messages from {len(CHANNELS)} channels...")
print(f"Output directory: {OUTPUT_DIR}")
print()

all_data = {}

for channel_id, label in CHANNELS.items():
    # Get real channel name
    real_name = fetch_channel_name(channel_id)
    print(f"Channel: #{real_name} ({label}) [{channel_id}]")

    messages = fetch_all_messages(channel_id)
    print(f"  Fetched {len(messages)} messages")

    if not messages:
        continue

    # Sort oldest first
    messages.sort(key=lambda m: m["id"])

    # Save raw JSON
    json_path = os.path.join(OUTPUT_DIR, f"{real_name}_{channel_id}.json")
    with open(json_path, "w") as f:
        json.dump(messages, f, indent=2)

    # Save readable text
    txt_path = os.path.join(OUTPUT_DIR, f"{real_name}_{channel_id}.txt")
    with open(txt_path, "w") as f:
        f.write(f"# Discord Channel: #{real_name}\n")
        f.write(f"# Channel ID: {channel_id}\n")
        f.write(f"# Messages: {len(messages)}\n")
        f.write("=" * 60 + "\n\n")

        for msg in messages:
            author = msg.get("author", {}).get("username", "unknown")
            content = msg.get("content", "")
            timestamp = msg.get("timestamp", "")[:19]
            embeds = msg.get("embeds", [])
            attachments = msg.get("attachments", [])

            f.write(f"[{timestamp}] {author}:\n")
            if content:
                f.write(f"  {content}\n")
            for embed in embeds:
                if embed.get("title"):
                    f.write(f"  [Embed] {embed['title']}\n")
                if embed.get("description"):
                    f.write(f"  {embed['description'][:200]}\n")
            for att in attachments:
                f.write(f"  [Attachment] {att.get('filename', 'file')} - {att.get('url', '')}\n")
            f.write("\n")

    all_data[real_name] = {
        "channel_id": channel_id,
        "message_count": len(messages),
        "files": {"json": json_path, "txt": txt_path},
    }
    print(f"  Saved to {txt_path}")
    time.sleep(1)  # rate limit between channels

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
total = sum(d["message_count"] for d in all_data.values())
print(f"Total messages fetched: {total}")
for name, data in all_data.items():
    print(f"  #{name}: {data['message_count']} messages")
print(f"\nFiles saved to {OUTPUT_DIR}/")
