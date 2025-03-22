from visualization import fill_heatmaps
fill_heatmaps(seed=42, n_decks=500_000, augment_decks=10_000)
"""
Generates the heatmaps by calling the fill_heatmaps function 
from visualization.py

Args:
    seed (int): The seed for generating the decks
    n_decks (int): The number of decks
    augment_decks (int): The number of additional decks to augment with
    
Returns: 
    None
"""