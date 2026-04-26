"""
tests.py — Test suite for the Minimax Tic-Tac-Toe backend.

Run with: python tests.py
"""

import sys
import random
from game import (
    new_board, apply_move, check_winner, is_draw, is_terminal,
    terminal_score, get_legal_moves, board_to_dict,
)
from algorithms import minimax_move
from session import create_session, human_move, reset_session, run_benchmark

PASS = 0
FAIL = 0


def test(name: str, condition: bool, detail: str = ""):
    global PASS, FAIL
    if condition:
        print(f"  PASS  {name}")
        PASS += 1
    else:
        print(f"  FAIL  {name}" + (f" -- {detail}" if detail else ""))
        FAIL += 1


def section(title: str):
    print(f"\n{'─' * 50}")
    print(f"  {title}")
    print(f"{'─' * 50}")


# ---------------------------------------------------------------------------
# Game logic tests
# ---------------------------------------------------------------------------

section("Board & Rules")

b = new_board()
test("New board has 9 empty cells", len(b) == 9 and all(c is None for c in b))

b2 = apply_move(b, 4, 'X')
test("Apply move is non-mutating", b[4] is None and b2[4] == 'X')

try:
    apply_move(b2, 4, 'O')
    test("Occupied cell raises ValueError", False)
except ValueError:
    test("Occupied cell raises ValueError", True)

win_board = ['X', 'X', 'X', 'O', 'O', None, None, None, None]
test("Detect X win (row)", check_winner(win_board) == 'X')

o_diag = ['O', 'X', 'X', None, 'O', None, 'X', None, 'O']
test("Detect O win (diagonal)", check_winner(o_diag) == 'O')

draw_board = ['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'X']
test("Detect draw", is_draw(draw_board))
test("Draw is terminal", is_terminal(draw_board))
test("Draw score is 0", terminal_score(draw_board) == 0)
test("Win score X=+1", terminal_score(win_board) == 1)
test("Win score O=-1", terminal_score(o_diag) == -1)
test("Legal moves on fresh board", get_legal_moves(new_board()) == list(range(9)))
test("Legal moves on full board", get_legal_moves(draw_board) == [])

try:
    terminal_score(new_board())
    test("Non-terminal score raises ValueError", False)
except ValueError:
    test("Non-terminal score raises ValueError", True)

# ---------------------------------------------------------------------------
# Minimax tests
# ---------------------------------------------------------------------------

section("Minimax Algorithm")

must_win = ['X', None, 'X', None, 'O', None, None, None, None]
mm_result = minimax_move(must_win, 'X')
test("Minimax: X plays winning move (index 1)", mm_result.move == 1, f"got {mm_result.move}")
test("Minimax: score is +1 for forced win", mm_result.score == 1)
test("Minimax: nodes_visited > 0", mm_result.stats.nodes_visited > 0)
test("Minimax: elapsed_ms recorded", mm_result.stats.elapsed_ms >= 0)

must_block = ['X', None, 'X', None, None, None, None, None, 'O']
mm_o = minimax_move(must_block, 'O')
test("Minimax: O blocks X (index 1)", mm_o.move == 1, f"got {mm_o.move}")

# ---------------------------------------------------------------------------
# Session tests
# ---------------------------------------------------------------------------

section("Session Management")

sess = create_session(human_player='X', algorithm='minimax')
sid = sess["session_id"]
test("Session created", bool(sid))
test("Human player is X", sess["human_player"] == 'X')
test("AI player is O", sess["ai_player"] == 'O')
test("Board starts empty", all(c is None for c in sess["board"]["cells"]))
test("Current turn is X (human goes first)", sess["current_turn"] == 'X')

state = human_move(sid, 4)
test("Human move registered in history", state["history"][0]["cell_index"] == 4)
test("AI responded (history has 2 entries)", len(state["history"]) == 2)
test("ai_move key present in response", "ai_move" in state)
test("ai_move has stats", "stats" in state["ai_move"])

reset_state = reset_session(sid)
test("Board reset to empty", all(c is None for c in reset_state["board"]["cells"]))
test("History cleared after reset", reset_state["history"] == [])

random.seed(42)
state = reset_session(sid)
game_over = False
for _ in range(9):
    if state["board"]["is_terminal"]:
        game_over = True
        break
    legal = state["board"]["legal_moves"]
    state = human_move(sid, random.choice(legal))
    if state["board"]["is_terminal"]:
        game_over = True
        break

test("Game reaches terminal state", game_over or state["board"]["is_terminal"])
winner = state["board"]["winner"]
test("AI (O) never loses (result is draw or O wins)", winner in (None, 'O'), f"Winner was: {winner}")

# ---------------------------------------------------------------------------
# Benchmark test
# ---------------------------------------------------------------------------

section("Benchmark")

bm = run_benchmark(new_board(), 'X')
test("Benchmark returns minimax results", "minimax" in bm)
test("Benchmark nodes_visited > 0", bm["minimax"]["nodes_visited"] > 0)
test("Benchmark elapsed_ms recorded", bm["minimax"]["elapsed_ms"] >= 0)

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

section("Results")
total = PASS + FAIL
print(f"\n  {PASS}/{total} tests passed")
if FAIL:
    print(f"  {FAIL} test(s) FAILED")
    sys.exit(1)
else:
    print("  All tests passed")
