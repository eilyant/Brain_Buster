# game.py
import time
import sys
import os
from grid import Grid # type: ignore
def get_grid_size():
    """Prompt the user to enter a valid grid size (2, 4, or 6)."""
    while True:
        size = input("Enter grid size (2, 4, or 6): ")
        if size in {"2", "4", "6"}:
            return int(size)
        print("Invalid grid size. Please enter 2, 4, or 6.")
def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["2", "4", "6"]:
        print("Usage: python3 game.py <grid size (2, 4, or 6)>")
        sys.exit(1)

    grid_size = int(sys.argv[1])
    game_grid = Grid(grid_size)

    while True:
        os.system("clear")
        print("----------------")
        print("| Brain Buster  |")
        print("----------------")
        game_grid.display()
        print("\nMenu:")
        print("1. Reveal a pair of cells")
        print("2. Reveal a single cell")
        print("3. Reveal all cells (end game)")
        print("4. Start a new game")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")
        if choice not in {'1', '2', '3', '4', '5'}:
            print("Invalid choice. Please try again.")
            time.sleep(1.5)
            continue  # Ask for input again without breaking the loop

        if choice == '1':
            reveal_pair(game_grid)
        elif choice == '2':
            reveal_single_cell(game_grid)
        elif choice == '3':
            game_grid.reveal_all()
            print("Game Over")
            break
        elif choice == '4':
            # Ask for a new grid size and start a new game
            grid_size = get_grid_size()
            game_grid = Grid(grid_size)
            print("\nStarting a new game...")
            continue  # Restart the loop with the new game
        elif choice == '5':
            print("Goodbye!")
            break

        if game_grid.is_game_won():
            os.system("clear")
            print("----------------")
            print("| Brain Buster  |")
            print("----------------")
            game_grid.display()  # Keep the winning grid on display
            score = game_grid.calculate_score()
            if game_grid.option_two_reveal == game_grid.size ** 2:
                score = 0
            elif score == 0:
                print("You completed the game without making any guesses. Score: 0")
            else:
                print(f"Congratulations! You found all pairs. Your score is: {score}")
            # Prompt to start a new game or exit after winning
            play_again = input("Would you like to start a new game? (y/n): ").strip().lower()
            if play_again == 'y':
                grid_size = get_grid_size()
                game_grid = Grid(grid_size)  # Reset the grid for a new game
            else:
                print("Thank you for playing! Goodbye!")
                break

def reveal_pair(grid):
    """Reveal a pair of cells specified by the user."""
    while True:
        try:
            # Prompt for the first cell and validate it
            while True:
                cell1 = input("Enter the first cell (e.g., A0): ")
                try:
                    row1, col1 = grid._parse_cell(cell1)  # Validate first cell
                    break  # Exit the loop if the cell is valid
                except ValueError as e:
                    print(e)
                    time.sleep(1)  # Optional: Pause for 1 second to let the user read the error message

            # Prompt for the second cell and validate it
            while True:
                cell2 = input("Enter the second cell (e.g., B1): ")
                if cell1 == cell2:
                    print("You must select two different cells.")
                    continue  # Prompt for a different second cell
                try:
                    row2, col2 = grid._parse_cell(cell2)  # Validate second cell
                    break  # Exit the loop if the cell is valid
                except ValueError as e:
                    print(e)
                    time.sleep(1)  # Optional: Pause for 1 second to let the user read the error message

            # Attempt to reveal the pair, checking for a match
            if not grid.reveal_pair(cell1, cell2):
                print("No match. Try again.")
            else:
                print("It's a match!")
            break  # Exit the outer loop once both cells are valid and processed
        except ValueError as e:
            print(e)
            time.sleep(1)  # Optional pause, although this may be redundant with the above loops

def reveal_single_cell(grid):
    """Reveal a single cell specified by the user."""
    while True:
        try:
            cell = input("Enter the cell (e.g., A0): ")
            grid.reveal_single(cell)
            break  # Only exit the loop if the cell entry was valid
        except ValueError as e:
            print(e)
            time.sleep(1)  # Optional: Pause for 1 second to allow the user to read the error message

if __name__ == "__main__":
    main()