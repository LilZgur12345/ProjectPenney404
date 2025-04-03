import numpy as np
# Import the initial number of decks
from visualization import fill_heatmaps, initial_num_decks  

# Number of additional decks to augment with
seed = 43
augment_decks = 100_000
total_decks = initial_num_decks + augment_decks
output_file = f'{total_decks}_decks_augmented'

# Create the new heatmaps
fill_heatmaps(seed = seed, n_decks = initial_num_decks, 
              augment_decks = augment_decks, output_file = output_file)


augment_decks_again = 10  # Example: augmenting again with 200 more decks
new_total_decks = total_decks + augment_decks_again  # Update total decks after the second augmentation
output_file_again = f'{new_total_decks}_decks_augmented'

# Create the new heatmaps for the second augmentation
fill_heatmaps(seed = seed, n_decks = total_decks,  # Set n_decks to total_decks from the first augmentation
              augment_decks = augment_decks_again, output_file = output_file_again)
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
