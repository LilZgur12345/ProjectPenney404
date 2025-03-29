import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import numpy as np
import matplotlib.patches as patches
from src.helpers import PATH_DATA
from src.datagen import store_decks
from processing import calculate_win_probabilities

# Specify the number of initial decks
initial_num_decks = 1_000_000

# Define the path for the initial heatmaps and data files
initial_cards_data = f'probability_data/cards_{initial_num_decks}_decks.npy'
initial_tricks_data = f'probability_data/tricks_{initial_num_decks}_decks.npy'
draws_cards_data = f'probability_data/draws_cards_{initial_num_decks}_decks.npy'
draws_tricks_data = f'probability_data/draws_tricks_{initial_num_decks}_decks.npy'

initial_cards_heatmap_PNG = f'heatmaps/cards_{initial_num_decks}_decks.png'
initial_tricks_heatmap_PNG = f'heatmaps/tricks_{initial_num_decks}_decks.png'

def all_possible_sequences(length: int) -> list:
    """
    Generates all possible sequences of length 3 (total of 8)

    Args:
        length (int): The length of the sequence

    Returns:
        A list of all possible sequences
    """
    return [format(i, f'0{length}b').replace('0', 'B').replace('1', 'R') for i in range(8)]

def create_heatmaps(cards_data: np.ndarray, 
                    tricks_data: np.ndarray, 
                    output_file: str, 
                    n_decks: int, 
                    ) -> None:
    """
    Create the heatmaps that contain totals and tricks win/draw probabilities

    Args:
        cards_data (np.ndarray): The heatmap for cards (p2's probabilities)
        tricks_data (np.ndarray): The heatmap for tricks (p2's probabilities)
        output_file (str): The name of the output file
        n_decks (int): The number of decks

    Returns:
        None
    """
    ax_labels = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']
    
    # For cards heatmap
    plt.figure(figsize = (12, 8))
    ax1 = sns.heatmap(cards_data[0] * 100, annot = False, cmap = 'Blues',
                xticklabels = ax_labels, yticklabels = ax_labels, cbar = False, 
                linewidths = 0.65, linecolor = 'white', square = True,
                cbar_kws = {'label': 'Player 2 Win Probability'})
    
    # Creates a rectangle with length and width = 1 for each cell
    for i in range(len(ax_labels)):
        ax1.add_patch(patches.Rectangle((i, i), 1, 1, facecolor = "lightgray", linewidth = 0.65, edgecolor = 'white', zorder = 4)) 

    for i in range(8):
        for j in range(8):
            win_prob = cards_data[0, i, j]
            draw_prob = cards_data[1, i, j]
            text = f"{win_prob * 100:.0f} ({draw_prob * 100:.0f})"
            text_color = 'white' if win_prob > 0.5 else 'black' # If win prob is > 50%, use white text
            # 0.5 is half of the cell size
            ax1.text(j + 0.5, i + 0.5, text, ha = 'center', va = 'center', color = text_color)

    plt.title(f"Penney's Game Probabilities for P2 \n Win (Draw) by Cards \n N = {n_decks}")
    plt.xlabel("Player 2 Sequence")
    plt.ylabel("Player 1 Sequence")
    plt.tight_layout()

    # Saves as a PNG with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = os.path.join('heatmaps', f"cards_{output_file}_{timestamp}.png")
    plt.savefig(file_path)
    print(f"Saved heatmap as cards_{output_file}_{timestamp}.png")
    plt.clf()

    # For tricks heatmap
    plt.figure(figsize = (12, 8))
    ax2 = sns.heatmap(tricks_data[0] * 100, annot = False, cmap = 'Blues',
                xticklabels = ax_labels, yticklabels = ax_labels, cbar = False, 
                linewidths = 0.65, linecolor = 'white', square = True,
                cbar_kws = {'label': 'Player 2 Win Probability'})

    # Creates a rectangle with length and width = 1 for each cell
    for i in range(len(ax_labels)):
        ax2.add_patch(patches.Rectangle((i, i), 1, 1, facecolor = "lightgray", linewidth = 0.65, edgecolor = 'white', zorder= 4 ))

    for i in range(8):
        for j in range(8):
            win_prob = tricks_data[0, i, j]
            draw_prob = tricks_data[1, i, j]
            text = f"{win_prob * 100:.0f} ({draw_prob * 100:.0f})"
            text_color = 'white' if win_prob > 0.5 else 'black' # If win prob is > 50%, use white text
            # 0.5 is half of the cell size
            ax2.text(j + 0.5, i + 0.5, text, ha = 'center', va = 'center', color = text_color)

    plt.title(f"Penney's Game Probabilities for P2 \n Win (Draw) by Tricks \n N = {n_decks}")
    plt.xlabel("Player 2 Sequence")
    plt.ylabel("Player 1 Sequence")
    plt.tight_layout()

    # Saves as a PNG with timestamp
    timestamp2 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path2 = os.path.join('heatmaps', f"tricks_{output_file}_{timestamp2}.png")
    plt.savefig(file_path2)
    print(f"Saved heatmap as tricks_{output_file}_{timestamp2}.png")
    plt.clf()

def generate_initial_heatmaps(n_decks):
    """
    Generate the cards/tricks heatmaps for initial_num_decks

    Args: 
        n_decks (int): The number of decks
    Returns:
        None
    """
    # Calculate the win probabilities for the initial number of decks
    results = calculate_win_probabilities(n_decks = n_decks)

    # Define all possible sequences of length 3 ('B' or 'R')
    sequence_list = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']

    # Initialize 3D arrays with cards/tricks probabilities
    cards_data = np.zeros((2, 8, 8))  
    tricks_data = np.zeros((2, 8, 8))  

    # Populate the heatmaps with results
    for i, seq1 in enumerate(sequence_list):
        for j, seq2 in enumerate(sequence_list):
            result = results.get((seq1, seq2))
            if result:
                # Extract the cards and tricks results
                cards_result = result.get('cards', {}) # Empty dictionary is default
                tricks_result = result.get('tricks', {})
                
                if 'win' in cards_result:
                    cards_data[0, i, j] = cards_result['win']
                    cards_data[1, i, j] = cards_result['draw']
                
                if 'win' in tricks_result:
                    tricks_data[0, i, j] = tricks_result['win']
                    tricks_data[1, i, j] = tricks_result['draw']

    # Save the data as .npy files -> probability_data folder
    if not os.path.exists('probability_data'):
        os.makedirs('probability_data')  

    np.save(initial_cards_data, cards_data)
    np.save(initial_tricks_data, tricks_data)

    # Create and save the heatmaps as PNGs
    create_heatmaps(cards_data, tricks_data, output_file = f"{initial_num_decks}_decks", 
                    n_decks = n_decks)

def fill_heatmaps(seed: int,
                  n_decks: int, 
                  augment_decks: int, 
                  output_file: str = 'penney_heatmaps'
                  ) -> None:
    """
    Populate the heatmaps for Penney's game simulation

    Args:
        seed (int): The random seed
        n_decks (int): The number of decks
        augment_decks (int): The number of additional decks to augment
        output_file (str): The base name for the file containing the heatmaps

    Returns:
        None
    """
    # Load the intial win probability data
    try:
        cards_data = np.load(initial_cards_data)
        tricks_data = np.load(initial_tricks_data)
    # Raise an error if the initial data is not found
    except FileNotFoundError as e:
        print(f"Error loading heatmap data: {e}")
        return

    # Augment data if desired
    augment = augment_decks > 0
    if augment:
        store_decks(n_decks=augment_decks, seed=seed, filename="penneydecks.npy", augment=True)
        results = calculate_win_probabilities(n_decks = augment_decks)
        sequence_list = ['BBB', 'BBR', 'BRB', 'BRR', 'RBB', 'RBR', 'RRB', 'RRR']

    # Fill the heatmaps with game outcomes
        for i, seq1 in enumerate(sequence_list):
            for j, seq2 in enumerate(sequence_list):
                result = results.get((seq1, seq2))
            # Check if result (win probability) exists
                if result is not None:
                    # Break down into tricks and cards results
                    tricks_result = result.get('tricks', {})
                    cards_result = result.get('cards', {}) 

                # If player 2 wins in both tricks and cards
                if 'win' in tricks_result and 'win' in cards_result:
                        # Update the heatmaps with the new probabilities
                        total_decks = n_decks + augment_decks
                        # Calculate the average probabilities for the augmented decks (given same weight as initial decks)
                        tricks_data[0, i, j] = (tricks_data[0, i, j] * n_decks + tricks_result['win'] * augment_decks) / (total_decks) 
                        tricks_data[1, i, j] = (tricks_data[1, i, j] * n_decks + tricks_result['draw'] * augment_decks) / (total_decks) 
                        cards_data[0, i, j] = (cards_data[0, i, j] * n_decks + cards_result['win'] * augment_decks) / (total_decks) 
                        cards_data[1, i, j] = (cards_data[1, i, j] * n_decks + cards_result['draw'] * augment_decks) / (total_decks) 
    
    # Save the augmented data as .npy files
    augmented_cards_data = f'probability_data/cards_{total_decks}_decks_augmented.npy'
    augmented_tricks_data = f'probability_data/tricks_{total_decks}_decks_augmented.npy'

    np.save(augmented_cards_data, cards_data)
    np.save(augmented_tricks_data, tricks_data)

    # Save the heatmaps
    create_heatmaps(cards_data, tricks_data, output_file, n_decks + augment_decks)

if __name__ == "__main__":
    # Actually generate the heatmaps for the initial number of decks
    generate_initial_heatmaps(n_decks = initial_num_decks)