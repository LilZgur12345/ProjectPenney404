from src.helpers import PATH_DATA
import numpy as np

def score_game(deck:np.ndarray, p1_seq:str, p2_seq:str) -> str:
    p1_current_position = len(deck) #Initial postitions
    p2_current_position = len(deck)

    for i in range(len(deck) - len(p1_seq) + 1): #From start to end of deck
        seq1_end = i + len(p1_seq)
        if tuple(deck[i:seq1_end]) == p1_seq:
            p1_current_position = i

    for i in range(len(deck) - len(p2_seq) + 1):
        seq2_end = i + len(p2_seq)
        if tuple(deck[i:seq2_end]) == p2_seq:
            p2_current_position = i
    
    #Results
    if p1_current_position < p2_current_position:
        return 'Player 1 is the Winner'
    elif p2_current_position < p1_current_position:
        return 'Player 2 is the Winner'
    else:
        return 'It is a tie'
    
def run_simulation(decks:np.ndarray, seq1:str, seq2:str) -> np.ndarray:
    results = np.array([score_game(deck, seq1, seq2) for deck in decks])
    return results
