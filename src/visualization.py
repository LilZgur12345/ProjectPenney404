import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from src.processing import run_simulation
from src.datagen import store_decks

def create_heatmap(decks: np.ndarray, output_file:str) -> None:
    """
    Create a heatmap showing the probabilities of Player 2 winning over Player 1's sequence.
    
    Args:
        decks: np.ndarray, array of shuffled decks.
    """
    all_sequences = ['000', '001', '010', '011', '100', '101', '110', '111'] # 8 possible sequences
    
    # Initialize an 8x8 matrix
    heatmap_data = np.zeros((8, 8))

    # Iterate through & calculate the probabilities
    for i in range(8):
        for j in range(8):
            if i != j:  # Only want different sequence pairs
                p1_seq = all_sequences[i]
                p2_seq = all_sequences[j]
    
                results = run_simulation(decks, p1_seq, p2_seq) # Run simulation 
                
                # Calculate probability of P2 winning
                p2_probability = np.sum(results == 'Player 2 Wins') / len(results)
                
                # Store in matrix
                heatmap_data[i, j] = p2_probability
    
    # Plot the heatmap
    plt.figure(figsize = (12, 8))
    sns.heatmap(heatmap_data, annot = True, fmt = ".2f", cmap="Blues",
                xticklabels = all_sequences, yticklabels = all_sequences, 
                cbar_kws={'label': 'Player 2 Win Probability'})
    plt.title("Penney's Game Heatmap")
    plt.xlabel("Player 2 Sequence")
    plt.ylabel("Player 1 Sequence")
    plt.savefig(output_file)
    plt.show()

def main() -> None:
    # Generate decks with a fixed seed
    seed = 42
    decks, seed = store_decks(10000, seed)
    output_file = 'penney_heatmap.png' # Save png file
    create_heatmap(decks, output_file)

if __name__ == "__main__":
    main()