import json
import os
import random
import time
from data.greetings import greetings

# --------------------------
# Paths
# --------------------------
INSTALL_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(INSTALL_DIR, "config.json")

# --------------------------
# Default values
# --------------------------
user_name = "User"
nickname = ""
language = "English"

# --------------------------
# Build info
# --------------------------
CURRENT_BUILD = 1
LATEST_BUILD = 1  # update for future releases
PUBLISHED_DATE = "March 14th 2026"

# --------------------------
# Load config if exists
# --------------------------
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        user_name = data.get("name", user_name)
        nickname = data.get("nickname", nickname)
        language = data.get("language", language)

# --------------------------
# Nickname prompt
# --------------------------
use_nick = False
if nickname:
    choice = input(f'Your nickname is: "{nickname}"\nDo you want me to call you by your nickname this session? (Y/N): ')
    if choice.strip().lower() == "y":
        use_nick = True

display_name = nickname if use_nick else user_name

# --------------------------
# Welcome message
# --------------------------
welcome_text = greetings.get(language, greetings["English"])["welcome"].format(name=display_name)
print(welcome_text)
print("\nType 'help' to see what I can do.")

# --------------------------
# Main command loop
# --------------------------
while True:
    cmd = input("Opera> ").strip().lower()

    if cmd == "exit":
        print("Initializing logout...")
        time.sleep(1.5)
        print("Goodbye! 🎵")
        time.sleep(1)
        break

    elif cmd == "help":
        print("Available commands: help, greet, hi, operainfo, exit")

    elif cmd == "greet":
        print(welcome_text)

    elif cmd == "hi":
        hi_list = greetings.get(language, greetings["English"])["hi"]
        print(random.choice(hi_list))

    elif cmd == "operainfo":
        print()
        print("Opera v1")
        print(f"Build {CURRENT_BUILD}")
        print(f"Published Date: {PUBLISHED_DATE}")
        print("Made in the Czech Republic 🇨🇿")
        if CURRENT_BUILD < LATEST_BUILD:
            print("Please upgrade to the latest version of Opera, if you want to upgrade here is the link: https://github.com/honzik233/opera.org")

    else:
        print(f"I don't understand '{cmd}'. Type 'help' for commands.")