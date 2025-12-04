def print_board(board):
    """
    Печатает игровое поле 3x3.

    :param board: двумерный список 3x3, где каждый элемент — 'X', 'O' или '.'
    """
    for row in board:
        print(" ".join(row))
    print()


def check_winner(board):
    """
    Проверяет, есть ли победитель на доске.

    :param board: двумерный список 3x3
    :return: 'X', 'O', 'Tie' или None
    """
    # Проверка строк
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != '.':
            return row[0]
    # Проверка столбцов
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '.':
            return board[0][col]
    # Проверка диагоналей
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '.':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '.':
        return board[0][2]

    # Проверка на ничью
    if all(board[r][c] != '.' for r in range(3) for c in range(3)):
        return 'Tie'

    return None  # Игра не закончена


def minimax(board, depth, is_maximizing):
    """
    Рекурсивный алгоритм Минимакс. Возвращает оценку позиции.

    :param board: текущее состояние доски
    :param depth: текущая глубина рекурсии
    :param is_maximizing: True, если ходит X (максимизирует), False — если O
    :return: числовая оценка позиции (+10, -10, 0)
    """
    result = check_winner(board)

    if result == 'X':
        return 10
    elif result == 'O':
        return -10
    elif result == 'Tie':
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == '.':
                    board[r][c] = 'X'
                    score = minimax(board, depth + 1, False)
                    board[r][c] = '.'
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == '.':
                    board[r][c] = 'O'
                    score = minimax(board, depth + 1, True)
                    board[r][c] = '.'
                    best_score = min(score, best_score)
        return best_score


def find_best_move(board, player):
    """
    Находит лучший ход для указанного игрока (X или O).

    :param board: текущее состояние доски
    :param player: 'X' или 'O'
    :return: кортеж (row, col) и оценка хода
    """
    is_maximizing = (player == 'X')
    best_score = float('-inf') if is_maximizing else float('inf')
    best_move = (-1, -1)

    for r in range(3):
        for c in range(3):
            if board[r][c] == '.':
                board[r][c] = player
                score = minimax(board, 0, not is_maximizing)
                board[r][c] = '.'
                if is_maximizing:
                    if score > best_score:
                        best_score = score
                        best_move = (r, c)
                else:
                    if score < best_score:
                        best_score = score
                        best_move = (r, c)

    return best_move, best_score


def main():
    """
    Основная функция. Запрашивает формат ввода, определяет игрока,
    находит лучший ход и выводит результат.
    """
    print("Выберите формат ввода:")
    print("1 — одной строкой (например: XX.O..O..)")
    print("2 — по строкам (3 строки по 3 символа)")
    choice = input("Введите 1 или 2: ").strip()

    if choice == "1":
        print("Введите поле (9 символов, . — пустая клетка):")
        s = input().strip()
        if len(s) != 9 or not all(c in 'XO.' for c in s):
            print("Ошибка: неверный формат поля.")
            return
        board = [[s[i * 3 + j] for j in range(3)] for i in range(3)]

    elif choice == "2":
        print("Введите поле по строкам (по 3 символа):")
        rows = []
        for i in range(3):
            line = input(f"Строка {i+1}: ").strip()
            if len(line) != 3 or not all(c in 'XO.' for c in line):
                print("Ошибка: каждая строка должна содержать ровно 3 символа X, O или .")
                return
            rows.append(line)
        board = [[rows[i][j] for j in range(3)] for i in range(3)]
        s = ''.join(rows)

    else:
        print("Ошибка: введите 1 или 2.")
        return

    count_x = s.count('X')
    count_o = s.count('O')

    winner = check_winner(board)
    if winner:
        print(f"Игра завершена. Результат: {winner if winner != 'Tie' else 'Ничья'}")
        if winner == 'X':
            print("+100 очков")
        elif winner == 'O':
            print("-100 очков")
        else:
            print("0 очков")
        return

    if count_x == count_o:
        current_player = 'X'
    elif count_x == count_o + 1:
        current_player = 'O'
    else:
        print("Ошибка: некорректное состояние игры.")
        return

    move, score = find_best_move(board, current_player)

    if move == (-1, -1):
        print("Нет доступных ходов.")
        return

    # Выполняем ход на доске
    r, c = move
    board[r][c] = current_player

    print("Рекомендуемый ход:")
    print_board(board)
    print(f"Оценка: {score}")

    # Определяем, какую награду вывести
    final_winner = check_winner(board)
    if final_winner == 'X':
        print("+100 очков")
    elif final_winner == 'O':
        print("-100 очков")
    elif final_winner == 'Tie':
        print("0 очков")
    else:
        print("+100 очков")  # За выполнение хода, если игра не закончена


if __name__ == "__main__":
    main()