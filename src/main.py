import numpy as np
from datagen import store_decks
# Import the initial number of decks
from visualization import fill_heatmaps, initial_num_decks  

# Number of additional decks to augment with
seed = 42
augment_decks = 100

# Store the decks before augmenting
augmented_decks, current_seed = store_decks(n_decks = augment_decks, seed = seed, filename = "penneydecks.npy", augment = True)

# Augment/update the heatmaps with the additional decks
total_decks = initial_num_decks + augment_decks
output_file = f"{total_decks}_decks_augmented"

fill_heatmaps(seed = current_seed, n_decks = initial_num_decks, augment_decks = augment_decks, output_file = output_file)
"""
Generate the augmented heatmaps by calling the fill_heatmaps function 
from visualization.py

Args:
    seed (int): The random seed
    n_decks (int): The number of initial decks
    augment_decks (int): The number of additional decks to augment
    output_file (str): The name for the file containing the heatmaps

Returns: 
    None
"""
