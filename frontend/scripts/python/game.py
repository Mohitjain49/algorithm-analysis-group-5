"""
game.py — Tic-Tac-Toe game state and rules engine.

Board representation:
    A flat list of 9 elements, indices 0-8 (row-major order).
    Values: None (empty), 'X' (maximizer), 'O' (minimizer).

    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8
"""

from typing import Optional

WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
]


def new_board() -> list:
    """Return a fresh empty board."""
    return [None] * 9


def get_legal_moves(board: list) -> list[int]:
    """Return indices of all empty cells."""
    return [i for i, cell in enumerate(board) if cell is None]


def apply_move(board: list, index: int, player: str) -> list:
    """Return a new board with the move applied (non-mutating)."""
    if board[index] is not None:
        raise ValueError(f"Cell {index} is already occupied.")
    new = board[:]
    new[index] = player
    return new


def check_winner(board: list) -> Optional[str]:
    """
    Return 'X' or 'O' if that player has won, else None.
    Does NOT return draw — call is_draw() separately.
    """
    for a, b, c in WINNING_LINES:
        if board[a] is not None and board[a] == board[b] == board[c]:
            return board[a]
    return None


def is_draw(board: list) -> bool:
    """True if the board is full and has no winner."""
    return all(cell is not None for cell in board) and check_winner(board) is None


def is_terminal(board: list) -> bool:
    """True if the game is over (win or draw)."""
    return check_winner(board) is not None or is_draw(board)


def terminal_score(board: list) -> int:
    """
    Score for a terminal board state.
    +1  → X wins
    -1  → O wins
     0  → draw
    Raises ValueError on non-terminal boards.
    """
    winner = check_winner(board)
    if winner == 'X':
        return 1
    if winner == 'O':
        return -1
    if is_draw(board):
        return 0
    raise ValueError("Board is not in a terminal state.")


def board_to_dict(board: list) -> dict:
    """
    Serialize board for API responses.
    Returns a dict with:
      - cells: list of 9 values ('X', 'O', or None)
      - winner: 'X', 'O', or None
      - is_draw: bool
      - is_terminal: bool
      - legal_moves: list of empty cell indices
    """
    winner = check_winner(board)
    draw = is_draw(board)
    return {
        "cells": board,
        "winner": winner,
        "is_draw": draw,
        "is_terminal": winner is not None or draw,
        "legal_moves": get_legal_moves(board) if not (winner or draw) else [],
    }
