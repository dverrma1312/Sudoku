# 🧩 Sudoku (Python Desktop Application)

A clean, lightweight, single-file Sudoku application built in Python using native `tkinter`. It requires **zero external pip dependencies** and works out of the box on macOS, Windows, and Linux.

---

## 🚀 Quick Start

Run the application directly using Python 3:

```bash
python3 main.py
```

---

## ✨ Features

- **Built-in Puzzle Generator**: Creates fresh, solvable puzzles on demand.
- **3 Difficulty Levels**: Easy, Medium, and Hard.
- **Interactive 9×9 Board**: Clean canvas layout with thick 3×3 box gridlines.
- **Clue Protection**: Starting clues are locked in dark bold text so you can't accidentally overwrite them.
- **Visual Feedback**: The active square is highlighted in light blue, and player moves appear in bright blue.
- **Check Moves**: Validate your progress anytime without giving away unplaced numbers.
- **Instant Solver**: Reveals the full solution if you get stuck.
- **Keyboard & Mouse Navigation**: Click or use arrow keys (`↑`, `↓`, `←`, `→`) to move; press `1`–`9` to fill numbers, and `Backspace` / `Delete` to clear.

---

## ⌨️ Controls & Shortcuts

| Action | Control |
| :--- | :--- |
| **Select Cell** | Left Click on any square |
| **Move Cursor** | Arrow Keys (`↑`, `↓`, `←`, `→`) |
| **Enter Digit** | Keys `1` – `9` (Number row or NumPad) |
| **Clear Cell** | `Backspace`, `Delete`, or `0` |

---

## 📁 Project Structure

```
sudoku/
├── main.py             # Complete, self-contained Sudoku application
├── requirements.txt    # Standard library notice (no pip installs needed)
└── README.md           # Instructions & documentation
```
