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
    tricks = [0, 0]  # [Player 1's tricks, Player 2's tricks]
    p1_cards = 0
    p2_cards = 0
    num_cards = 0
    recent_cards = []  # Holds the most recent cards to check against sequences

    # Process the deck and check for sequences
    for elem in deck:
        recent_cards.append(elem)
        num_cards += 1

        # If the length of recent_cards exceeds the length of the sequences, remove the oldest card
        if len(recent_cards) > max(len(p1_seq), len(p2_seq)):
            recent_cards.pop(0)

        # Check if the last `len(p1_seq)` cards match player 1's sequence
        if len(recent_cards) >= len(p1_seq) and tuple(recent_cards[-len(p1_seq):]) == p1_seq:
            tricks[0] += 1
            p1_cards += num_cards  # Track total cards for player 1
            num_cards = 0  # Reset card count after a sequence match
            recent_cards = []  # Reset recent_cards after player 1's sequence match
            continue

        # Check if the last `len(p2_seq)` cards match player 2's sequence
        elif len(recent_cards) >= len(p2_seq) and tuple(recent_cards[-len(p2_seq):]) == p2_seq:
            tricks[1] += 1
            p2_cards += num_cards  # Track total cards for player 2
            num_cards = 0  # Reset card count after a sequence match
            recent_cards = []  # Reset recent_cards after player 2's sequence match
            continue

    return {"tricks": tricks, "p1_cards": p1_cards, "p2_cards": p2_cards}

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

        # Determine card winner for this deck
        if win_stats['p1_cards'] > win_stats['p2_cards']:
            p1_wins_cards += 1
        elif win_stats['p2_cards'] > win_stats['p1_cards']:
            p2_wins_cards += 1
        else:
            draws_cards += 1


    total_trials = n_decks

    # Identical Sequence Logic
    if p1_sequence == p2_sequence:
      p1_wins_tricks, p2_wins_tricks, draws_tricks = 0, 0, n_decks
      p1_wins_cards, p2_wins_cards, draws_cards = 0, 0, n_decks



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


