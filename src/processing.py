import numpy as np
from datagen import get_decks

HALF_DECK_SIZE = 26

def sequence_to_binary(sequence: str) -> np.ndarray:
    """
    Converts the sequence into binary 0's & 1's

    Args:
        sequence: The sequence containing 'B' & 'R'

    Returns:
        An array of 0's & 1's for the given sequence
    """
    return np.array([0 if char == 'B' else 1 for char in sequence]) # 'B' = 0, 'R' = 1

def find_sequence(deck: np.ndarray, sequence: np.ndarray) -> int:
    """
    Find the sequence's first appearance in the deck

    Args:
        deck: The shuffled deck of cards
        seq: The sequence we're looking for

    Returns:
        The position of i, where the sequence starts in the deck
    """
    for i in range(len(deck) - len(sequence) + 1):
        if np.array_equal(deck[i:i+len(sequence)], sequence):
            return i
    return len(deck)   # If sequence is not found, return the end of the deck

def count_occurrences(deck: np.ndarray, sequence: np.ndarray) -> int:
    """
    Finds the number of times a sequence occurs in the shuffled deck (non-overlapping)

    Args:
        deck: The shuffled deck of cards
        seq: The sequence we're looking for

    Returns:
        The total count of sequence occurrences
    """
    count = 0
    i = 0
    while i <= len(deck) - len(sequence):
        if np.array_equal(deck[i:i+len(sequence)], sequence): # Checking if the sequence is found
            count += 1
            i += len(sequence)
        else:
            i += 1
    return count

def penneys_game(p1_sequence: str, p2_sequence: str, n_decks: int) -> dict:
    """
    Player 1 & player 2 choose sequences of 3 cards that are compared based on tricks/totals scoring

    Args:
        p1_sequence: First player's sequence
        p2_sequence: Second player's sequence
        n_decks: The number of shuffled decks

    Returns:
        A dictionary with player 2's win/loss/draw probabilities
    """

    # First convert the sequences to binary
    p1_seq_binary = sequence_to_binary(p1_sequence)
    p2_seq_binary = sequence_to_binary(p2_sequence)

    p1_wins_trick, p2_wins_trick, draws_trick = 0, 0, 0
    p1_wins_totals, p2_wins_totals, draws_totals = 0, 0, 0

    for i in range(n_decks): 
        # Generate shuffled decks for each trial
        decks = get_decks(n_decks=1, seed=i)

        # The first deck from the shuffled decks
        deck = decks[0]

        # Find the positions of the sequences for tricks-based scoring
        p1_pos = find_sequence(deck, p1_seq_binary)
        p2_pos = find_sequence(deck, p2_seq_binary)

        # Determine the results for tricks
        if p1_pos < p2_pos:
            p1_wins_trick += 1
        elif p2_pos < p1_pos:
            p2_wins_trick += 1
        else:
            draws_trick += 1

        # Count the occurrences of each player's sequence for totals-based scoring
        p1_occurrences = count_occurrences(deck, p1_seq_binary)
        p2_occurrences = count_occurrences(deck, p2_seq_binary)

        # Results for totals
        if p1_occurrences > p2_occurrences:
            p1_wins_totals += 1
        elif p2_occurrences > p1_occurrences:
            p2_wins_totals += 1
        else:
            draws_totals += 1

    total_trials = n_decks 

    return {
        'tricks': {
            'win': p2_wins_trick / total_trials,
            'loss': p1_wins_trick / total_trials,
            'draw': draws_trick / total_trials,
            'player2_win_probability': p2_wins_trick / total_trials,
            'player1_win_probability': p1_wins_trick / total_trials
        },
        'totals': {
            'win': p2_wins_totals / total_trials,
            'loss': p1_wins_totals / total_trials,
            'draw': draws_totals / total_trials,
            'player2_win_probability': p2_wins_totals / total_trials,
            'player1_win_probability': p1_wins_totals / total_trials
        }
    }

def calculate_win_probabilities(n_decks: int) -> dict:
    """
    Calculates player 2's probabilities of winning/lossing/drawing

    Args:
        n_decks: The number of shuffled decks

    Returns:
        A dictionary of win/loss/draw probabilities for each pair of sequences
    """
    # Define all possible sequences of length 3 ('B' or 'R')
    sequence_list = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']

    # Create an empty dictionary
    probabilities = {}
    for p1_seq in sequence_list:
        for p2_seq in sequence_list:
            probabilities[(p1_seq, p2_seq)] = penneys_game(p1_seq, p2_seq, n_decks=n_decks)

    return probabilities

if __name__ == '__main__':
    n_decks = 100_000  # The game will be played 100,000 times
    results = calculate_win_probabilities(n_decks)

    for (p1_seq, p2_seq), probs in results.items():
        print(f"Player 1 {p1_seq} vs Player 2 {p2_seq}:")
        print(f"  Scoring by tricks: Win={probs['tricks']['win'] * 100:.2f}%, Loss={probs['tricks']['loss'] * 100:.2f}%, Draw={probs['tricks']['draw'] * 100:.2f}%")
        print(f"  Scoring by totals: Win={probs['totals']['win'] * 100:.2f}%, Loss={probs['totals']['loss'] * 100:.2f}%, Draw={probs['totals']['draw'] * 100:.2f}%")