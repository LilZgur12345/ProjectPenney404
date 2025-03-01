import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datagen import augmenting_decks
from processing import calculate_win_probabilities

def all_possible_sequences(length: int) -> list:
    """
    Generates all possible sequences of length 3 (total of 8)

    Args:
        length (int): The length of the sequence

    Returns: 
        A list of all possible sequences
    """
    return [list(format(i, f'0{length}b')) for i in range(2**length)]

def create_heatmaps(heatmap_total, heatmap_tricks, output_file, n_decks) -> None:
    """
    Creates the heatmaps that contain totals and tricks win probabilities

    Args:
        heatmap_total (np.ndarray): The heatmap for total cards win probabilities
        heatmap_tricks (np.ndarray): The heatmap for tricks win probabilities
        output_file (str): The name of the output file
        n_decks (int): The number of decks

    Returns: 
        None
    """
    ax_labels = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_total * 100, annot=True, fmt=".1f", cmap="Blues",
                xticklabels=ax_labels, yticklabels=ax_labels,
                cbar_kws={'label': 'Player 2 Win Probability'})
    plt.title(f"Penney's Game Heatmap [Total Cards] - {n_decks} Decks")
    plt.xlabel("Player 2 Sequence")
    plt.ylabel("Player 1 Sequence")
    plt.tight_layout()
    plt.savefig(f"totals_{output_file}.png")
    print(f"Saved totals heatmap as totals_{output_file}.png")
    plt.clf()

    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_tricks * 100, annot=True, fmt=".1f", cmap="Blues",
                xticklabels=ax_labels, yticklabels=ax_labels,
                cbar_kws={'label': 'Player 2 Win Probability'})
    plt.title(f"Penney's Game Heatmap [Tricks] - {n_decks} Decks")
    plt.xlabel("Player 2 Sequence")
    plt.ylabel("Player 1 Sequence")
    plt.tight_layout()
    plt.savefig(f"tricks_{output_file}.png")
    print(f"Saved tricks heatmap as tricks_{output_file}.png")
    plt.clf()

def fill_heatmaps(seed: int, n_decks: int, augment_decks: int, output_file: str = 'penney_heatmaps') -> None:
    """
    Generate the heatmaps for Penney's game

    Args:
        seed (int): The seed for generating decks
        n_decks (int): The number of decks
        augment_decks (int): The number of additional decks to augment
        output_file (str): The base name for the file containing the heatmaps

    Returns:
        None
    """
    # Augment decks using datagen.py
    augment = augment_decks > 0
    augmenting_decks(n_decks=n_decks, augment_decks=augment_decks, seed=seed, augment=augment)
    seq_length = 3
    all_sequences = all_possible_sequences(seq_length)

    # Initialize the heatmaps with 2D arrays
    heatmap_total = np.zeros((len(all_sequences), len(all_sequences)))  # Total cards heatmap
    heatmap_tricks = np.zeros((len(all_sequences), len(all_sequences)))  # Tricks heatmap

    results = calculate_win_probabilities(n_decks=n_decks + augment_decks)

    # Populate the heatmaps
    for i, seq1 in enumerate(all_sequences):
        for j, seq2 in enumerate(all_sequences):
            p1_seq = ''.join(['B' if binary == '0' else 'R' for binary in seq1])
            p2_seq = ''.join(['B' if binary == '0' else 'R' for binary in seq2])
            
            result = results[(p1_seq, p2_seq)]  

            if type(result) == dict and 'tricks' in result and 'totals' in result:
                tricks_result = result['tricks']
                totals_result = result['totals']

                # Store the probabilities in the heatmaps
                heatmap_tricks[i, j] = tricks_result['win']
                heatmap_total[i, j] = totals_result['win']

                if 'player1_win_probability' in tricks_result and 'player1_win_probability' in totals_result:
                    heatmap_tricks[j, i] = tricks_result['player1_win_probability']
                    heatmap_total[j, i] = totals_result['player1_win_probability']
            else:
                print(f"Result: {result}")

    # Create and save the heatmaps
    create_heatmaps(heatmap_total, heatmap_tricks, output_file, n_decks + augment_decks)