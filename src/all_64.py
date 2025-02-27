import numpy as np
from datagen import get_decks  # Importing the get_decks function from datagen.py

HALF_DECK_SIZE = 26  # Half deck size for red and black cards

def sequence_to_binary(sequence: str) -> np.ndarray:
    """
    Convert a sequence of 'B' and 'R' into binary (0 for 'B' and 1 for 'R').
    """
    return np.array([0 if ch == 'B' else 1 for ch in sequence])

def find_sequence(deck: np.ndarray, seq: np.ndarray) -> int:
    """
    Find the position of the first occurrence of a sequence in the deck.
    
    Args:
    deck: A shuffled deck of cards.
    seq: The sequence to search for (binary representation).
    
    Returns:
    The position of the first occurrence of the sequence in the deck.
    """
    for i in range(len(deck) - len(seq) + 1):
        if np.array_equal(deck[i:i+len(seq)], seq):
            return i
    return float('inf')  # Return infinity if the sequence is not found

def count_non_overlapping_occurrences(deck: np.ndarray, seq: np.ndarray) -> int:
    """
    Count the total occurrences of a sequence in the shuffled deck, 
    allowing non-overlapping occurrences only.
    
    Args:
    deck: A shuffled deck of cards.
    seq: The sequence to search for (binary representation).
    
    Returns:
    The total count of non-overlapping occurrences of the sequence in the deck.
    """
    count = 0
    i = 0
    while i <= len(deck) - len(seq):
        if np.array_equal(deck[i:i+len(seq)], seq):
            count += 1
            i += len(seq)  # Skip over the found sequence to avoid overlap
        else:
            i += 1  # Move one step forward and keep checking
    return count

def simulate_penneys_game(player1_sequence: str, player2_sequence: str, num_trials: int = 100000, n_decks: int = 1) -> dict:
    """
    Simulate the Penney's game for a given number of trials. Player 1 and Player 2 choose sequences of 3 cards.
    
    Args:
    player1_sequence: The sequence chosen by Player 1 (e.g., 'BBB').
    player2_sequence: The sequence chosen by Player 2 (e.g., 'RBB').
    num_trials: Number of simulation trials (default 100,000).
    n_decks: The number of shuffled decks to generate for each trial.
    
    Returns:
    A dictionary with win/loss/draw probabilities for Player 2.
    """
    # Convert the sequences to binary format
    p1_seq_bin = sequence_to_binary(player1_sequence)
    p2_seq_bin = sequence_to_binary(player2_sequence)
    
    p1_wins_trick, p2_wins_trick, draws_trick = 0, 0, 0
    p1_wins_total, p2_wins_total, draws_total = 0, 0, 0
    
    # Simulate each trial
    for trial in range(num_trials):
        # Generate shuffled decks using get_decks function from datagen.py
        decks = get_decks(n_decks=n_decks, seed=trial)  # Use n_decks for generating multiple decks
        
        # Pick the first deck from the generated shuffled decks
        deck = decks[0]  # You can modify this to loop over different decks if needed
        
        # Find the positions of the sequences in the shuffled deck for trick-based scoring
        p1_pos = find_sequence(deck, p1_seq_bin)
        p2_pos = find_sequence(deck, p2_seq_bin)
        
        # Determine the result for tricks based on the first occurrence of the sequences
        if p1_pos < p2_pos:
            p1_wins_trick += 1
        elif p2_pos < p1_pos:
            p2_wins_trick += 1
        else:
            draws_trick += 1
        
        # Count the non-overlapping occurrences of each player's sequence in the shuffled deck for totals-based scoring
        p1_occurrences = count_non_overlapping_occurrences(deck, p1_seq_bin)
        p2_occurrences = count_non_overlapping_occurrences(deck, p2_seq_bin)
        
        # Determine the result for totals based on the total count of occurrences
        if p1_occurrences > p2_occurrences:
            p1_wins_total += 1
        elif p2_occurrences > p1_occurrences:
            p2_wins_total += 1
        else:
            draws_total += 1
    
    total_trials = num_trials
    return {
        'tricks': {
            'win': p2_wins_trick / total_trials,
            'loss': p1_wins_trick / total_trials,
            'draw': draws_trick / total_trials,
            'player2_win_prob': p2_wins_trick / total_trials,
            'player1_win_prob': p1_wins_trick / total_trials
        },
        'totals': {
            'win': p2_wins_total / total_trials,
            'loss': p1_wins_total / total_trials,
            'draw': draws_total / total_trials,
            'player2_win_prob': p2_wins_total / total_trials,
            'player1_win_prob': p1_wins_total / total_trials
        }
    }

def calculate_win_probabilities(num_trials: int = 100000, n_decks: int = 1) -> dict:
    """
    Calculate the win/loss/draw probabilities for Player 2, based on Penney's game.
    Simulate for all pairs of sequences.

    Args:
    num_trials: Number of trials to run.
    n_decks: The number of shuffled decks to generate for each trial.

    Returns:
    A dictionary of win/loss/draw probabilities for each sequence pair.
    """
    # Define all possible sequences of length 3 ('B' or 'R')
    sequence_list = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']

    probabilities = {}
    # Using nested loops to generate all possible pairs of (p1, p2)
    for p1_seq in sequence_list:
        for p2_seq in sequence_list:
            probabilities[(p1_seq, p2_seq)] = simulate_penneys_game(p1_seq, p2_seq, num_trials=num_trials, n_decks=n_decks)

    return probabilities

if __name__ == '__main__':
    num_trials = 1000  # Number of simulation trials
    n_decks = 1  # You can change the number of decks if needed
    results = calculate_win_probabilities(num_trials, n_decks)

    # Output the results for Player 2's probabilities
    for (p1_seq, p2_seq), probs in results.items():
        print(f"Player 1 chooses {p1_seq} vs Player 2 chooses {p2_seq}:")
        print(f"  - Scoring by tricks: Win={probs['tricks']['win'] * 100:.2f}%, Loss={probs['tricks']['loss'] * 100:.2f}%, Draw={probs['tricks']['draw'] * 100:.2f}%")
        print(f"  - Scoring by totals: Win={probs['totals']['win'] * 100:.2f}%, Loss={probs['totals']['loss'] * 100:.2f}%, Draw={probs['totals']['draw'] * 100:.2f}%")