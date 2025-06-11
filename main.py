import telebot
from casino import casino_5050
from user import register_user, get_user
from rofl import ROFL_COMMANDS

TOKEN = "7617127741:AAEYXIWVTdaDMY2FRhzqCWZOjO0ASofq_wE"
bot = telebot.TeleBot(TOKEN)

# /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    user = register_user(message.from_user.id, message.from_user.username)
    bot.reply_to(message, f"Привет, {message.from_user.first_name}! Тебе выдано 100000 ₡ на старт.")

# /help
@bot.message_handler(commands=['help'])
def help_handler(message):
    cmds = "\n".join(sorted(f"/{cmd}" for cmd in ROFL_COMMANDS))
    casino_commands = (
        "казино (сумма) — сыграть в 50/50\n"
        "слоты (сумма) — сыграть в слоты\n"
        "монета (сумма) — подбросить монету\n"
        "кости (сумма) — бросить кости\n"
        "угадай (число) (сумма) — угадать число\n"
        "дуэль (ник) (сумма) — дуэль с игроком\n"
        "баланс, б — показать баланс\n"
        "профиль — показать профиль"
    )
    text = (
        "Рофл-команды (можно писать с / или просто текстом):\n"
        f"{cmds}\n\n"
        f"Казино-игры:\n{casino_commands}\n\n"
        "Пример: казино 1000 — сыграть 1000 ₡ в 50/50."
    )
    bot.reply_to(message, text)

# /баланс, /б
@bot.message_handler(commands=['баланс', 'б'])
def balance_handler(message):
    user = get_user(message.from_user.id)
    if not user:
        bot.reply_to(message, "Ты не зарегистрирован, используй /start")
        return
    casino_money = user.get("casino_money", 0)
    job_money = user.get("job_money", 0)
    total = casino_money + job_money
    bot.reply_to(message, f"Твой баланс: {total} ₡\n(Казино: {casino_money}, Работа: {job_money})")

# /профиль
@bot.message_handler(commands=['профиль'])
def profile_handler(message):
    user = get_user(message.from_user.id)
    if not user:
        bot.reply_to(message, "Ты не зарегистрирован, используй /start")
        return

    username = user.get("username", "неизвестно")
    casino_money = user.get("casino_money", 0)
    job_money = user.get("job_money", 0)
    prefixes = user.get("prefix_list", [])
    prefix = user.get("owned_prefix", "Нет")
    businesses = user.get("businesses", {})

    biz_text = '\n'.join(
        f"{name}: территория {info.get('territory', 0)}, доход {info.get('income', 0)}"
        for name, info in businesses.items()
    ) or "Нет бизнесов"
    prefix_text = ', '.join(prefixes) if prefixes else "Нет префиксов"

    bot.reply_to(message, (
        f"Профиль @{username}:\n"
        f"Казино-деньги: {casino_money} ₡\n"
        f"Деньги с работы: {job_money} ₡\n"
        f"Бизнесы:\n{biz_text}\n"
        f"Префиксы: {prefix_text}\n"
        f"Текущий префикс: {prefix}"
    ))

# Все /команды
@bot.message_handler(func=lambda msg: msg.text and msg.text.startswith("/"))
def command_router(message):
    cmd = message.text[1:].split()[0].lower()

    if cmd in ROFL_COMMANDS:
        bot.reply_to(message, f"{message.from_user.first_name} использовал команду /{cmd}!")
        return

    if cmd == "казино":
        try:
            bet = int(message.text.split()[1])
        except (IndexError, ValueError):
            bot.reply_to(message, "Использование: /казино <ставка>")
            return
        user = get_user(message.from_user.id)
        if not user:
            bot.reply_to(message, "Ты не зарегистрирован, используй /start")
            return
        _, reply = casino_5050(message.from_user.id, bet)
        bot.reply_to(message, reply)
        return

    bot.reply_to(message, "Неизвестная команда. Введи /help для списка.")

# Рофл команды без слеша
@bot.message_handler(func=lambda msg: msg.text and not msg.text.startswith("/"))
def rofl_text_handler(message):
    parts = message.text.strip().lower().split()
    if not parts:
        return
    cmd = parts[0].replace(" ", "_")
    target = " ".join(parts[1:]) if len(parts) > 1 else None

    if cmd in ROFL_COMMANDS:
        if target:
            bot.reply_to(message, f"{message.from_user.first_name} использовал команду /{cmd} на {target}!")
        else:
            bot.reply_to(message, f"{message.from_user.first_name} использовал команду /{cmd}!")

if __name__ == "__main__":
    print("Бот запущен.")
    bot.infinity_polling()
