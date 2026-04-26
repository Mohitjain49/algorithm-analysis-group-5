"""
algorithms.py — Minimax implementation.

Fully instrumented:
  - node_count: total recursive calls made

Returns a MoveResult dataclass containing the chosen move index,
its score, and all instrumentation data.
"""

from dataclasses import dataclass, field
import time

from game import (
    get_legal_moves,
    apply_move,
    is_terminal,
    terminal_score,
)


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

@dataclass
class SearchStats:
    """Instrumentation data collected during a search."""
    nodes_visited: int = 0
    elapsed_ms: float = 0.0
    algorithm: str = ""


@dataclass
class MoveResult:
    """Result of asking the AI to pick a move."""
    move: int                  # chosen board index (0-8)
    score: int                 # minimax score of the chosen move
    stats: SearchStats = field(default_factory=SearchStats)


# ---------------------------------------------------------------------------
# Plain Minimax
# ---------------------------------------------------------------------------

def _minimax(board: list, is_maximizing: bool, counter: list) -> int:
    """
    Recursive minimax. counter is a single-element list used as a mutable
    integer to count nodes without passing state through returns.
    """
    counter[0] += 1

    if is_terminal(board):
        return terminal_score(board)

    moves = get_legal_moves(board)

    if is_maximizing:
        best = -2
        for move in moves:
            child = apply_move(board, move, 'X')
            score = _minimax(child, False, counter)
            if score > best:
                best = score
        return best
    else:
        best = 2
        for move in moves:
            child = apply_move(board, move, 'O')
            score = _minimax(child, True, counter)
            if score < best:
                best = score
        return best


def minimax_move(board: list, player: str) -> MoveResult:
    """
    Choose the best move for `player` using plain Minimax.

    player: 'X' (maximizer) or 'O' (minimizer)
    """
    is_maximizing = (player == 'X')
    moves = get_legal_moves(board)

    if not moves:
        raise ValueError("No legal moves available.")

    counter = [0]
    best_score = -2 if is_maximizing else 2
    best_move = moves[0]

    t0 = time.perf_counter()

    for move in moves:
        counter[0] += 1
        child = apply_move(board, move, player)
        score = _minimax(child, not is_maximizing, counter)

        if is_maximizing and score > best_score:
            best_score = score
            best_move = move
        elif not is_maximizing and score < best_score:
            best_score = score
            best_move = move

    elapsed = (time.perf_counter() - t0) * 1000

    stats = SearchStats(
        nodes_visited=counter[0],
        elapsed_ms=round(elapsed, 4),
        algorithm="minimax",
    )
    return MoveResult(move=best_move, score=best_score, stats=stats)
