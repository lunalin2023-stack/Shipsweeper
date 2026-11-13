# ==========================================
# display.py - User Interface
# ==========================================

import os
import sys

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 24
BOARD_SIZE = 10
COLUMN_LETTERS = "ABCDEFGHIJ"

WATER_VALUES = (None, "", ".", "~", "water", "empty", 0, False)


def fit(text):
    return str(text)[:SCREEN_WIDTH]


def center(text):
    return fit(str(text).center(SCREEN_WIDTH).rstrip())


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_lines(lines):
    for line in list(lines)[: SCREEN_HEIGHT - 1]:
        print(fit(line))


def coord_to_text(row, col):
    return f"{COLUMN_LETTERS[col]}{row + 1}"


def attack_symbol(value):
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, int):
        return str(value) if 0 <= value <= 8 else "?"
    text = str(value).strip().lower()
    if text in ("", ".", "~"):
        return None
    if text in ("x", "hit"):
        return "X"
    if text in ("#", "sunk"):
        return "#"
    if text in ("o", "miss"):
        return "o"
    if len(text) == 1 and text.isdigit():
        return text
    return text[0].upper()


def cell_symbol(ship_value, attack_value, hide_ships=False):
    shot = attack_symbol(attack_value)
    is_ship = ship_value not in WATER_VALUES

    if shot is not None:
        if is_ship and not hide_ships and shot.isdigit():
            return "S"
        return shot

    if is_ship and not hide_ships:
        return "S"
    return "."


def board_lines(board, attack_board, hide_ships=False):
    lines = ["   " + " ".join(COLUMN_LETTERS)]
    for row in range(BOARD_SIZE):
        cells = []
        for col in range(BOARD_SIZE):
            ship = board[row][col] if board else None
            shot = attack_board[row][col] if attack_board else None
            cells.append(cell_symbol(ship, shot, hide_ships))
        lines.append(f"{row + 1:>2} " + " ".join(cells))
    return lines


def display_board(board, attack_board, hide_ships=False):
    title = "ENEMY WATERS" if hide_ships else "YOUR FLEET"
    print_lines(["    " + title] + ["    " + line for line in
                                     board_lines(board, attack_board, hide_ships)])


def display_both_boards(player_board, player_attacks,
                        computer_board, computer_attacks):
    left = ["YOUR FLEET"] + board_lines(player_board, player_attacks)
    right = ["ENEMY WATERS"] + board_lines(computer_board, computer_attacks,
                                         hide_ships=True)
    lines = ["    " + l.ljust(31) + r for l, r in zip(left, right)]
    lines.append("    Key: S ship  X hit  # sunk  o miss  "
                 "0-8 ship parts touching that square")
    print_lines(lines)


def display_message(message):
    if isinstance(message, (list, tuple)):
        for line in message:
            print(fit(" " + str(line)))
    elif message:
        print(fit(" " + str(message)))


def attack_message(who, row, col, result, clue=None):
    where = coord_to_text(row, col)
    if result == "sunk":
        return f"{who} fired at {where}: HIT - ship sunk!"
    if result == "hit":
        return f"{who} fired at {where}: HIT!"
    if clue is not None:
        return f"{who} fired at {where}: miss. Clue: {clue} ship part(s) nearby."
    return f"{who} fired at {where}: miss."


def display_radar(row, col, results):
    clues = {square: clue for square, clue in results}
    rows = sorted({r for r, _ in clues})
    cols = sorted({c for _, c in clues})
    lines = [center("=== RADAR SCAN ==="),
             center(f"Centre: {coord_to_text(row, col)}"), "",
             "        " + " ".join(COLUMN_LETTERS[c] for c in cols)]
    for r in rows:
        lines.append(f"     {r + 1:>2} " +
                     " ".join(str(clues.get((r, c), " ")) for c in cols))
    lines += ["", "  Each number = ship parts touching that square",
              "  (sideways or diagonally). Sunk ships are not counted."]
    print_lines(lines)


def display_shop(items):
    try:
        import shop
        descriptions = {n: i["description"] for n, i in shop.SHOP_ITEMS.items()}
    except (ImportError, AttributeError, KeyError, TypeError):
        descriptions = {}

    lines = [center("=== TACTICAL SHOP ===")]
    for number, (name, price) in enumerate(items.items(), start=1):
        line = f"  {number}. {name.title():<14} ${price:<4} {descriptions.get(name, '')}"
        lines.append(line.rstrip())
    lines.append("  Type item no./name to buy. Enter with empty input to leave.")
    print_lines(lines)


def display_title_screen():
    print_lines([
        center("S H I P S W E E P E R"),
        center("Tactical Command Edition"),
        "",
        "  OBJECTIVE: Sink the enemy fleet before they sink yours!",
        "",
        "  HOW TO PLAY:",
        "  - Enter a coordinate (e.g., C4) to fire.",
        "  - A MISS reveals numbers showing how many ship parts",
        "    touch that tile (like Minesweeper).",
        "  - When a ship sinks, nearby clues decrease dynamically.",
        "  - Earn cash for hits to spend in the SHOP.",
        "",
        "  COMMANDS: Type 'SHOP' or 'RADAR' during your turn.",
        "            Type 'Q' to quit the game.",
        "",
        center("Press Enter to deploy your fleet..."),
    ])


def display_menu(options, title="MENU"):
    lines = [center(f"=== {title} ===")]
    lines += [f"  {i}. {option}" for i, option in enumerate(options, start=1)]
    print_lines(lines)


class EndOfInput(Exception):
    pass


def get_player_input(prompt="Enter your move (e.g. C4): "):
    try:
        return input(fit(prompt)).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        raise EndOfInput()


def pause(prompt="\nPress Enter to continue... "):
    if not sys.stdin.isatty():
        return
    try:
        get_player_input(prompt)
    except EndOfInput:
        pass


def display_game_status(player, game_state):
    parts = []
    if game_state.get("turn") is not None:
        parts.append(f"Turn {game_state['turn']}")
    parts.append(f"Cash: ${player.get('cash', 0)}")
    if game_state.get("player_ships_left") is not None:
        parts.append(f"Your ships: {game_state['player_ships_left']}")
    if game_state.get("computer_ships_left") is not None:
        parts.append(f"Enemy ships: {game_state['computer_ships_left']}")
    if game_state.get("extra_shots"):
        parts.append(f"Extra strike: {game_state['extra_shots']}")
    if game_state.get("radar_charges"):
        parts.append(f"Radar: {game_state['radar_charges']}")

    print(fit("|".join(parts)))
    print("-" * SCREEN_WIDTH)


def display_victory(turns=None):
    lines = [center("*** VICTORY ***"),
             center("You sank the entire enemy fleet!")]
    if turns is not None:
        lines += [center(f"Turns played: {turns}")]
    print_lines(lines)


def display_defeat(turns=None):
    lines = [center("*** DEFEAT ***"),
             center("The computer sank your fleet.")]
    if turns is not None:
        lines += [center(f"Turns played: {turns}")]
    print_lines(lines)