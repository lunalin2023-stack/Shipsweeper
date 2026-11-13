# ==========================================
# shop.py - Economy and Shop System
# ==========================================

STARTING_CASH = 50

SHOP_ITEMS = {
    "radar": {
        "price": 40,
        "description": "Radar scan: reveals number clues in a 3x3 area",
    },
    "extra strike": {
        "price": 50,
        "description": "Extra strike: take one more shot next turn",
    },
}


def new_player_wallet(starting_cash=STARTING_CASH):
    return {"cash": starting_cash}


def get_cash(player):
    return player.get("cash", 0)


def add_cash(player, amount):
    if amount < 0:
        raise ValueError("amount must not be negative")
    player["cash"] = get_cash(player) + amount
    return player["cash"]


def reward_for_attack(player, hit, sunk):
    from combat import HIT_REWARD, SINK_BONUS

    earned = 0
    if hit:
        earned += HIT_REWARD
    if sunk:
        earned += SINK_BONUS
    if earned > 0:
        add_cash(player, earned)
        return earned, f"You earned ${earned}. Cash: ${get_cash(player)}"
    return 0, ""


def get_shop_items():
    return {name: info["price"] for name, info in SHOP_ITEMS.items()}


def get_shop_menu_lines():
    lines = []
    for number, (name, info) in enumerate(SHOP_ITEMS.items(), start=1):
        line = f"{number}. {name.title():<14} ${info['price']:<4} {info['description']}"
        lines.append(line[:80])
    return lines


def find_item(choice):
    choice = str(choice).strip().lower()
    names = list(SHOP_ITEMS.keys())
    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(names):
            return names[index]
        return None
    if choice in SHOP_ITEMS:
        return choice
    return None


def can_afford(player, item_name):
    if item_name not in SHOP_ITEMS:
        return False
    return get_cash(player) >= SHOP_ITEMS[item_name]["price"]


def purchase_item(player, item_name):
    item = find_item(item_name)
    if item is None:
        return False, f"'{item_name}' is not sold here."

    price = SHOP_ITEMS[item]["price"]
    if not can_afford(player, item):
        short = price - get_cash(player)
        return False, f"Not enough cash for {item}. You need ${short} more."

    player["cash"] = get_cash(player) - price
    return True, f"Bought {item}."  # ⭐ 不再显示 Cash left


def apply_power_up(item_name, game_state):
    item = find_item(item_name)
    if item == "extra strike":
        game_state["extra_shots"] = game_state.get("extra_shots", 0) + 1
        return "Extra strike ready."
    if item == "radar":
        game_state["radar_charges"] = game_state.get("radar_charges", 0) + 1
        return "Radar ready."
    return f"Unknown power-up: {item_name}"


def use_extra_shot(game_state):
    if game_state.get("extra_shots", 0) > 0:
        game_state["extra_shots"] -= 1
        return True
    return False


def use_radar_charge(game_state):
    if game_state.get("radar_charges", 0) > 0:
        game_state["radar_charges"] -= 1
        return True
    return False


def radar_area(row, col, size=10):
    squares = []
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            if 0 <= r < size and 0 <= c < size:
                squares.append((r, c))
    return squares