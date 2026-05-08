"""Constants and settings for the Tic-Tac-Toe game."""

# Board dimensions
BOARD_SIZE = 3

# Empty cell marker
EMPTY_CELL: str = " "

# Valid player markers
PLAYER_MARKERS = ("X", "O")

# Win combination lines (rows, columns, diagonals)
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
