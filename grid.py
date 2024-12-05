import random
import time
import os

class Grid:
    def __init__(self, size):
        self.size = size
        self.grid = [['X' for _ in range(size)] for _ in range(size)]
        self.revealed_grid = self._generate_pairs()
        self.guesses = 0
        self.matches = 0
        self.single_reveal_count = 0  # Track the number of single cell reveals
        self.option_two_reveal = 0
        self.matched_cells = set()  # Track permanently matched cells
    def _generate_pairs(self):
         # Create pairs and shuffle them randomly to distribute across the grid
        pairs = list(range(self.size * self.size // 2)) * 2  # Create pairs (e.g., 0,0,1,1,...)
        random.shuffle(pairs)  # Shuffle pairs
        # Arrange shuffled pairs into a grid structure
        return [pairs[i * self.size:(i + 1) * self.size] for i in range(self.size)]

    def _parse_cell(self, cell):
        # Convert to uppercase and check format
        cell = cell.upper()
        # Check if the input format is valid
        if len(cell) < 2 or not cell[0].isalpha() or not cell[1:].isdigit():
            raise ValueError("Input error: invalid cell format. Please use the format letter-number (e.g., A0).")

        # Convert letter to column index and the rest to row index
        col = ord(cell[0]) - ord('A')
        row = int(cell[1:])

        # Prepare error messages for out-of-range checks
        errors = []
        # Check if column is out of range based on grid size
        if col < 0 or col >= self.size:
            errors.append(f"column '{cell[0]}' is out of range for this grid")
        
        # Check if row is out of range based on grid size
        if row < 0 or row >= self.size:
            errors.append(f"row '{row}' is out of range for this grid")

        # If there are any errors, raise a combined error message
        if errors:
            raise ValueError("Input error: " + " and ".join(errors) + ". Please try again.")

        return row, col



    def display(self):
        # Print column headers with brackets and consistent spacing
        header = "   " + "  ".join(f"[{chr(65 + i)}]" for i in range(self.size))
        print(header)
    
        # Print each row with row headers in brackets and consistent spacing for cells
        for row in range(self.size):
            row_content = "    ".join(f"{self.grid[row][col]}" for col in range(self.size))
            print(f"[{row}] {row_content}")


    def reveal_pair(self, cell1, cell2):
        # Parse both cells
        row1, col1 = self._parse_cell(cell1)
        row2, col2 = self._parse_cell(cell2)

        # Check for duplicate cell selection
        if (row1, col1) == (row2, col2):
            raise ValueError("You must select two different cells.")

        # Check if the first cell is permanently matched
        if (row1, col1) in self.matched_cells:
            raise ValueError(f"The first cell {cell1} has already been permanently matched.")

        # Check if the second cell is permanently matched
        if (row2, col2) in self.matched_cells:
            raise ValueError(f"The second cell {cell2} has already been permanently matched.")

        # Reveal both cells temporarily
        self.guesses += 1
        temp1 = self.grid[row1][col1]
        temp2 = self.grid[row2][col2]
        self.grid[row1][col1] = self.revealed_grid[row1][col1]
        self.grid[row2][col2] = self.revealed_grid[row2][col2]
        self.display()

        # Check for a match
        if self.grid[row1][col1] == self.grid[row2][col2]:
            print("It's a match!")
            self.matches += 1
            # Mark these cells as permanently matched
            self.matched_cells.add((row1, col1))
            self.matched_cells.add((row2, col2))
            return True
        else:
            print("No match!")
            time.sleep(2)  # Pause for the user to see the result
            # Reset both cells to their previous state
            self.grid[row1][col1] = temp1
            self.grid[row2][col2] = temp2
            self.display()
            return False

    def reveal_single(self, cell):
        row, col = self._parse_cell(cell)

        # Check if the cell is already permanently matched
        if self.grid[row][col] == self.revealed_grid[row][col] and \
        all(self.grid[row][col] == self.revealed_grid[r][c] for r in range(self.size) for c in range(self.size)):
            raise ValueError(f"The cell {cell} has already been permanently matched.")

        # Increment single reveal count each time this method is called
        self.single_reveal_count += 1
        self.option_two_reveal += 1
        self.guesses += 2

        # Reveal the cell permanently until reset in Option 1
        self.grid[row][col] = self.revealed_grid[row][col]
        self.display()

    def reveal_all(self):
        # Reveal all cells by setting grid to revealed_grid
        for row in range(self.size):
            for col in range(self.size):
                self.grid[row][col] = self.revealed_grid[row][col]
        self.display()  # Display the fully revealed grid

    def is_game_won(self):
        # Check if the number of matches equals half the total cells (all pairs matched)
        for i in self.grid:
            for j in i:
                if j == 'X':
                    return False

        return True


    def calculate_score(self):
        min_guesses = self.size * self.size // 2  # Minimum guesses to find all pairs
        if self.guesses == 0 or self.single_reveal_count == self.size * self.size:
            # Player used single reveal to reveal all cells without making valid guesses
            print("You cheated – Loser! Your score is 0!")
            return 0
        return (min_guesses / self.guesses) * 100