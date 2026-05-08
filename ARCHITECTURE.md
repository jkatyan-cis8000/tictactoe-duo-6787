# ARCHITECTURE.md

Domain map and package structure for Tic-Tac-Toe game.

## Layer Model

```
src/
├── types/      — domain types (Player, Cell, Board, Position, GameState)
├── config/     — configuration constants (BOARD_SIZE, WIN_LINES, EMPTY_CELL)
├── utils/      — pure helper functions (no domain logic)
├── service/    — game rules and business logic
├── runtime/    — main entry point and orchestration
└── ui/         — CLI display and user input
```

## Dependency Graph

Dependencies flow **forward** (downward in the diagram above):

- `types` → no internal dependencies (leaf layer)
- `config` → `types`, `config`
- `utils` → `utils` (leaf layer, pure functions only)
- `service` → `types`, `config`, `repo`, `providers`, `service`
- `runtime` → `types`, `config`, `repo`, `service`, `providers`, `runtime`
- `ui` → `types`, `config`, `service`, `runtime`, `providers`, `ui`

**Importing rules:**
- Files may import from their own layer and any layer **above** them
- Cross-layer imports that don't follow this rule are violations
- Standard library modules (enum, typing, etc.) are allowed in all layers

## Module Interfaces

### `src/types/__init__.py`
Pure type definitions used throughout the system. Parse-don't-validate at boundaries.

```python
from enum import Enum

class Cell(Enum):
    X = "X"
    O = "O"
    EMPTY = " "

class Player(Enum):
    X = "X"
    O = "O"
    
    def opponent(self) -> Player:
        """Return the opposing player."""

class Board(list[list[Cell | None]]):
    """3x3 grid where None represents an empty cell."""

class Position(tuple[int, int]):
    """(row, col) coordinate pair for board placement."""

class GameState(Enum):
    IN_PROGRESS = "in_progress"
    WON = "won"
    DRAW = "draw"
```

### `src/config/__init__.py`
Configuration constants, no logic.

```python
BOARD_SIZE: int = 3
EMPTY_CELL: Cell = Cell.EMPTY
PLAYER_MARKERS: dict[Player, str] = {Player.X: "X", Player.O: "O"}

# Pre-computed winning lines as lists of (row, col) tuples
WIN_LINES: list[list[tuple[int, int]]] = [
    # Rows
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    # Columns
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    # Diagonals
    [(0, 0), (1, 1), (2, 2)],
    [(0, 2), (1, 1), (2, 0)],
]
```

### `src/utils/__init__.py`
Pure helper functions with no domain logic. Leaf layer.

```python
def clamp(value: int, min_val: int, max_val: int) -> int:
    """Clamp a value to be within [min_val, max_val]."""
```

### `src/service/__init__.py`
Game rules and business logic. Expects types from `types/` and configuration from `config/`.

```python
def create_board() -> Board:
    """Create a new empty 3x3 board."""

def is_valid_move(board: Board, pos: Position) -> bool:
    """Check if a move is valid (cell is empty and within bounds)."""

def apply_move(board: Board, pos: Position, player: Player) -> None:
    """Apply a move to the board. Mutates in place."""

def check_winner(board: Board) -> Player | None:
    """Check if there's a winner. Returns the winning player or None."""

def is_board_full(board: Board) -> bool:
    """Check if the board is completely filled."""

def get_game_state(board: Board) -> GameState:
    """Determine the current game state (IN_PROGRESS, WON, or DRAW)."""
```

### `src/ui/__init__.py`
CLI display and user input. Depends on types and service.

```python
def display_board(board: Board) -> None:
    """Display the current board state."""

def get_player_input() -> str | None:
    """Get player input. Returns None to quit."""
```

### `src/runtime/__init__.py`
Main entry point. Orchestrates game loop using service and UI layers.

```python
def main() -> None:
    """Run the Tic-Tac-Toe game loop."""

def parse_position(input_str: str) -> tuple[int, int]:
    """Parse a position string like '0,1' into (row, col) tuple."""
```

## Entry Points

- **Application entry point:** `src/runtime/__init__.py` → `main()`
- **Run game:** `python -m src.runtime`

## Testing

Tests live in `tests/` and are not lint-checked. Test modules mirror the source structure:

```
tests/
├── test_types.py
├── test_config.py
├── test_service.py
└── test_runtime.py
```

## Design Decisions

1. **Pre-computed WIN_LINES**: Win detection is O(1) by checking 8 pre-defined lines instead of computing dynamically.
2. **Parse-don't-validate**: Input parsing happens at boundaries; internal code trusts validated types.
3. **Stateless service layer**: Functions take Board as input, don't mutate global state.
4. **CLI-only UI**: Minimal interface focused on core gameplay flow.

## Future Extensibility

- `providers/` layer reserved for cross-cutting concerns (logging, metrics, DI container)
- `repo/` layer reserved for data persistence if needed (save/load games)
