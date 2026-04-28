from session import create_session, human_move, reset_session
from game import is_terminal
import json

class TicTacToeBridge:
    def __init__(self):
        # Initialize the session
        self.sess = create_session(human_player='X', algorithm='minimax')
        self.sid = self.sess['session_id']
        self.state = self.sess

        self.alpha_sess = create_session(human_player='X', algorithm='alpha_beta')
        self.alpha_sid = self.alpha_sess['session_id']
        self.alpha_state = self.alpha_sess

    def get_state(self):
        """Returns the current state as a JSON string for JS."""
        return json.dumps(self.state)
    
    def get_alpha_state(self):
        """Returns the current alpha state as a JSON string for JS."""
        return json.dumps(self.alpha_state)

    def fulfill_input(self, move_index):
        """
        The JS 'Input Fulfiller'. 
        Triggered when a user clicks a button in the UI.
        """
        move_index = int(move_index)
        legal = self.state['board']['legal_moves']
        
        if move_index not in legal:
            return json.dumps({"error": f"Move {move_index} illegal", "state": self.state})

        self.state = human_move(self.sid, move_index)
        return self.get_state()
    
    def fulfill_alpha_input(self, move_index):
        """
        The JS 'Input Fulfiller'. 
        Triggered when a user clicks a button in the UI. (Alpha)
        """
        move_index = int(move_index)
        legal = self.alpha_state['board']['legal_moves']
        
        if move_index not in legal:
            return json.dumps({"error": f"Move {move_index} illegal", "state": self.alpha_state})

        self.alpha_state = human_move(self.sid, move_index)
        return self.get_alpha_state()

    def restart(self):
        """Resets the game session."""
        self.state = reset_session(self.sid)
        return self.get_state()
    
    def alpha_restart(self):
        """Resets the game session. (Alpha)"""
        self.alpha_state = reset_session(self.alpha_sid)
        return self.get_alpha_state()

# Instantiate for Pyodide to access.
game_controller = TicTacToeBridge()