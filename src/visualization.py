import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import numpy as np
import matplotlib.patches as patches
from datagen import augmenting_decks
from processing import calculate_win_probabilities 

def all_possible_sequences(length: int
                           ) -> list:
    """
    Generates all possible sequences of length 3 (total of 8)

    Args:
        length (int): The length of the sequence

    Returns:
        A list of all possible sequences
    """
    # All 8 sequences with length = 3 converted from binary
    return [format(i, f'0{length}b').replace('0', 'B').replace('1', 'R') for i in range(8)]

def create_heatmaps(heatmap_cards, heatmap_tricks, output_file, n_decks, draws_cards, draws_tricks
                    ) -> None:
    """
    Create the heatmaps that contain totals and tricks win probabilities

    Args:
        heatmap_total (np.ndarray): The heatmap for cards (p2 win probabilities)
        heatmap_tricks (np.ndarray): The heatmap for tricks (p2 win probabilities)
        output_file (str): The name of the output file
        n_decks (int): The number of decks

    Returns:
        None
    """
    ax_labels = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']
    plt.figure(figsize=(12, 8))

    # Creates heatmap for cards
    ax1 = sns.heatmap(heatmap_cards * 100, annot=False, cmap='Blues',
                xticklabels=ax_labels, yticklabels=ax_labels, cbar=False, 
                linewidths=0.65, linecolor='white', square=True,
                cbar_kws={'label': 'Player 2 Win Probability'})
    for i in range(len(ax_labels)):
        # Creates a rectangle with length and width = 1 for each cell
        ax1.add_patch(patches.Rectangle((i, i), 1, 1, facecolor="lightgray", linewidth=0.65, edgecolor='white', zorder=4)) 
    
    for i in range(8):
        for j in range(8):
            win_prob = heatmap_cards[i, j]
            draw_prob = draws_cards[i, j]
            text = f"{win_prob * 100:.0f} ({draw_prob * 100:.0f})"  # Win (Draw)
            if win_prob > 0.5:  # If win prob is > 50%, use white text
                text_color = 'white'
            else:
                text_color = 'black'
            # 0.5 is half of the cell size
            ax1.text(j + 0.5, i + 0.5, text, ha='center', va='center', color=text_color)

    plt.title(f"Penney's Game Probabilities for P2 \n Win (Draw) by Cards \n N = {n_decks}")
    plt.xlabel("Player 2 Sequence")
    plt.ylabel("Player 1 Sequence")
    plt.tight_layout()

    # Saves as a PNG with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current timestamp
    file_path = os.path.join('heatmaps', f"totals_{output_file}_{timestamp}.png")
    plt.savefig(file_path)
    print(f"Saved totals heatmap as totals_{output_file}_{timestamp}.png")
    plt.clf()
    plt.figure(figsize=(12, 8))

    # Creates heatmap for tricks
    ax2 = sns.heatmap(heatmap_tricks * 100, annot=False, cmap='Blues',
                xticklabels=ax_labels, yticklabels=ax_labels, cbar=False, 
                linewidths=0.65, linecolor='white', square=True,
                cbar_kws={'label': 'Player 2 Win Probability'})
    for i in range(len(ax_labels)):
        # Creates a rectangle with length and width = 1 for each cell
        ax2.add_patch(patches.Rectangle((i, i), 1, 1, facecolor="lightgray", linewidth=0.65, edgecolor='white', zorder=4)) 
   
    for i in range(8):
        for j in range(8):
            win_prob = heatmap_tricks[i, j]
            draw_prob = draws_tricks[i, j]
            text = f"{win_prob * 100:.0f} ({draw_prob * 100:.0f})" # Win (Draw)
            if win_prob > 0.5:  # If win prob is > 50%, use white text
                text_color = 'white'
            else:
                text_color = 'black'
            # 0.5 is half of the cell size
            ax2.text(j + 0.5, i + 0.5, text, ha='center', va='center', color=text_color)

    plt.title(f"Penney's Game Probabilities for P2 \n Win (Draw) by Tricks \n N = {n_decks}")
    plt.xlabel("Player 2 Sequence")
    plt.ylabel("Player 1 Sequence")
    plt.tight_layout()

    # Saves as a PNG with timestamp
    timestamp2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
    file_path2 = os.path.join('heatmaps', f"tricks_{output_file}_{timestamp2}.png")
    plt.savefig(file_path2)
    print(f"Saved tricks heatmap as tricks_{output_file}_{timestamp2}.png")
    plt.clf()

def fill_heatmaps(seed: int, 
                  n_decks: int, 
                  augment_decks: int, 
                  output_file: str = 'penney_heatmaps'
                  ) -> None:
    """
    Generate the heatmaps for Penney's game

    Args:
        seed (int): The seed used
        n_decks (int): The number of decks
        augment_decks (int): The number of additional decks to augment
        output_file (str): The base name for the file containing the heatmaps

    Returns:
        None
    """
    # Augment decks if desired
    augment = augment_decks > 0
    augmenting_decks(n_decks = n_decks, augment_decks = augment_decks, seed = seed, augment = augment)

    seq_length = 3
    all_sequences = all_possible_sequences(seq_length)

    # First create 2D arrays for the heatmaps
    heatmap_cards = np.zeros((len(all_sequences), len(all_sequences)))  
    heatmap_tricks = np.zeros((len(all_sequences), len(all_sequences)))

    # For draws
    draws_cards = np.zeros((len(all_sequences), len(all_sequences)))  
    draws_tricks = np.zeros((len(all_sequences), len(all_sequences)))

    results = calculate_win_probabilities(n_decks = n_decks + augment_decks)

    # Populate the heatmaps with game outcomes
    for i, seq1 in enumerate(all_sequences):
        for j, seq2 in enumerate(all_sequences):
            result = results.get((seq1, seq2))
            # Check if result (win probability) exists
            if result is not None:
                # Break down into tricks and cards results
                tricks_result = result.get('tricks', {})
                cards_result = result.get('cards', {}) 

                # If player 2 wins in both tricks and cards
                if 'win' in tricks_result and 'win' in cards_result:
                    # Store the probabilities in the heatmaps
                     heatmap_tricks[i, j] = tricks_result['win'] 
                     draws_tricks[i, j] = tricks_result['draw'] 
                     heatmap_cards[i, j] = cards_result['win'] 
                     draws_cards[i, j] = cards_result['draw'] 


    # Save the heatmaps
    create_heatmaps(heatmap_cards, heatmap_tricks, output_file, n_decks + augment_decks, draws_cards, draws_tricks)