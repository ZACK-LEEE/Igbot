Instagram Group Automation Bot

A Python-based Instagram group automation system that works like a Telegram-style bot, using an automation account (not the official IG Bot API).

This project is designed for group management, with admin-only commands, user-safe commands, and Render deployment support.


---

✨ Features

👥 User Commands (Group)

/rules → Show group rules

/info → Bot information & developer ID


🛡️ Admin Commands (Group)

/setrules <text> → Set or update group rules

/onwelcome → Enable welcome messages

/offwelcome → Disable welcome messages

/mute @user → Ignore a user's messages

/kick @user → Remove a user from group (bot must be admin)

/spam @user <count> <text> → Mention spam (limit enforced)

/ping → Check bot status (group + DM)


📩 Admin Commands (DM)

/ping → Check bot uptime and status



---

🔐 Permission System

Normal users can only use:

/rules

/info


Admins only:

All moderation commands

/ping



Admin detection is done via Instagram group admin list.


---

🧠 How It Works

Uses a real Instagram account as automation

The account must be admin in the group

Listens to group messages continuously

Parses commands and applies permission checks

Saves data locally (rules, mutes, welcome state)


This is not an official Instagram bot. It uses private APIs via instagrapi.


---

📦 Project Structure

project/
│
├── main.py              # Main entry point
├── requirements.txt    # Python dependencies
├── session/             # IG login session (auto-created)
├── storage/             # Rules, welcome, mute data
│   ├── rules.json
│   ├── welcome.json
│   └── mutes.json
└── README.md


---

⚙️ Environment Variables (Required)

Set these in Render → Environment (do NOT hardcode):

IG_USERNAME=your_instagram_id
IG_PASSWORD=your_instagram_password
DEVELOPER_ID=lll_roronoa_zoro_lll
MAX_SPAM_LIMIT=10


---

🚀 Deployment (Render)

1. Push this repo to GitHub


2. Create a Background Worker on Render


3. Connect the GitHub repository


4. Set the Environment Variables


5. Start command:

python main.py


6. Enable auto-restart


7. (Optional) Use UptimeRobot to keep Render awake




---

🧾 Git Ignore Rules

Add this to .gitignore:

session/
storage/
.env

This keeps credentials and runtime data safe.


---

⚠️ Important Notes

Instagram does not officially support bots

Account may face limits if abused

Use realistic delays and moderation

Fake/test accounts recommended


This project is intended for private groups and educational use.


---

🧑‍💻 Developer

Developer ID: @lll_roronoa_zoro_lll

Language: Python

Mode: Instagram Automation Account



---

✅ Status

Production-ready • Render-compatible • GitHub-safe


---

If Instagram changes APIs, minor maintenance may be required.
