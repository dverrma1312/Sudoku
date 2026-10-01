import random
import tkinter as tk
from tkinter import messagebox


def is_valid(board, row, col, num):
    """Can we place 'num' at board[row][col] without breaking Sudoku rules?"""

    # Rule 1: num must not already exist in this row
    for c in range(9):
        if board[row][c] == num:
            return False

    # Rule 2: num must not already exist in this column
    for r in range(9):
        if board[r][col] == num:
            return False

    # Rule 3: num must not already exist in the 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if board[r][c] == num:
                return False

    return True

def solve(board):
    """Solve the board using backtracking. Returns True if solved, False if stuck."""

    # Scan every cell to find an empty one
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:

                # Try placing numbers 1 through 9
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num

                        # Recurse: try to solve the rest of the board
                        if solve(board):
                            return True

                        # Dead end — undo this move and try next number
                        board[row][col] = 0

                # None of 1-9 worked here, so backtrack
                return False

    # No empty cells left — board is completely solved!
    return True

def generate_full_board():
    """Create a complete, valid 9x9 board filled with random numbers."""
    board = [[0] * 9 for _ in range(9)]

    def fill(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)

                    for num in nums:
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            if fill(board):
                                return True
                            board[row][col] = 0

                    return False
        return True

    fill(board)
    return board


def generate_puzzle(difficulty):
    """Generate a puzzle with a unique solution. Returns (puzzle, solution)."""

    # 1. Build a fully solved board
    solution = generate_full_board()

    # 2. Copy it and start removing numbers
    puzzle = [row[:] for row in solution]

    # How many cells to remove based on difficulty
    remove_count = {"Easy": 35, "Medium": 45, "Hard": 52}
    to_remove = remove_count.get(difficulty, 45)

    # 3. Pick random cells and blank them out
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)

    for r, c in cells[:to_remove]:
        puzzle[r][c] = 0

    return puzzle, solution

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.root.resizable(False, False)

        # Each cell is 55x55 pixels, 9 cells = 495px total
        self.cell_size = 55
        self.board_size = self.cell_size * 9

        # The three boards we track
        self.current = [[0] * 9 for _ in range(9)]   # What player sees now
        self.original = [[0] * 9 for _ in range(9)]   # Starting clues (locked)
        self.solution = [[0] * 9 for _ in range(9)]   # The correct answer

        # Which cell is currently selected
        self.selected = (0, 0)

        # Build the UI
        self.create_widgets()

        # Start first game
        self.new_game()

    def create_widgets(self):
        # --- Top bar with buttons ---
        top = tk.Frame(self.root, padx=10, pady=10)
        top.pack()

        tk.Label(top, text="Difficulty:").pack(side=tk.LEFT, padx=(0, 5))

        self.diff_var = tk.StringVar(value="Medium")
        tk.OptionMenu(top, self.diff_var, "Easy", "Medium", "Hard").pack(
            side=tk.LEFT, padx=5
        )

        tk.Button(top, text="New Game", command=self.new_game).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(top, text="Check", command=self.check).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(top, text="Restart", command=self.restart).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(top, text="Solve", command=self.solve_it).pack(
            side=tk.LEFT, padx=5
        )

        # --- The game board canvas ---
        self.canvas = tk.Canvas(
            self.root,
            width=self.board_size,
            height=self.board_size,
            bg="white",
            cursor="hand2",
        )
        self.canvas.pack(padx=15, pady=5)
        self.canvas.bind("<Button-1>", self.on_click)

        # --- Keyboard bindings ---
        self.root.bind("<Key>", self.on_key)
        self.root.bind("<Up>", lambda e: self.move(-1, 0))
        self.root.bind("<Down>", lambda e: self.move(1, 0))
        self.root.bind("<Left>", lambda e: self.move(0, -1))
        self.root.bind("<Right>", lambda e: self.move(0, 1))

        # --- Bottom status message ---
        self.status = tk.Label(
            self.root,
            text="Click a cell and type 1-9 to play!",
            font=("Arial", 11),
            pady=10,
        )
        self.status.pack()