import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datagen import store_decks
from all_64 import calculate_win_probabilities  # Changed from scoring to all_64

def all_possible_sequences(length: int) -> list:
    # Generate all possible binary sequences of a given length
    return [''.join(map(str, format(i, f'0{length}b'))) for i in range(2**length)]

def create_heatmaps(heatmap_total, heatmap_tricks, all_seq, output_file, n_decks):
    """Generate and save the heatmaps for total cards and tricks win probabilities."""
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_total, annot=True, fmt=".2f", cmap="Blues",
                xticklabels=all_seq, yticklabels=all_seq,
                cbar_kws={'label': 'Player 2 Win Probability (Total Cards)'})
    plt.title(f"Penney's Game Heatmap [Total Cards] - {n_decks} Decks")
    plt.xlabel("Player 2 Sequence")
    plt.ylabel("Player 1 Sequence")
    plt.tight_layout()
    plt.savefig(f"totals_{output_file}.png")
    print(f"Saved totals heatmap as totals_{output_file}.png")
    plt.clf()

    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_tricks, annot=True, fmt=".2f", cmap="Blues",
                xticklabels=all_seq, yticklabels=all_seq,
                cbar_kws={'label': 'Player 2 Win Probability (Tricks)'})
    plt.title(f"Penney's Game Heatmap [Tricks] - {n_decks} Decks")
    plt.xlabel("Player 2 Sequence")
    plt.ylabel("Player 1 Sequence")
    plt.tight_layout()
    plt.savefig(f"tricks_{output_file}.png")
    print(f"Saved tricks heatmap as tricks_{output_file}.png")
    plt.clf()

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

    # Calculate win probabilities for all sequence pairs
    results = calculate_win_probabilities(num_trials=1000, n_decks=n_decks)

    # Populate the heatmaps
    for i, seq1 in enumerate(all_sequences):
        for j, seq2 in enumerate(all_sequences):
            # Convert binary sequences to strings of 'B' and 'R'
            p1_seq = ''.join(['B' if bit == '0' else 'R' for bit in seq1])
            p2_seq = ''.join(['B' if bit == '0' else 'R' for bit in seq2])
            
            try:
                result = results[(p1_seq, p2_seq)]  # Access the result directly from the dictionary
            except KeyError:
                print(f"Key not found: {(p1_seq, p2_seq)}")
                continue # Skip to the next iteration

            # Ensure correct result structure
            if isinstance(result, dict) and 'tricks' in result and 'totals' in result:
                tricks_result = result['tricks']
                totals_result = result['totals']

                # Store the probabilities in the respective heatmaps
                heatmap_tricks[i, j] = tricks_result['win']
                heatmap_total[i, j] = totals_result['win']

                # Fill the symmetric positions as well.  Check for player1_win_prob.
                if 'player1_win_prob' in tricks_result and 'player1_win_prob' in totals_result:
                    heatmap_tricks[j, i] = tricks_result['player1_win_prob']
                    heatmap_total[j, i] = totals_result['player1_win_prob']
                else:
                    print("player1_win_prob not found.  Symmetric heatmap value not set.")

            else:
                print(f"Unexpected result structure for {p1_seq} vs {p2_seq}. Result: {result}")

    # Create and save the heatmaps
    create_heatmaps(heatmap_total, heatmap_tricks, all_sequences, output_file, n_decks)

if __name__ == "__main__":
    main()