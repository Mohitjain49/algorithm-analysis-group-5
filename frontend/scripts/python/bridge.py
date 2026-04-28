from session import create_session, human_move, reset_session
from game import is_terminal
import json

class TicTacToeBridge:
    def __init__(self):
        # Initialize the session
        self.sess = create_session(human_player='X', algorithm='minimax')
        self.sid = self.sess['session_id']
        self.state = self.sess

    def get_state(self):
        """Returns the current state as a JSON string for JS."""
        return json.dumps(self.state)

    def fulfill_input(self, move_index):
        """
        The JS 'Input Fulfiller'. 
        Triggered when a user clicks a button in the UI.
        """
        move_index = int(move_index)
        legal = self.state['board']['legal_moves']
        
        # 1. Validate move
        if move_index not in legal:
            return json.dumps({"error": f"Move {move_index} illegal", "state": self.state})

        # 2. Apply move (this also triggers the AI counter-move in session.py)
        self.state = human_move(self.sid, move_index)
        
        # 3. Return the state (including winner info if terminal)
        return self.get_state()

    def restart(self):
        """Resets the game session."""
        self.state = reset_session(self.sid)
        return self.get_state()

# Instantiate for PyScript to access
game_controller = TicTacToeBridge()