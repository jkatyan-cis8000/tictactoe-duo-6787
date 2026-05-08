"""Pure type definitions for the Tic-Tac-Toe game."""

from enum import Enum
from typing import NewType

# Player type - X or O
class Player(str, Enum):
    X = "X"
    O = "O"

    def opponent(self) -> "Player":
        return Player.O if self == Player.X else Player.X


# Cell state - empty, X, or O
Cell = Player | None

# Board is a 3x3 grid of cells
Board = list[list[Cell]]

# Position on the board (row, col), 0-indexed
Position = NewType("Position", tuple[int, int])

# Game status
class GameState(str, Enum):
    IN_PROGRESS = "in_progress"
    WON = "won"
    DRAW = "draw"
