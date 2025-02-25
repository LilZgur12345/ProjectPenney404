import matplotlib.pyplot as plt
import seaborn as sns
from src.helpers import PATH_DATA
from src.processing import score_game
from src.store import store_results
import numpy as np

def create_heatmap(decks: np.ndarray, p1_seq:str, p2_seq:str):
    #Create a list of results
    results = score_game(decks, p1_seq, p2_seq)
    #Reshape the results into a 2D array
    result_counts = np.unique(results, return_counts=True)
    result_counts = np.reshape(result_counts[1], (1, -1))

    plt.figure(figsize=(10, 8))
    sns.heatmap(result_counts, annot=True, fmt="d", cmap="YlGnBu", xticklabels=result_counts, yticklabels=["Counts"])
    plt.title("Heatmap of Game Results")
    plt.xlabel("Result")
    plt.ylabel("Count")
    plt.show()
    
    # Store the results
    store_results(results)


    if __name__ == "__main__":
    # Define your sequences for Player 1 and Player 2
        seq1 = "010"  # Example sequence for player 1
        seq2 = "001"  # Example sequence for player 2

    # Load the decks (make sure they are pre-generated or generated on demand)
    decks, seed = store_results(100000, 42)

    # Generate the heatmap
    create_heatmap(decks, seq1, seq2)

