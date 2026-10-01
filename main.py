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
        
    def draw_board(self):
        """Draws the entire board: highlight, numbers, and grid lines."""
        self.canvas.delete("all")

        # 1. Highlight the selected cell
        sr, sc = self.selected
        self.canvas.create_rectangle(
            sc * self.cell_size,
            sr * self.cell_size,
            (sc + 1) * self.cell_size,
            (sr + 1) * self.cell_size,
            fill="#D0E8FF",
            width=0,
        )

        # 2. Draw all numbers
        for row in range(9):
            for col in range(9):
                val = self.current[row][col]
                if val != 0:
                    x = col * self.cell_size + self.cell_size // 2
                    y = row * self.cell_size + self.cell_size // 2

                    # Original clues = black bold, player entries = blue
                    if self.original[row][col] != 0:
                        color = "black"
                        font = ("Arial", 18, "bold")
                    else:
                        color = "#2563EB"
                        font = ("Arial", 18)

                    self.canvas.create_text(x, y, text=str(val), font=font, fill=color)

        # 3. Draw grid lines
        for i in range(10):
            pos = i * self.cell_size

            if i % 3 == 0:
                color = "#1F2937"
                width = 3
            else:
                color = "#D1D5DB"
                width = 1

            # Vertical line
            self.canvas.create_line(pos, 0, pos, self.board_size, fill=color, width=width)
            # Horizontal line
            self.canvas.create_line(0, pos, self.board_size, pos, fill=color, width=width)
        def on_click(self, event):
            """Player clicked on the board — select that cell."""
        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if 0 <= row < 9 and 0 <= col < 9:
            self.selected = (row, col)
            self.draw_board()

    def move(self, dr, dc):
        """Arrow key pressed — move the selection cursor."""
        r = max(0, min(8, self.selected[0] + dr))
        c = max(0, min(8, self.selected[1] + dc))
        self.selected = (r, c)
        self.draw_board()

    def on_key(self, event):
        """Player pressed a key — type a number or erase."""
        row, col = self.selected

        # Don't allow editing original clues
        if self.original[row][col] != 0:
            self.status.config(text="That cell is a starting clue — it's locked!")
            return

        # Number 1-9 typed
        if event.char in "123456789":
            self.current[row][col] = int(event.char)
            self.status.config(text=f"Placed {event.char} at row {row+1}, col {col+1}.")
            self.draw_board()

        # Erase key pressed
        elif event.keysym in ("BackSpace", "Delete") or event.char == "0":
            self.current[row][col] = 0
            self.status.config(text=f"Cleared row {row+1}, col {col+1}.")
            self.draw_board()
            
            
        
