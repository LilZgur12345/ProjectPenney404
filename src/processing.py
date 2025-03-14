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
    return np.array([0 if char == 'B' else 1 for char in sequence])  # 'B' = 0, 'R' = 1

def play_game_deck(deck: list, p1_seq: tuple, p2_seq: tuple) -> dict:
    """
Simulates a single Penney's game deck and returns win statistics.

Args:
    deck: The shuffled deck of cards (as a list).
    p1_seq: Player 1's sequence (as a tuple).
    p2_seq: Player 2's sequence (as a tuple).

Returns:
    A dictionary containing the number of tricks won by each player and the
    number of cards won by each player.
"""

# Initialize variables
    memory = []  # The memory that will store the most recent cards
    tricks = [0, 0]  # [Player 1's tricks, Player 2's tricks]
    p1_cards = [0]
    p2_cards = [0]
    extra = [0]
    num_cards = 0

# Process the deck and check for sequences
    for elem in deck:
        memory.append(elem)
        num_cards += 1

    # Check if the last `len(p1_seq)` cards match player 1's sequence
        if tuple(memory[-len(p1_seq):]) == p1_seq:
            tricks[0] += 1
            p1_cards[0] += num_cards
            num_cards = 0
            memory = []  # Reset memory after player 1's sequence match
            continue # addded continue

    # Check if the last `len(p2_seq)` cards match player 2's sequence
        elif tuple(memory[-len(p2_seq):]) == p2_seq:
            tricks[1] += 1
            p2_cards[0] += num_cards
            num_cards = 0
            memory = []  # Reset memory after player 2's sequence match
            continue # added continue
        else:
        # If memory is too long (greater than or equal to the sequence length), remove the oldest card
            if len(memory) >= len(p1_seq):
                memory.pop(0)

    extra[0] += num_cards  # Add remaining cards to extra

    return {"tricks": tricks, "p1_cards": p1_cards, "p2_cards": p2_cards, "extra cards": extra}

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

# If the sequences are identical, player 2 cannot win
    if p1_sequence == p2_sequence:
        return {
            'tricks': {
            'win': 0.0,
            'loss': 1.0,
            'draw': 0.0,
            'player2_win_probability': 0.0,
            'player1_win_probability': 1.0
            },
            'cards': {
            'win': 0.0,
            'loss': 1.0,
            'draw': 0.0,
            'player2_win_probability': 0.0,
            'player1_win_probability': 1.0
             }
        }

    p1_wins_tricks, p2_wins_tricks, draws_tricks = 0, 0, 0
    p1_wins_cards, p2_wins_cards, draws_cards = 0, 0, 0

    for i in range(n_decks):
    # Generate shuffled decks for each trial
        decks = get_decks(n_decks=1, seed=i)

    # The first deck from the shuffled decks
        deck = decks[0].tolist()

    # Play the game using the helper function
        win_stats = play_game_deck(deck, tuple(p1_seq_binary), tuple(p2_seq_binary))

    # Score based on the tricks won
        if win_stats['tricks'][0] > win_stats['tricks'][1]:
            p1_wins_tricks += 1
        elif win_stats['tricks'][1] > win_stats['tricks'][0]:
            p2_wins_tricks += 1
        else:
            draws_tricks += 1

    # Score based on number of cards won
        if win_stats['p1_cards'][0] > win_stats['p2_cards'][0]:
            p1_wins_cards += 1
        elif win_stats['p2_cards'][0] > win_stats['p1_cards'][0]:
            p2_wins_cards += 1
        else:
            draws_cards += 1

    total_trials = n_decks

    return {
        'tricks': {
            'win': p2_wins_tricks / total_trials,
            'loss': p1_wins_tricks / total_trials,
            'draw': draws_tricks / total_trials,
            'player2_win_probability': p2_wins_tricks / total_trials,
            'player1_win_probability': p1_wins_tricks / total_trials
        },
        'cards': {
            'win': p2_wins_cards / total_trials,
            'loss': p1_wins_cards / total_trials,
            'draw': draws_cards / total_trials,
            'player2_win_probability': p2_wins_cards / total_trials,
            'player1_win_probability': p1_wins_cards / total_trials
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

    probabilities = {}
    for p1_seq in sequence_list:
        for p2_seq in sequence_list:
            probabilities[(p1_seq, p2_seq)] = penneys_game(p1_seq, p2_seq, n_decks=n_decks)

    return probabilities