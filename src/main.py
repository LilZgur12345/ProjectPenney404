import numpy as np
# Import the initial number of decks
from visualization import fill_heatmaps, initial_num_decks  

# Number of additional decks to augment with
seed = 43
augment_decks = 100
total_decks = initial_num_decks + augment_decks
output_file = f'{total_decks}_decks_augmented'

# Create the new heatmaps
fill_heatmaps(seed = seed, n_decks = total_decks, 
              augment_decks = augment_decks, output_file = output_file)
"""
Generate the augmented heatmaps by calling the fill_heatmaps function 
from visualization.py

Args:
    seed (int): The random seed
    n_decks (int): The number of initial decks
    augment_decks (int): The number of additional decks to augment
    output_file (str): The name for the file containing the new heatmaps

Returns: 
    None
"""
