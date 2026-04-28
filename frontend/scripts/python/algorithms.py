from dataclasses import dataclass, field
from typing import Optional
import time

from game import (
    get_legal_moves,
    apply_move,
    is_terminal,
    terminal_score,
    check_winner,
    is_draw,
)


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

@dataclass
class SearchStats:
    """Instrumentation data collected during a search."""
    nodes_visited: int = 0
    pruned_branches: int = 0
    elapsed_ms: float = 0.0
    algorithm: str = ""

    @property
    def pruning_efficiency(self) -> Optional[float]:
        """Percentage of branches pruned (alpha-beta only); None for plain minimax."""
        if self.algorithm != "alpha_beta":
            return None
        total = self.nodes_visited + self.pruned_branches
        if total == 0:
            return 0.0
        return round(self.pruned_branches / total * 100, 2)


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
        counter[0] += 1  # count root-level expansions
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
        pruned_branches=0,
        elapsed_ms=round(elapsed, 4),
        algorithm="minimax",
    )
    return MoveResult(move=best_move, score=best_score, stats=stats)


# ---------------------------------------------------------------------------
# Alpha-Beta Pruning
# ---------------------------------------------------------------------------

def _alpha_beta(
    board: list,
    is_maximizing: bool,
    alpha: int,
    beta: int,
    counter: list,
    pruned: list,
) -> int:
    """
    Recursive minimax with alpha-beta pruning.
    counter and pruned are single-element mutable lists (node + prune counters).
    """
    counter[0] += 1

    if is_terminal(board):
        return terminal_score(board)

    moves = get_legal_moves(board)

    if is_maximizing:
        value = -2
        for move in moves:
            child = apply_move(board, move, 'X')
            score = _alpha_beta(child, False, alpha, beta, counter, pruned)
            value = max(value, score)
            alpha = max(alpha, value)
            if beta <= alpha:
                pruned[0] += len(moves) - moves.index(move) - 1
                break
        return value
    else:
        value = 2
        for move in moves:
            child = apply_move(board, move, 'O')
            score = _alpha_beta(child, True, alpha, beta, counter, pruned)
            value = min(value, score)
            beta = min(beta, value)
            if beta <= alpha:
                pruned[0] += len(moves) - moves.index(move) - 1
                break
        return value


def alpha_beta_move(board: list, player: str) -> MoveResult:
    """
    Choose the best move for `player` using Minimax with Alpha-Beta Pruning.

    player: 'X' (maximizer) or 'O' (minimizer)
    """
    is_maximizing = (player == 'X')
    moves = get_legal_moves(board)

    if not moves:
        raise ValueError("No legal moves available.")

    counter = [0]
    pruned = [0]
    best_score = -2 if is_maximizing else 2
    best_move = moves[0]
    alpha = -2
    beta = 2

    t0 = time.perf_counter()

    for move in moves:
        counter[0] += 1
        child = apply_move(board, move, player)
        score = _alpha_beta(child, not is_maximizing, alpha, beta, counter, pruned)

        if is_maximizing:
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
        else:
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, best_score)

    elapsed = (time.perf_counter() - t0) * 1000

    stats = SearchStats(
        nodes_visited=counter[0],
        pruned_branches=pruned[0],
        elapsed_ms=round(elapsed, 4),
        algorithm="alpha_beta",
    )
    return MoveResult(move=best_move, score=best_score, stats=stats)
