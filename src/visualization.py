import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
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
    return [''.join(format(i, f'0{length}b').replace('0', 'B').replace('1', 'R')) for i in range(2**length)]

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
                xticklabels=ax_labels, yticklabels=ax_labels, cbar=False, 
                linewidths=0.5, linecolor='white',
                cbar_kws={'label': 'Player 2 Win Probability'})
    plt.title(f"Penney's Game Heatmap [Total Cards] - {n_decks} Decks")
    plt.xlabel("Player 2 Sequence")
    plt.ylabel("Player 1 Sequence")
    plt.tight_layout()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
    file_path = os.path.join('heatmaps', f"totals_{output_file}_{timestamp}.png")
    plt.savefig(file_path)
    print(f"Saved totals heatmap as totals_{output_file}_{timestamp}.png")
    plt.clf()

    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_tricks * 100, annot=True, fmt=".1f", cmap="Blues",
                xticklabels=ax_labels, yticklabels=ax_labels, cbar=False, 
                linewidths=0.5, linecolor='white',
                cbar_kws={'label': 'Player 2 Win Probability'})
    plt.title(f"Penney's Game Heatmap [Tricks] - {n_decks} Decks")
    plt.xlabel("Player 2 Sequence")
    plt.ylabel("Player 1 Sequence")
    plt.tight_layout()
    timestamp2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
    file_path2 = os.path.join('heatmaps', f"tricks_{output_file}_{timestamp2}.png")
    plt.savefig(file_path2)
    print(f"Saved tricks heatmap as tricks_{output_file}_{timestamp2}.png")
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
            result = results.get((seq1, seq2))

            if result is not None:
                tricks_result = result.get('tricks', {})
                cards_result = result.get('cards', {}) #Changed this line

                if 'win' in tricks_result and 'win' in cards_result:
                    # Store the probabilities in the heatmaps
                    heatmap_tricks[i, j] = tricks_result['win']
                    heatmap_total[i, j] = cards_result['win'] #And this line

    # Create and save the heatmaps
    create_heatmaps(heatmap_total, heatmap_tricks, output_file, n_decks + augment_decks)