# Sudoku — Python Desktop Application

A complete Sudoku game built from scratch in Python using the `tkinter` GUI library.  
No external packages required — runs on any system with Python 3 installed.

```
python3 main.py
```

---

## How the Application Works

When the app starts, it generates a random Sudoku puzzle, draws it on screen, and waits for the player to interact. Here is the full flow from launch to gameplay:

```
App starts
  │
  ▼
__init__()                          Sets up window, boards, and variables
  │
  ├── create_widgets()              Builds the buttons, canvas, and status bar
  │
  └── new_game()                    Generates the first puzzle
        │
        └── generate_puzzle()       Creates a random puzzle + its solution
              │
              ├── generate_full_board()    Fills a blank 9x9 grid randomly
              │     │
              │     └── is_valid()         Checks Sudoku rules at every step
              │
              └── Removes random cells     Pokes holes based on difficulty
        │
        └── draw_board()            Paints the puzzle on the canvas
```

After this, the app sits idle and waits for the player to click cells, type numbers, or press buttons.

---

## File Structure

Everything lives in a single file:

```
main.py
├── is_valid()              Rule checker
├── solve()                 Backtracking solver
├── generate_full_board()   Random board generator
├── generate_puzzle()       Puzzle creator (calls generate_full_board)
├── class SudokuApp
│   ├── __init__()          App setup
│   ├── create_widgets()    UI layout (buttons, canvas, bindings)
│   ├── draw_board()        Renders the grid and numbers
│   ├── on_click()          Handles mouse clicks
│   ├── move()              Handles arrow key navigation
│   ├── on_key()            Handles number typing and erasing
│   ├── new_game()          Generates a fresh puzzle
│   ├── restart()           Resets to starting clues
│   ├── check()             Validates player's answers
│   └── solve_it()          Reveals the solution
└── Entry point             Creates the window and runs the app
```

---

## Function-by-Function Explanation

### 1. `is_valid(board, row, col, num)`

**Purpose:** The foundation of the entire app. Every other function calls this.

**What it does:** Checks whether placing a number at a specific cell would break any of the three Sudoku rules:
- The number must not already exist in the same **row**.
- The number must not already exist in the same **column**.
- The number must not already exist in the same **3×3 box**.

**How the 3×3 box check works:**
```
If the cell is at row=5, col=7:

  box_row = (5 // 3) * 3 = 3      ← Top edge of the box
  box_col = (7 // 3) * 3 = 6      ← Left edge of the box

  The box covers rows 3-5, cols 6-8:
  ┌─────────┐
  │ (3,6) (3,7) (3,8) │
  │ (4,6) (4,7) (4,8) │
  │ (5,6) (5,7) (5,8) │  ← Our cell is here
  └─────────┘
```

**Returns:** `True` if the move is legal, `False` if it breaks a rule.

---

### 2. `solve(board)`

**Purpose:** A pure, deterministic solver that can solve any valid Sudoku puzzle.

**Algorithm:** Backtracking (depth-first search with recursion).

**How it works — step by step:**
1. Scan the board left to right, top to bottom, looking for the first empty cell (`0`).
2. Try placing `1` in that cell. Is it valid? If yes, move to the next empty cell.
3. If a future cell gets stuck (no number 1–9 fits), come back and try `2` instead.
4. If all numbers 1–9 fail at a cell, undo and go back further (backtrack).
5. When no empty cells remain, the puzzle is solved.

```
Think of it like a maze:

  Try 1 → works → Try 1 → works → Try 1 → STUCK!
                                     Try 2 → STUCK!
                                     ...
                                     Try 9 → STUCK!
                            ← Backtrack
                   Try 2 → works → Try 1 → works → ... → SOLVED!
```

**Key detail:** This function tries numbers in order (1, 2, 3... 9) with NO randomness. Given the same puzzle, it always produces the same solution.

---

### 3. `generate_full_board()`

**Purpose:** Creates a completely filled, valid 9×9 Sudoku board with random numbers.

**How it works:** Uses the same backtracking approach as `solve()`, but with one critical difference — `random.shuffle(nums)` randomizes the order in which numbers are tried.

**Why randomness matters here:**
- Without shuffle: the function always produces the exact same board (1,2,3,4... pattern).
- With shuffle: every call produces a completely different, unique board.

**Why this is a separate function from `solve()`:**
- `solve()` is a **solver** — deterministic, predictable, no randomness.
- `generate_full_board()` is a **generator** — needs randomness to create variety.
- One function, one job. Mixing them would be confusing.

---

### 4. `generate_puzzle(difficulty)`

**Purpose:** Creates a playable puzzle from a solved board.

**Steps:**
1. Call `generate_full_board()` to get a random, fully solved board → this becomes the **solution**.
2. Make a copy of it → this copy becomes the **puzzle**.
3. Based on difficulty, remove a certain number of cells (set them to `0`):
   - **Easy:** remove 35 cells (46 clues remain)
   - **Medium:** remove 45 cells (36 clues remain)
   - **Hard:** remove 52 cells (29 clues remain)
4. Return both the puzzle and the solution.

**Why we return both:** The puzzle is what the player sees. The solution is stored internally so we can check the player's answers and power the "Solve" button.

---

### 5. `SudokuApp.__init__()`

**Purpose:** Runs once when the app starts. Sets up everything.

**What it initializes:**
- `self.current` — the board currently shown on screen (changes as player types).
- `self.original` — a frozen copy of the starting clues (never changes, used to lock cells).
- `self.solution` — the correct answer (never shown until player clicks "Solve").
- `self.selected` — which cell (row, col) is currently highlighted.

Then it calls `create_widgets()` to build the UI and `new_game()` to load the first puzzle.

---

### 6. `create_widgets()`

**Purpose:** Builds the visual layout of the window.

**Layout:**
```
┌──────────────────────────────────────────────────────┐
│  Difficulty: [Medium▼]  [New Game] [Check] [Restart] [Solve]  │
├──────────────────────────────────────────────────────┤
│                                                      │
│                  495 × 495 Canvas                    │
│              (9×9 grid drawn here)                   │
│                                                      │
├──────────────────────────────────────────────────────┤
│  "Click a cell and type 1-9 to play!"                │
└──────────────────────────────────────────────────────┘
```

**Bindings set up here:**
- Left mouse click on canvas → `on_click()`
- Any keyboard key → `on_key()`
- Arrow keys → `move()` with direction values like (-1, 0) for Up

---

### 7. `draw_board()`

**Purpose:** Paints the entire board on the canvas. Called every time something changes.

**What it draws (in order):**
1. A light blue rectangle behind the selected cell (highlight).
2. All numbers from `self.current`:
   - Numbers that exist in `self.original` → drawn in **black bold** (locked clues).
   - Numbers NOT in `self.original` → drawn in **blue** (player's entries).
3. Grid lines:
   - Thin gray lines between every cell.
   - Thick dark lines every 3 cells (3×3 box boundaries).

**Why it is called repeatedly:** The canvas does not update automatically. After any change (clicking a cell, typing a number, starting a new game), we must erase everything and repaint from scratch.

---

### 8. `on_click(event)` and `move(dr, dc)`

**Purpose:** Let the player navigate the board.

**`on_click`:** Converts mouse pixel coordinates to grid coordinates:
```
Click at pixel (162, 73):
  col = 162 // 55 = 2
  row = 73  // 55 = 1
  → Selected cell is (row=1, col=2)
```

**`move`:** Shifts the selection by a direction. Arrow Up calls `move(-1, 0)` (go up one row, stay in same column). Values are clamped between 0 and 8 so you can't go off the board.

---

### 9. `on_key(event)`

**Purpose:** Handles number typing and erasing.

**Logic:**
1. First checks if the selected cell is an original clue → if yes, ignore the keypress.
2. If the player typed `1`–`9` → store that number in `self.current[row][col]`.
3. If the player pressed Backspace/Delete/0 → set the cell back to `0` (blank).
4. Redraws the board after each change.

---

### 10. `new_game()`

**Purpose:** Generates a brand-new unique puzzle.

**Flow:**
1. Reads the difficulty from the dropdown.
2. Calls `generate_puzzle(difficulty)` → gets back a puzzle and solution.
3. Copies the puzzle into `self.current` and `self.original`.
4. Copies the solution into `self.solution`.
5. Redraws the board.

Every click of "New Game" produces a completely different puzzle because `generate_full_board()` uses `random.shuffle()`.

---

### 11. `restart()`

**Purpose:** Erases all player entries and resets the board to the starting clues.

**How:** Copies `self.original` back into `self.current`. The puzzle and solution stay the same — only the player's progress is wiped.

---

### 12. `check()`

**Purpose:** Tells the player if their answers are correct without revealing the solution.

**How:** Loops through all 81 cells and counts:
- **Empty cells** (still `0`) → tells the player how many remain.
- **Mistakes** (filled but does not match `self.solution`) → tells the player how many are wrong.
- **All filled and correct** → shows a victory popup.

---

### 13. `solve_it()`

**Purpose:** Reveals the complete solution on screen.

**How:** Copies `self.solution` into `self.current` and redraws.

---

## Controls

| Action | How |
|--------|-----|
| Select a cell | Click on it, or use Arrow Keys |
| Enter a number | Press `1` through `9` |
| Erase a number | Press `Backspace`, `Delete`, or `0` |
| New random puzzle | Click "New Game" |
| Check your answers | Click "Check" |
| Reset your progress | Click "Restart" |
| Reveal the answer | Click "Solve" |

---

## Technical Challenges Faced

1. **Indentation errors** — Python methods were accidentally nested inside other methods, making them invisible to the class. Fixed by ensuring every method starts at the same indentation level.

2. **Solver vs Generator responsibility** — Initially used one function for both solving and generating, which mixed deterministic logic with randomness. Separated into `solve()` (pure, sequential) and `generate_full_board()` (randomized).

3. **Shallow copy bug** — Using `puzzle = solution` made both variables point to the same list in memory. Modifying the puzzle also destroyed the solution. Fixed by using `[row[:] for row in solution]` to create independent copies.

4. **Slow startup on hard puzzles** — Backtracking solver explored thousands of paths on difficult boards, causing multi-second load times. Addressed by precomputing solutions or optimizing cell selection order.

5. **GUI window hidden behind editor** — On macOS, the Tkinter window opened behind VS Code, making it look like the app crashed. Fixed by bringing the window to front programmatically.
