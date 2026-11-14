# Shipsweeper: Tactical Command Edition

## 1. Game Description

Tactical Command Edition is a single-player, turn-based naval strategy and logic puzzle game inspired by Battleship. Players must locate and destroy the enemy fleet using attacks, numerical clues, and tactical power-ups. 

Instead of relying on blind guessing, the game functions as a logic puzzle: a miss reveals numerical clues about the surrounding area, allowing the player to use spatial reasoning to map out the computer's hidden layout.

## 2. Game Features

- 10 x 10 coordinate grid
- Hidden ship placement
- Hit and miss detection
- Minesweeper-style numerical clues based on neighbouring ship segments
- Dynamic clue refreshing (clues decrease when ships sink)
- Cash and tactical shop system
- Radar and Extra Strike power-ups
- Anti-cheat, stateful Computer-controlled opponent

## 3. Development Environment & How to Run

- Language: Python 3.13
- Version Control: Git and GitHub
- Environment: Docker

Ensure you have Python 3.13 installed. Run the following command in your docker:

python main.py

## 4. Project Structure

- main.py: Main game controller
- board.py: Board management
- ship.py: Ship management
- combat.py: Combat system
- logic.py: Logic puzzle system (clue calculation and batch reveal)
- computer.py: Computer AI (placement and targeting)
- shop.py: Economy and shop system
- display.py: User interface (80x24 constraint)

## 5. Game Rules & Mechanics

### Overview
- The game is played on a 10x10 grid. Coordinates range from A-J (columns) and 1-10 (rows), e.g., C4.
- Type `Q` at any time during your turn to quit to the main menu. Type `Q` at the main menu to exit the game entirely.

### A. Fleet Placement
1. Both you and the computer secretly place 5 ships.
2. You may place ships by entering a coordinate. By default, ships are placed **horizontally (to the right)**. Add `V` to place **vertically (downwards)**.
   - Example: `C4` (Horizontal), `C4 V` (Vertical).
3. Ships cannot overlap or go out of bounds. Ships may touch each other.
4. **Fleet Composition:** Carrier (5), Battleship (4), Cruiser (3), Submarine (3), Destroyer (2).

### B. Shooting & Clues (Minesweeper Logic)
1. **Status Bar:** Displays current turn, cash, remaining ships, and purchased power-ups. Initial cash is $50.
2. **Cash Rewards:** 
   - Successful hit: +$20 per segment.
   - Sinking a ship: +$70 (including the hit bonus).
3. **Board Symbols:**
   - `S`: Your ship parts
   - `.`: unknown water
   - `X`: Hit
   - `#`: Sunk ship segment
   - `o`: Miss (no clue)
   - `0-8`: Number of unsunk ship parts touching that square
4. **Clue Generation:** 
   - **MISS:** Reveals a number for the 3x3 area surrounding the missed tile. The number indicates how many unsunk ship segments are in those 8 adjacent squares.
   - **HIT:** Marked as `X`. No neighbouring clues are revealed.
5. **Dynamic Clue Refresh:** When a ship sinks, all relevant numerical clues on the board automatically decrease to reflect the current afloat fleet.

### C. Tactical Shop & Power-ups
1. Type `SHOP` during your turn to buy power-ups. You can only open the shop between turns.
2. **Radar ($40):** 
   - Reveals numerical clues for a 3x3 area around a chosen center coordinate.
   - Results are immediately written to your enemy board.
   - Radar does NOT overwrite already-revealed tiles or ships.
   - Type `RADAR` during your turn to use it. You can use it in the same turn you buy it.
3. **Extra Strike ($50):** 
   - Allows you to take an extra shot on your **NEXT** turn.
   - You can only use **one** Extra Strike per turn. Multiple purchases will accumulate in your inventory.

## 6. Team Contributions

- **Member 1 (Peng Nga Huen):** Game architecture, board management (`board.py`), and system integration (`main.py`).
- **Member 2 (Guan Wingshan):** Ship mechanics (`ship.py`) and combat resolution (`combat.py`).
- **Member 3 (Lin Yuqing):** Logic puzzle system (`logic.py`), Computer AI (`computer.py`), and UI debugging.
- **Member 4 (Laith AlNahhas):** Terminal UI (`display.py`), Economy & Shop system (`shop.py`).

