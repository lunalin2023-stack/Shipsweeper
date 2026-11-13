# ==========================================
# ship.py - Ship Management
# ==========================================

from typing import Callable, List, Optional, Sequence, Tuple

BOARD_SIZE = 10
HORIZONTAL = "H"
VERTICAL = "V"

SHIP_TYPES = {
    "Carrier": 5,
    "Battleship": 4,
    "Cruiser": 3,
    "Submarine": 3,
    "Destroyer": 2,
}

FLEET = tuple(SHIP_TYPES.items())

_STEPS = {HORIZONTAL: (0, 1), VERTICAL: (1, 0)}


class PlacementError(Exception):
    pass


class Ship:
    def __init__(
        self,
        name: str,
        length: int,
        ship_id: int = 0,
        positions: Optional[Sequence[Tuple[int, int]]] = None,
    ) -> None:
        if not isinstance(length, int) or length < 1:
            raise PlacementError("A ship must be at least 1 square long.")
        self.name = name
        self.length = length
        self.ship_id = ship_id
        self._positions: List[Tuple[int, int]] = []
        self._position_set = set()
        self._hits = set()
        if positions is not None:
            self.set_positions(positions)

    def set_positions(self, positions: Sequence[Tuple[int, int]]) -> None:
        cells = list(positions)
        if len(cells) != self.length:
            raise PlacementError(
                "The %s needs %d squares, got %d." % (self.name, self.length, len(cells))
            )
        if len(set(cells)) != len(cells):
            raise PlacementError("A ship cannot occupy the same square twice.")
        self._positions = cells
        self._position_set = set(cells)
        self._hits.clear()

    @property
    def positions(self) -> List[Tuple[int, int]]:
        return list(self._positions)

    @property
    def hits(self) -> set:
        return set(self._hits)

    @property
    def damage(self) -> int:
        return len(self._hits)

    @property
    def health(self) -> int:
        return self.length - len(self._hits)

    def occupies(self, row: int, col: int) -> bool:
        return (row, col) in self._position_set

    def take_hit(self, row: int, col: int) -> bool:
        if (row, col) not in self._position_set:
            return False
        if (row, col) in self._hits:
            return False
        self._hits.add((row, col))
        return True

    def is_sunk(self) -> bool:
        return len(self._hits) >= self.length

    def status(self) -> str:
        return "%s %d/%d" % (self.name, self.health, self.length)

    def __repr__(self) -> str:
        return "<Ship %s %d/%d at %s>" % (
            self.name,
            self.health,
            self.length,
            self._positions,
        )


def create_ship(name: str, ship_id: int = 0) -> Ship:
    if name not in SHIP_TYPES:
        raise PlacementError(
            "Unknown ship type %r. Choose one of: %s."
            % (name, ", ".join(SHIP_TYPES))
        )
    return Ship(name, SHIP_TYPES[name], ship_id=ship_id)


def in_bounds(row: int, col: int, size: int = BOARD_SIZE) -> bool:
    return (
        isinstance(row, int)
        and isinstance(col, int)
        and 0 <= row < size
        and 0 <= col < size
    )


def parse_coordinate(text: str, size: int = BOARD_SIZE) -> Tuple[int, int]:
    if not isinstance(text, str):
        raise ValueError("Enter a square such as C4.")
    cleaned = text.strip().upper().replace(" ", "")
    if len(cleaned) < 2:
        raise ValueError("Enter a square such as C4.")
    letter, digits = cleaned[0], cleaned[1:]
    last_letter = chr(ord("A") + size - 1)
    if not ("A" <= letter <= last_letter):
        raise ValueError("The column must be a letter from A to %s." % last_letter)
    if not digits.isdigit():
        raise ValueError("The row must be a number from 1 to %d." % size)
    number = int(digits)
    if not 1 <= number <= size:
        raise ValueError("The row must be a number from 1 to %d." % size)
    return number - 1, ord(letter) - ord("A")


def format_coordinate(row: int, col: int) -> str:
    return "%s%d" % (chr(ord("A") + col), row + 1)


def normalise_orientation(orientation: str) -> str:
    if not isinstance(orientation, str):
        raise PlacementError("Direction must be H (horizontal) or V (vertical).")
    key = orientation.strip().upper()
    if key in ("H", "HORIZONTAL", "ROW"):
        return HORIZONTAL
    if key in ("V", "VERTICAL", "COLUMN", "COL"):
        return VERTICAL
    raise PlacementError("Direction must be H (horizontal) or V (vertical).")


def ship_cells(
    row: int,
    col: int,
    length: int,
    orientation: str,
    size: int = BOARD_SIZE,
) -> List[Tuple[int, int]]:
    if not isinstance(length, int) or length < 1:
        raise PlacementError("A ship must be at least 1 square long.")
    direction = normalise_orientation(orientation)
    step_row, step_col = _STEPS[direction]
    cells = [(row + i * step_row, col + i * step_col) for i in range(length)]
    for cell_row, cell_col in cells:
        if not in_bounds(cell_row, cell_col, size):
            raise PlacementError("That placement runs off the board.")
    return cells


def can_place_ship(
    ships: Sequence[Ship],
    row: int,
    col: int,
    length: int,
    orientation: str,
    size: int = BOARD_SIZE,
) -> bool:
    try:
        cells = ship_cells(row, col, length, orientation, size)
    except PlacementError:
        return False
    occupied = set()
    for ship in ships:
        occupied.update(ship.positions)
    return not any(cell in occupied for cell in cells)


def place_ship(
    ships: List[Ship],
    name: str,
    length: int,
    row: int,
    col: int,
    orientation: str = HORIZONTAL,
    ship_id: Optional[int] = None,
    size: int = BOARD_SIZE,
) -> Ship:
    cells = ship_cells(row, col, length, orientation, size)
    for ship in ships:
        for cell_row, cell_col in cells:
            if ship.occupies(cell_row, cell_col):
                raise PlacementError(
                    "%s is already occupied by the %s."
                    % (format_coordinate(cell_row, cell_col), ship.name)
                )
    if ship_id is None:
        ship_id = len(ships) + 1
    new_ship = Ship(name, length, ship_id=ship_id, positions=cells)
    ships.append(new_ship)
    return new_ship


def stamp_on_board(board: List[List], ship: Ship, marker=None) -> None:
    value = ship.ship_id if marker is None else marker
    for row, col in ship.positions:
        board[row][col] = value


def all_sunk(ships: Sequence[Ship]) -> bool:
    return all(ship.is_sunk() for ship in ships)


def ships_afloat(ships: Sequence[Ship]) -> List[Ship]:
    return [ship for ship in ships if not ship.is_sunk()]


def place_fleet(
    ships: List[Ship],
    fleet: Sequence[Tuple[str, int]] = FLEET,
    size: int = BOARD_SIZE,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
    show_fn: Optional[Callable[[Sequence[Ship], str], None]] = None,
) -> List[Ship]:
    ships.clear()
    index = 0
    total = len(fleet)
    message = ""

    while index < total:
        name, length = fleet[index]
        if show_fn is not None:
            show_fn(ships, message)
            message = ""

        try:
            raw = input_fn(
                "Place %s (%d squares) [Enter C4 for Horizontal, or C4 V for Vertical]: "
                % (name, length)
            )
        except (EOFError, KeyboardInterrupt):
            raise PlacementError("Placement cancelled by the player.")

        command = "" if raw is None else str(raw).strip()
        lowered = command.lower()

        if lowered in ("q", "quit"):
            raise PlacementError("Placement cancelled by the player.")
        if lowered in ("r", "reset"):
            ships.clear()
            index = 0
            message = "Fleet cleared - starting the placement again."
            continue

        parts = command.split()
        if not parts:
            message = "! Enter a square such as C4, optionally followed by H or V."
            continue

        if len(parts) == 1 and len(parts[0]) > 2 and parts[0][-1].upper() in ("H", "V"):
            parts = [parts[0][:-1], parts[0][-1]]

        orientation = parts[1] if len(parts) > 1 else HORIZONTAL

        try:
            row, col = parse_coordinate(parts[0], size)
            ship = place_ship(
                ships, name, length, row, col, orientation,
                ship_id=index + 1, size=size,
            )
        except (ValueError, PlacementError) as error:
            message = f"! {error}"
            continue

        cells = ship.positions
        message = f"{name} placed on {format_coordinate(*cells[0])}-{format_coordinate(*cells[-1])}."
        index += 1

    return ships