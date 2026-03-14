import os
import json
from attr import define, field, asdict
from typing import List

# Hidden database folder
DB_FOLDER = os.path.join(os.path.expanduser("~"), ".database")
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER, exist_ok=True)  # create hidden folder

# Paths for files
USERS_FILE = os.path.join(DB_FOLDER, "users.json")
SETTINGS_FILE = os.path.join(DB_FOLDER, "settings.json")
LOGS_FILE = os.path.join(DB_FOLDER, "logs.json")


# --------------------------
# ATTR-BASED DATA CLASSES
# --------------------------

@define
class User:
    name: str
    nickname: str = ""
    language: str = "English"
    id: int = field(factory=int)  # can auto-generate or assign
    data: dict = field(factory=dict)  # any extra user data


@define
class Settings:
    version: str = "v1.0.0"
    last_update: str = ""
    preferences: dict = field(factory=dict)


@define
class LogEntry:
    user_id: int
    action: str
    timestamp: str


# --------------------------
# DATABASE HANDLERS
# --------------------------

def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


# --------------------------
# USER MANAGEMENT
# --------------------------

def add_user(user: User):
    users = load_json(USERS_FILE)
    users.append(asdict(user))
    save_json(USERS_FILE, users)


def get_user_by_name(name: str):
    users = load_json(USERS_FILE)
    for u in users:
        if u["name"] == name:
            return u
    return None


def update_user(user: User):
    users = load_json(USERS_FILE)
    for idx, u in enumerate(users):
        if u["name"] == user.name:
            users[idx] = asdict(user)
            break
    save_json(USERS_FILE, users)


# --------------------------
# SETTINGS MANAGEMENT
# --------------------------

def save_settings(settings: Settings):
    save_json(SETTINGS_FILE, asdict(settings))


def load_settings():
    data = load_json(SETTINGS_FILE)
    if data:
        return Settings(**data)
    return Settings()


# --------------------------
# LOG MANAGEMENT
# --------------------------

def add_log(entry: LogEntry):
    logs = load_json(LOGS_FILE)
    logs.append(asdict(entry))
    save_json(LOGS_FILE, logs)


def get_logs_for_user(user_id: int) -> List[dict]:
    logs = load_json(LOGS_FILE)
    return [l for l in logs if l["user_id"] == user_id]


# --------------------------
# EXAMPLE USAGE
# --------------------------
if __name__ == "__main__":
    # Create a user
    user = User(name="Alice", nickname="Ally", language="English", id=1)
    add_user(user)

    # Update settings
    settings = Settings(version="v1.0.0", last_update="2026-03-14")
    save_settings(settings)

    # Add a log entry
    log = LogEntry(user_id=1, action="Login", timestamp="2026-03-14 12:00:00")
    add_log(log)

    # Fetch user and logs
    fetched_user = get_user_by_name("Alice")
    user_logs = get_logs_for_user(1)

    print(f"User: {fetched_user}")
    print(f"Logs: {user_logs}")