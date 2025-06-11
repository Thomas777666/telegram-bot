import json
import os

DATA_FILE = "users.json"
_users = {}

def load_users():
    global _users
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        _users = json.load(f)

def save_users():
    global _users
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(_users, f, indent=2, ensure_ascii=False)

def register_user(user_id, username):
    global _users
    str_id = str(user_id)
    if str_id not in _users:
        _users[str_id] = {
            "id": user_id,
            "username": username or "",
            "casino_money": 100000,
            "job_money": 0,
            "prefix_list": [],
            "owned_prefix": None,
            "businesses": {},
            "rp_count": 0
        }
        save_users()
    return _users[str_id]

def get_user(user_id):
    global _users
    return _users.get(str(user_id))

def update_user(user_id, data):
    global _users
    _users[str(user_id)] = data
    save_users()

def can_transfer_job_money():
    return False

def can_transfer_casino_money(amount):
    MAX_TRANSFER = 5_000_000_000_000_000
    return 0 < amount <= MAX_TRANSFER

# Загружаем пользователей один раз при импорте
load_users()
