"""
session.py — Lightweight in-memory game session manager.

Each session tracks:
  - board state
  - whose turn it is
  - move history with stats
  - algorithm in use
"""

import uuid
from dataclasses import dataclass, field
from typing import Optional

from game import new_board, apply_move, board_to_dict, is_terminal
from algorithms import minimax_move, MoveResult

ALGORITHMS = {
    "minimax": minimax_move,
}


@dataclass
class MoveRecord:
    """A single move stored in session history."""
    move_number: int
    player: str
    cell_index: int
    score: Optional[int]
    stats: Optional[dict]


@dataclass
class GameSession:
    session_id: str
    board: list
    human_player: str
    ai_player: str
    current_turn: str
    algorithm: str
    history: list = field(default_factory=list)
    move_number: int = 0


_sessions: dict[str, GameSession] = {}


def create_session(
    human_player: str = 'X',
    algorithm: str = "minimax",
) -> dict:
    """
    Create a new game session.

    human_player: which symbol the human plays ('X' starts first)
    algorithm: 'minimax'
    """
    if algorithm not in ALGORITHMS:
        raise ValueError(f"Unknown algorithm '{algorithm}'. Choose from: {list(ALGORITHMS)}")
    if human_player not in ('X', 'O'):
        raise ValueError("human_player must be 'X' or 'O'.")

    ai_player = 'O' if human_player == 'X' else 'X'
    session_id = str(uuid.uuid4())

    session = GameSession(
        session_id=session_id,
        board=new_board(),
        human_player=human_player,
        ai_player=ai_player,
        current_turn='X',
        algorithm=algorithm,
    )
    _sessions[session_id] = session

    state = _build_state(session)

    if session.current_turn == session.ai_player:
        return _run_ai_turn(session)

    return state


def human_move(session_id: str, cell_index: int) -> dict:
    """
    Apply a human move and (if the game is not over) run the AI's response.
    """
    session = _get_session(session_id)

    if is_terminal(session.board):
        raise ValueError("Game is already over.")

    if session.current_turn != session.human_player:
        raise ValueError("It is not the human's turn.")

    if session.board[cell_index] is not None:
        raise ValueError(f"Cell {cell_index} is already occupied.")

    session.board = apply_move(session.board, cell_index, session.human_player)
    session.move_number += 1
    session.history.append(MoveRecord(
        move_number=session.move_number,
        player=session.human_player,
        cell_index=cell_index,
        score=None,
        stats=None,
    ))
    session.current_turn = session.ai_player

    if is_terminal(session.board):
        return _build_state(session)

    return _run_ai_turn(session)


def run_benchmark(board: list, player: str) -> dict:
    """
    Run Minimax on a given board state and return stats.
    Does not affect any session.
    """
    mm = minimax_move(board, player)
    return {
        "player": player,
        "board_snapshot": board,
        "minimax": {
            "move": mm.move,
            "score": mm.score,
            "nodes_visited": mm.stats.nodes_visited,
            "elapsed_ms": mm.stats.elapsed_ms,
        },
    }


def get_session_state(session_id: str) -> dict:
    """Return the current game state for a session without making any moves."""
    return _build_state(_get_session(session_id))


def reset_session(session_id: str) -> dict:
    """Reset the board while keeping session settings."""
    session = _get_session(session_id)
    session.board = new_board()
    session.current_turn = 'X'
    session.history = []
    session.move_number = 0

    if session.current_turn == session.ai_player:
        return _run_ai_turn(session)

    return _build_state(session)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_session(session_id: str) -> GameSession:
    if session_id not in _sessions:
        raise KeyError(f"Session '{session_id}' not found.")
    return _sessions[session_id]


def _run_ai_turn(session: GameSession) -> dict:
    """Execute the AI move and update session state."""
    ai_fn = ALGORITHMS[session.algorithm]
    result: MoveResult = ai_fn(session.board, session.ai_player)

    session.board = apply_move(session.board, result.move, session.ai_player)
    session.move_number += 1
    session.history.append(MoveRecord(
        move_number=session.move_number,
        player=session.ai_player,
        cell_index=result.move,
        score=result.score,
        stats={
            "algorithm": result.stats.algorithm,
            "nodes_visited": result.stats.nodes_visited,
            "elapsed_ms": result.stats.elapsed_ms,
        },
    ))
    session.current_turn = session.human_player

    state = _build_state(session)
    state["ai_move"] = {
        "cell_index": result.move,
        "score": result.score,
        "stats": state["history"][-1]["stats"],
    }
    return state


def _build_state(session: GameSession) -> dict:
    """Serialize full session state."""
    board_info = board_to_dict(session.board)
    return {
        "session_id": session.session_id,
        "board": board_info,
        "human_player": session.human_player,
        "ai_player": session.ai_player,
        "current_turn": session.current_turn,
        "algorithm": session.algorithm,
        "move_number": session.move_number,
        "history": [
            {
                "move_number": r.move_number,
                "player": r.player,
                "cell_index": r.cell_index,
                "score": r.score,
                "stats": r.stats,
            }
            for r in session.history
        ],
    }
