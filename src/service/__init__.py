"""Service layer - game rules and business logic."""

from src.types import Board, Cell, Player, Position, GameState
from src.config import BOARD_SIZE, WIN_LINES


def create_board() -> Board:
    """Create a new empty 3x3 board."""
    return [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def is_valid_move(board: Board, pos: Position) -> bool:
    """Check if a move is valid (cell is empty and within bounds)."""
    row, col = pos
    if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
        return False
    return board[row][col] is None


def apply_move(board: Board, pos: Position, player: Player) -> None:
    """Apply a move to the board."""
    row, col = pos
    board[row][col] = player


def check_winner(board: Board) -> Player | None:
    """Check if there's a winner. Returns the winning player or None."""
    for line in WIN_LINES:
        cells = [board[row][col] for row, col in line]
        if cells[0] is not None and all(c == cells[0] for c in cells):
            return cells[0]
    return None


def is_board_full(board: Board) -> bool:
    """Check if the board is completely filled."""
    return all(cell is not None for row in board for cell in row)


def get_game_state(board: Board) -> GameState:
    """Determine the current game state."""
    winner = check_winner(board)
    if winner is not None:
        return GameState.WON
    if is_board_full(board):
        return GameState.DRAW
    return GameState.IN_PROGRESS
