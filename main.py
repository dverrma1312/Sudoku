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
