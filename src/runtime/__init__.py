"""Runtime layer - main entry point and orchestration."""

from src.types import Player, Position, GameState
from src.service import create_board, apply_move, is_valid_move, get_game_state
from src.ui import display_board, get_player_input


def main() -> None:
    """Run the Tic-Tac-Toe game loop."""
    board = create_board()
    current_player = Player.X
    
    print("Welcome to Tic-Tac-Toe!")
    print("Enter positions as 'row,col' (0-indexed, e.g., '0,0' is top-left)")
    print()
    
    while True:
        display_board(board)
        print(f"Player {current_player}'s turn")
        
        raw_input = get_player_input()
        if raw_input is None:
            print("Goodbye!")
            break
        
        try:
            row, col = parse_position(raw_input)
            pos = Position((row, col))
            
            if not is_valid_move(board, pos):
                print("Invalid move! Cell is taken or out of bounds.")
                continue
            
            apply_move(board, pos, current_player)
            state = get_game_state(board)
            
            if state == GameState.WON:
                display_board(board)
                print(f"Player {current_player} wins!")
                break
            
            if state == GameState.DRAW:
                display_board(board)
                print("It's a draw!")
                break
            
            current_player = current_player.opponent()
            
        except ValueError:
            print("Invalid input! Enter as 'row,col' (e.g., '1,2')")
            continue


def parse_position(input_str: str) -> tuple[int, int]:
    """Parse a position string like '0,1' into (row, col) tuple."""
    parts = input_str.strip().split(",")
    if len(parts) != 2:
        raise ValueError("Expected format: row,col")
    return int(parts[0].strip()), int(parts[1].strip())
