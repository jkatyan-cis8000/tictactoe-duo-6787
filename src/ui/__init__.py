"""UI layer - CLI display and user input."""

from src.types import Board
from src.service import is_board_full


def display_board(board: Board) -> None:
    """Display the current board state."""
    print()
    print("  0   1   2")
    for i, row in enumerate(board):
        cells = [cell if cell is not None else " " for cell in row]
        print(f"{i} {cells[0]} | {cells[1]} | {cells[2]}")
        if i < 2:
            print("  ---+---+---")
    print()


def get_player_input() -> str | None:
    """Get player input. Returns None to quit."""
    try:
        user_input = input("Enter position (row,col) or 'q' to quit: ").strip()
        if user_input.lower() == "q":
            return None
        return user_input
    except (EOFError, KeyboardInterrupt):
        return None
