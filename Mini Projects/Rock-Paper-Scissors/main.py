import random
from colorama import init, Fore, Style

init(autoreset=True)

ACTIONS = ["камень", "ножницы", "бумага"]

# Правила: каждый ключ побеждает свой value
RULES = {
    "камень": "ножницы",
    "ножницы": "бумага",
    "бумага": "камень"
}

def get_counter_move(move: str) -> str:
    """Возвращает ход, который побеждает указанный."""
    for winner, loser in RULES.items():
        if loser == move:
            return winner
    return move  # на случай некорректного ввода (теоретически недостижимо)

def predict_move_from_history(history: list[str]) -> str:
    """Предсказывает следующий ход игрока по истории."""
    if len(history) < 2:
        return random.choice(ACTIONS)

    # Если игрок дважды подряд сделал один ход — ожидаем повтор
    if history[-1] == history[-2]:
        return history[-1]

    # Иначе — выбираем самый частый ход из всей истории
    counts = {action: history.count(action) for action in ACTIONS}
    return max(counts, key=counts.get)

def get_bot_move(difficulty: str, user_history: list[str]) -> str:
    """Выбирает ход бота в зависимости от режима сложности."""
    if difficulty == "1":
        return random.choice(ACTIONS)
    elif difficulty == "2":
        return "бумага"  # фиксированный ход — "глупый" режим
    elif difficulty == "3":
        # Против умного бота: бьём предсказанный ход игрока
        predicted = predict_move_from_history(user_history)
        return get_counter_move(predicted)
    else:
        return random.choice(ACTIONS)  # fallback на случай некорректных данных

def print_welcome():
    print(f"Здравствуйте!\nВас приветствует {Fore.CYAN}консольный чат-бот{Style.RESET_ALL} для игры «камень-ножницы-бумага».")
    print(f"Начните игру командой {Fore.BLUE}/start{Style.RESET_ALL}, завершите игру — {Fore.BLUE}/stop{Style.RESET_ALL}, выйдите из программы — {Fore.BLUE}/quit{Style.RESET_ALL}.")

def get_main_command() -> str:
    """Принимает команду в главном меню до начала игры."""
    while True:
        cmd = input(f">>>{Fore.GREEN}").strip().lower()
        print(Style.RESET_ALL, end="")
        if cmd in ["/start", "/quit"]:
            return cmd
        elif cmd == "/stop":
            print("Игра ещё не начата. Используйте /start для начала.")
        else:
            print("Некорректная команда. Доступны: /start, /quit.")

def get_in_game_command() -> str:
    """Принимает ввод во время игры: ход или команда."""
    while True:
        user_input = input(f">>>{Fore.GREEN}").strip().lower()
        print(Style.RESET_ALL, end="")
        if user_input in ("/stop", "/quit"):
            return user_input
        elif user_input in ACTIONS:
            return user_input
        else:
            print("Введите «камень», «ножницы», «бумага», /stop или /quit.")

def get_difficulty() -> str:
    print("Выберите сложность:")
    print("1 — Случайная (бот ходит случайно)")
    print("2 — Лёгкая (бот всегда выбирает «бумага»)")
    print("3 — Умная (бот анализирует ваши ходы)")
    while True:
        diff = input(f">>>{Fore.GREEN}").strip()
        print(Style.RESET_ALL, end="")
        if diff in ["1", "2", "3"]:
            return diff
        print("Введите 1, 2 или 3.")

def display_round_result(user_move: str, bot_move: str) -> int:
    """Выводит результат раунда и возвращает +1, -1 или 0."""
    if user_move == bot_move:
        print(f"{Fore.YELLOW}Ничья!{Style.RESET_ALL}")
        return 0
    elif RULES[user_move] == bot_move:
        print(f"{Fore.GREEN}{user_move}{Style.RESET_ALL} бьёт {Fore.CYAN}{bot_move}{Style.RESET_ALL}!")
        print(f"{Fore.GREEN}Вы выиграли{Style.RESET_ALL} этот раунд!")
        return 1
    else:
        print(f"{Fore.CYAN}{bot_move}{Style.RESET_ALL} бьёт {Fore.GREEN}{user_move}{Style.RESET_ALL}.")
        print(f"{Fore.RED}Вы проиграли{Style.RESET_ALL} этот раунд.")
        return -1

def main():
    print_welcome()
    while True:
        command = get_main_command()
        if command == "/quit":
            print("До скорых встреч!")
            return

        # Начинаем новую игру
        difficulty = get_difficulty()
        user_history = []
        user_score, bot_score = 0, 0
        print("Игра началась! Введите свой ход, /stop или /quit.")

        while True:
            user_input = get_in_game_command()

            if user_input == "/stop":
                print("\nИгра завершена!")
                print(f"Счёт: {Fore.GREEN}Игрок{Style.RESET_ALL} — {user_score}, {Fore.CYAN}Бот{Style.RESET_ALL} — {bot_score}")
                break  # возврат в главное меню

            if user_input == "/quit":
                print("\nИгра завершена!")
                print(f"Счёт: {Fore.GREEN}Игрок{Style.RESET_ALL} — {user_score}, {Fore.CYAN}Бот{Style.RESET_ALL} — {bot_score}")
                print("До скорых встреч!")
                return

            # Обрабатываем ход игрока
            user_move = user_input
            user_history.append(user_move)
            bot_move = get_bot_move(difficulty, user_history)
            print(f"{Fore.CYAN}Бот{Style.RESET_ALL} выбрал: {Fore.CYAN}{bot_move}{Style.RESET_ALL}")

            result = display_round_result(user_move, bot_move)
            if result == 1:
                user_score += 1
            elif result == -1:
                bot_score += 1

if __name__ == "__main__":
    main()