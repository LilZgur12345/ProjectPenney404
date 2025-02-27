import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datagen import store_decks
from scoring import calculate_win_probabilities  # Correct import for scoring function

def all_possible_sequences(length: int) -> list:
    # Generate all possible binary sequences of a given length
    return [''.join(map(str, format(i, f'0{length}b'))) for i in range(2**length)]

def create_heatmaps(heatmap_total, heatmap_tricks, all_seq, output_file, n_decks):
    # Create total cards heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_total, annot=True, fmt=".2f", cmap="Blues",
                xticklabels=all_seq, yticklabels=all_seq, 
                cbar_kws={'label': 'Player 2 Win Probability (Total Cards)'})
    plt.title(f"Penney's Game Heatmap [Total Cards] - {n_decks} Decks")
    plt.xlabel("Player 2 Sequence")
    plt.ylabel("Player 1 Sequence")
    plt.tight_layout()  # Ensure labels fit inside the plot
    plt.savefig(f"totals_{output_file}.png")  # Save the heatmap
    print(f"Saved totals heatmap as totals_{output_file}.png")
    plt.clf()  # Clear the figure to prepare for the next one

    # Create tricks heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_tricks, annot=True, fmt=".2f", cmap="Blues",
                xticklabels=all_seq, yticklabels=all_seq, 
                cbar_kws={'label': 'Player 2 Win Probability (Tricks)'})
    plt.title(f"Penney's Game Heatmap [Tricks] - {n_decks} Decks")
    plt.xlabel("Player 2 Sequence")
    plt.ylabel("Player 1 Sequence")
    plt.tight_layout()  # Ensure labels fit inside the plot
    plt.savefig(f"tricks_{output_file}.png")  # Save the heatmap
    print(f"Saved tricks heatmap as tricks_{output_file}.png")
    plt.clf()  # Clear the figure for further plots if needed

def main() -> None:
    # Generate decks with a fixed seed
    seed = 42
    n_decks = 1000  # Number of shuffled decks
    decks, seed = store_decks(n_decks, seed)  # Store shuffled decks
    output_file = 'penney_heatmaps'  

    # Define the sequence length (3 in the case of Penney's game)
    seq_length = 3
    
    # Get all possible binary sequences of the given length
    all_sequences = all_possible_sequences(seq_length)

    # Initialize the heatmaps (2D arrays) for storing probabilities
    heatmap_total = np.zeros((len(all_sequences), len(all_sequences)))  # Total cards heatmap
    heatmap_tricks = np.zeros((len(all_sequences), len(all_sequences)))  # Tricks heatmap

    # Get win probabilities for both scoring methods
    results = calculate_win_probabilities(num_trials=1000, n_decks=n_decks)  # Call the function to get results

    # Check the structure of the results
    print(f"Results dictionary keys: {list(results.keys())}")  # This should show 'tricks' and 'totals'

    # Loop through the predefined pairs of sequences (seq1, seq2) that exist in the results
    for (seq1, seq2), outcome in results.items():
        # Access the results for both tricks and totals
        tricks_result = outcome['tricks']
        totals_result = outcome['totals']
        
        # Ensure the sequences match by directly comparing the strings
        if seq1 in all_sequences and seq2 in all_sequences:
            # Find the indices of seq1 and seq2 in the all_sequences list
            i = all_sequences.index(seq1)
            j = all_sequences.index(seq2)
            
            # Store the probabilities in the respective heatmaps
            heatmap_tricks[i, j] = tricks_result['win']  # Get tricks win probability
            heatmap_total[i, j] = totals_result['win']   # Get total cards win probability

    # Create and save the heatmaps
    create_heatmaps(heatmap_total, heatmap_tricks, all_sequences, output_file, n_decks)

if __name__ == "__main__":
    main()