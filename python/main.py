from session import create_session, human_move, reset_session
from game import is_terminal

def print_board(cells):
    symbols = {None: '.', 'X': 'X', 'O': 'O'}
    print()
    for row in range(3):
        i = row * 3
        print(f" {symbols[cells[i]]} | {symbols[cells[i+1]]} | {symbols[cells[i+2]]} ")
        if row < 2:
            print("---+---+---")
    print()

def print_index_guide():
    print("\n  Cell numbers:")
    for row in range(3):
        i = row * 3
        print(f"  {i} | {i+1} | {i+2} ")
        if row < 2:
            print("  --+---+--")
    print()

def main():
    print("=== Minimax Tic-Tac-Toe ===")
    print("You are X. The AI is O. X goes first.")
    print_index_guide()

    sess = create_session(human_player='X', algorithm='minimax')
    sid = sess['session_id']
    state = sess

    while True:
        print_board(state['board']['cells'])

        if state['board']['is_terminal']:
            winner = state['board']['winner']
            if winner == 'X':
                print("You win!")
            elif winner == 'O':
                print("AI wins!")
            else:
                print("It's a draw!")

            again = input("\nPlay again? (y/n): ").strip().lower()
            if again == 'y':
                state = reset_session(sid)
                print("\n=== New Game ===")
                continue
            else:
                print("Thanks for playing!")
                break

        legal = state['board']['legal_moves']
        print(f"Legal moves: {legal}")

        try:
            move = int(input("Your move (0-8): ").strip())
        except ValueError:
            print("Please enter a number between 0 and 8.")
            continue

        if move not in legal:
            print(f"Cell {move} is not available. Choose from {legal}.")
            continue

        state = human_move(sid, move)

        if 'ai_move' in state:
            print(f"AI played: {state['ai_move']['cell_index']}")

if __name__ == '__main__':
    main()