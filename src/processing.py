import numpy as np
from datagen import get_decks

def sequence_to_binary(sequence: str
                       ) -> np.ndarray:
    """
    Convert the sequence into binary 0s & 1s

    Args:
        sequence (str): The sequence consisting of 'B' & 'R'

    Returns:
        An array of 0s & 1s for the given sequence
    """
    # Convert characters into binary
    return np.array([0 if char == 'B' else 1 for char in sequence])  # 'B' = 0, 'R' = 1

def play_game(deck: list, 
              p1_sequence: tuple, 
              p2_sequence: tuple
              ) -> dict:
    """
    Simulate the logic of Penney's Game using the shuffled deck

    Args:
        deck (list): The shuffled deck 
        p1_seq (tuple): Player 1's sequence 
        p2_seq (tuple): Player 2's sequence

    Returns:
        A dictionary containing the number of tricks/cards 
        won by each player
    """
    tricks = [0, 0]  # Total tricks won by each player - list
    p1_cards, p2_cards = 0, 0  # Total cards won by each player - ints
    num_cards = 0
    # Holds the last sequence (three cards)
    last_sequence = []  

    # Go through each card in the deck
    for i in deck:
        last_sequence.append(i)
        num_cards += 1

        # Ensure that last_sequence has no more than 3 cards
        last_sequence = last_sequence[-3:]

        # Check if the last 3 cards match player 1's sequence
        if len(last_sequence) == 3:
            if tuple(last_sequence) == p1_sequence:
                tricks[0] += 1
                p1_cards += num_cards
                num_cards = 0 # Reset card count 
                last_sequence = [] # Reset last_sequence after player 1's match
                continue

        # Check if the last 3 cards match player 2's sequence
            if tuple(last_sequence) == p2_sequence:
                tricks[1] += 1
                p2_cards += num_cards  
                num_cards = 0 # Reset card count 
                last_sequence = [] # Reset last_sequence after player 2's match
                continue

    return {'tricks': tricks, 'p1_cards': p1_cards, 'p2_cards': p2_cards}

def penneys_game(p1_sequence: str, 
                 p2_sequence: str, 
                 n_decks: int
                 ) -> dict:
    """
    Player 1 & player 2 each choose sequences of 3 cards, 
    scored by tricks/totals

    Args:
        p1_sequence (str): First player's sequence
        p2_sequence (str): Second player's sequence
        n_decks (int): The number of shuffled decks

    Returns:
        A dictionary with player 2's win/loss/draw probabilities
    """
    # Convert the sequences to binary
    p1_seq_binary = sequence_to_binary(p1_sequence)
    p2_seq_binary = sequence_to_binary(p2_sequence)

    # Initialize counters
    p1_wins_tricks, p2_wins_tricks, draws_tricks = 0, 0, 0
    p1_wins_cards, p2_wins_cards, draws_cards = 0, 0, 0

    for i in range(n_decks):
        # Generate shuffled decks
        deck = get_decks(n_decks = 1, seed = i)[0].tolist()

        # Play the game using play_game()
        win_stats = play_game(deck, tuple(p1_seq_binary), tuple(p2_seq_binary))

        # Score based on tricks
        if win_stats['tricks'][0] > win_stats['tricks'][1]:
            p1_wins_tricks += 1
        elif win_stats['tricks'][1] > win_stats['tricks'][0]:
            p2_wins_tricks += 1
        else:
            draws_tricks += 1

        # Score based on cards
        if win_stats['p1_cards'] > win_stats['p2_cards']:
            p1_wins_cards += 1
        elif win_stats['p2_cards'] > win_stats['p1_cards']:
            p2_wins_cards += 1
        else:
            draws_cards += 1

    total_decks = n_decks

    # When sequences are the same -> draw
    if p1_sequence == p2_sequence:
      p1_wins_tricks, p2_wins_tricks, draws_tricks = 0, 0, n_decks
      p1_wins_cards, p2_wins_cards, draws_cards = 0, 0, n_decks

    # Return the probabilties for tricks/total cards
    return {
        'tricks': {
            'win': p2_wins_tricks / total_decks,
            'loss': p1_wins_tricks / total_decks,
            'draw': draws_tricks / total_decks,
            'player2_win_probability': p2_wins_tricks / total_decks,
            'player1_win_probability': p1_wins_tricks / total_decks
        },
        'cards': {
            'win': p2_wins_cards / total_decks,
            'loss': p1_wins_cards / total_decks,
            'draw': draws_cards / total_decks,
            'player2_win_probability': p2_wins_cards / total_decks,
            'player1_win_probability': p1_wins_cards / total_decks
        }
    }

def calculate_win_probabilities(n_decks: int
                                ) -> dict:
    """
    Calculate player 2's probabilities of winning/lossing/drawing 
    for all possible sequences

    Args:
        n_decks: The number of shuffled decks

    Returns:
        A dictionary of win/loss/draw probabilities for each pair of sequences
    """
    # Define all possible sequences of length 3 ('B' or 'R')
    sequence_list = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']

    probabilities = {}
    for p1_sequence in sequence_list:
        for p2_sequence in sequence_list:
            # Find the probability for each sequence pair
            result = penneys_game(p1_sequence, p2_sequence, n_decks = n_decks)
            probabilities[(p1_sequence, p2_sequence)] = {
                # Return tricks and total cards win probabilities 
                'tricks': result['tricks'], 
                'cards': result['cards']    
            }
    return probabilities