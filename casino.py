import random
from user import get_user, update_user

MIN_BET = 400

def check_bet(user_id, amount):
    user = get_user(user_id)
    if not user:
        return False, "Пользователь не зарегистрирован."
    if amount < MIN_BET:
        return False, f"Минимальная ставка — {MIN_BET} ₡."
    if amount > user['casino_money']:
        return False, "У тебя недостаточно казино-деньги."
    return True, None

def update_balance(user_id, amount):
    user = get_user(user_id)
    if user:
        user['casino_money'] += amount
        from user import update_user
        update_user(user_id, user)

def casino_5050(user_id, bet):
    ok, err = check_bet(user_id, bet)
    if not ok:
        return False, err
    win = random.choice([True, False])
    if win:
        update_balance(user_id, bet)
        return True, f"Ты выиграл {bet} ₡! Баланс пополнен."
    else:
        update_balance(user_id, -bet)
        return False, f"Ты проиграл {bet} ₡."

def slots(user_id, bet):
    ok, err = check_bet(user_id, bet)
    if not ok:
        return False, err
    symbols = ["🍒", "🍋", "🍉", "⭐", "🔔", "💎"]
    reel = [random.choice(symbols) for _ in range(3)]
    counts = {}
    for s in reel:
        counts[s] = counts.get(s, 0) + 1
    payout = 0
    if 3 in counts.values():
        payout = bet * 5
    elif 2 in counts.values():
        payout = bet * 2
    update_balance(user_id, payout - bet)
    res = " | ".join(reel)
    if payout > 0:
        return True, f"🎰 {res}\nТы выиграл {payout} ₡!"
    else:
        return False, f"🎰 {res}\nТы проиграл {bet} ₡."

def coin_flip(user_id, bet, choice):
    ok, err = check_bet(user_id, bet)
    if not ok:
        return False, err
    result = random.choice(["орёл", "решка"])
    if choice == result:
        update_balance(user_id, bet)
        return True, f"Монетка упала на {result}! Ты выиграл {bet} ₡."
    else:
        update_balance(user_id, -bet)
        return False, f"Монетка упала на {result}. Ты проиграл {bet} ₡."

def dice(user_id, bet):
    ok, err = check_bet(user_id, bet)
    if not ok:
        return False, err
    user_roll = random.randint(1, 6)
    bot_roll = random.randint(1, 6)
    if user_roll > bot_roll:
        update_balance(user_id, bet)
        return True, f"Ты бросил {user_roll}, бот — {bot_roll}. Ты выиграл {bet} ₡!"
    elif user_roll < bot_roll:
        update_balance(user_id, -bet)
        return False, f"Ты бросил {user_roll}, бот — {bot_roll}. Ты проиграл {bet} ₡."
    else:
        return None, f"Ничья! Оба бросили {user_roll}. Баланс не изменился."

def guess_number(user_id, bet, guess):
    ok, err = check_bet(user_id, bet)
    if not ok:
        return False, err
    answer = random.randint(1, 5)
    if guess == answer:
        update_balance(user_id, bet * 3)
        return True, f"Ты угадал число {answer}! Выигрыш: {bet*3} ₡."
    else:
        update_balance(user_id, -bet)
        return False, f"Неверно. Было {answer}. Проигрыш: {bet} ₡."

def duel(user1_id, user2_id, bet):
    # Проверка пользователей и ставок
    user1 = get_user(user1_id)
    user2 = get_user(user2_id)
    if not user1 or not user2:
        return False, "Один из участников не зарегистрирован."
    if bet < MIN_BET:
        return False, f"Минимальная ставка — {MIN_BET} ₡."
    if user1['casino_money'] < bet or user2['casino_money'] < bet:
        return False, "У одного из участников недостаточно денег."
    # Рандомный выбор победителя
    winner = random.choice([user1_id, user2_id])
    loser = user2_id if winner == user1_id else user1_id
    # Обновляем балансы
    update_balance(winner, bet)
    update_balance(loser, -bet)
    if winner == user1_id:
        return True, f"Ты выиграл дуэль и получил {bet} ₡!"
    else:
        return False, f"Ты проиграл дуэль и потерял {bet} ₡."
