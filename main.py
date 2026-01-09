import os
import time
import json
import asyncio
from datetime import datetime
from instagrapi import Client
from dotenv import load_dotenv

load_dotenv()

IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")
DEVELOPER_ID = os.getenv("DEVELOPER_ID", "unknown")
MAX_SPAM_LIMIT = int(os.getenv("MAX_SPAM_LIMIT", "10"))

SESSION_FILE = "session/session.json"
RULES_FILE = "storage/rules.json"
WELCOME_FILE = "storage/welcome.json"
MUTE_FILE = "storage/mutes.json"

os.makedirs("session", exist_ok=True)
os.makedirs("storage", exist_ok=True)

bot_start_time = time.time()
cl = Client()


# ---------- helpers ----------

def load_json(path, default):
    if not os.path.exists(path):
        with open(path, "w") as f:
            json.dump(default, f)
        return default
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


rules_db = load_json(RULES_FILE, {})
welcome_db = load_json(WELCOME_FILE, {})
mute_db = load_json(MUTE_FILE, {})


def uptime():
    sec = int(time.time() - bot_start_time)
    h = sec // 3600
    m = (sec % 3600) // 60
    return f"{h}h {m}m"


def is_admin(thread, user_id):
    admins = [u.pk for u in thread.admins] if thread.admins else []
    return user_id in admins


# ---------- login ----------

def login():
    if os.path.exists(SESSION_FILE):
        cl.load_settings(SESSION_FILE)
        cl.login(IG_USERNAME, IG_PASSWORD)
    else:
        cl.login(IG_USERNAME, IG_PASSWORD)
        cl.dump_settings(SESSION_FILE)


# ---------- command handlers ----------

def cmd_info():
    return (
        "🤖 Group Automation Info\n\n"
        "• Purpose: Private Group Management\n"
        f"• Developer: @{DEVELOPER_ID}\n"
        "• Language: Python\n"
        "• Mode: Instagram Automation"
    )


def cmd_ping():
    return (
        "Pong 🏓\n"
        "Status: Online\n"
        f"Uptime: {uptime()}\n"
        "Mode: Group Automation\n"
        "Boss Mode: Active 😈"
    )


# ---------- main loop ----------

async def listen():
    while True:
        threads = cl.direct_threads(amount=20)

        for thread in threads:
            messages = cl.direct_messages(thread.id, amount=5)

            for msg in messages:
                if msg.user_id == cl.user_id:
                    continue

                text = msg.text or ""
                user_id = msg.user_id
                thread_id = thread.id

                if mute_db.get(str(thread_id), {}).get(str(user_id)):
                    continue

                # ----- USER COMMANDS -----
                if text == "/rules":
                    rules = rules_db.get(str(thread_id), "No rules set.")
                    cl.direct_send(rules, thread_id)

                if text == "/info":
                    cl.direct_send(cmd_info(), thread_id)

                # ----- ADMIN COMMANDS -----
                if not is_admin(thread, user_id):
                    continue

                if text.startswith("/setrules"):
                    content = text.replace("/setrules", "").strip()
                    rules_db[str(thread_id)] = content
                    save_json(RULES_FILE, rules_db)
                    cl.direct_send("✅ Rules updated.", thread_id)

                if text == "/onwelcome":
                    welcome_db[str(thread_id)] = True
                    save_json(WELCOME_FILE, welcome_db)
                    cl.direct_send("✅ Welcome enabled.", thread_id)

                if text == "/offwelcome":
                    welcome_db[str(thread_id)] = False
                    save_json(WELCOME_FILE, welcome_db)
                    cl.direct_send("❌ Welcome disabled.", thread_id)

                if text.startswith("/mute"):
                    if msg.mentioned_user_ids:
                        target = msg.mentioned_user_ids[0]
                        mute_db.setdefault(str(thread_id), {})[str(target)] = True
                        save_json(MUTE_FILE, mute_db)
                        cl.direct_send("🔇 User muted.", thread_id)

                if text.startswith("/kick"):
                    if msg.mentioned_user_ids:
                        target = msg.mentioned_user_ids[0]
                        try:
                            cl.direct_thread_remove_user(thread_id, target)
                            cl.direct_send("👢 User removed.", thread_id)
                        except:
                            cl.direct_send("❌ Cannot remove user.", thread_id)

                if text.startswith("/spam"):
                    parts = text.split(" ", 3)
                    if len(parts) < 4:
                        continue
                    target = msg.mentioned_user_ids[0]
                    count = int(parts[2])
                    spam_text = parts[3]

                    if count > MAX_SPAM_LIMIT:
                        cl.direct_send("❌ Spam limit exceeded.", thread_id)
                        continue

                    for _ in range(count):
                        cl.direct_send(f"@{target} {spam_text}", thread_id)
                        time.sleep(0.7)

                if text == "/ping":
                    cl.direct_send(cmd_ping(), thread_id)

        await asyncio.sleep(4)


# ---------- start ----------

if __name__ == "__main__":
    login()
    asyncio.run(listen())