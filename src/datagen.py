import numpy as np
import os
from src.helpers import PATH_DATA

HALF_DECK_SIZE = 26

def get_decks(n_decks: int,
              seed: int, 
              half_deck_size: int = HALF_DECK_SIZE 
              ) -> tuple[np.ndarray, np.ndarray]:
    """
    Efficiently generate 'n_decks' shuffled decks using NumPy

    Args:
        n_decks (int): The number of decks to generate
        seed (int): The seed for the random number generator
        half_deck_size (int): The number of cards in half a deck (26)
    
    Returns:
        decks (np.ndarray): 2D array of shape (n_decks, num_cards), 
        where each row is a shuffled deck
    """
    init_deck = [0]*half_deck_size + [1]*half_deck_size
    decks = np.tile(init_deck, (n_decks, 1))
    rng = np.random.default_rng(seed)
    rng.permuted(decks, axis=1, out=decks)
    return decks

def store_decks(n_decks: int, seed: int, filename: str = 'penneydecks.npy', augment: bool = False) -> tuple[np.ndarray, int]:
    """
    Store and/or load the shuffled decks in a NumPy file

    Args:
        n_decks (int): The number of decks to generate
        seed (int): The seed for the random number generator
        filename (str): The name of the file thats stores the decks
        augment (bool): Option to augment the data

    Returns:
        decks (np.ndarray): 2D array of shape (n_decks, num_cards), 
        where each row is a shuffled deck
        seed (int): The seed used to generate the shuffled decks
    """
    decks_file = os.path.join(PATH_DATA, filename)
    os.makedirs(PATH_DATA, exist_ok=True)

    if os.path.exists(decks_file):
        data = np.load(decks_file, allow_pickle=True).item()
        existing_decks = data['decks']
        current_seed = data['seed']
    
        if augment:
            additional_decks = get_decks(n_decks, seed=current_seed)
            updated_decks = np.concatenate((existing_decks, additional_decks), axis=0)
            data['decks'] = updated_decks 
            np.save(decks_file, data)
            return updated_decks, current_seed
        else:
            return existing_decks, current_seed
    else:
        decks = get_decks(n_decks, seed=seed)
        data = {'decks': decks, 'seed': seed}
        np.save(decks_file, data)
        return decks, seed

def augmenting_decks(n_decks: int, augment_decks: int, seed: int, augment: bool) -> tuple:
    """
    Handles the logic for augmenting decks if required, moving logic from visualization.py
    to datagen.py.

    Args:
        n_decks (int): The number of decks 
        augment_decks (int): The number of additional decks 
        seed (int): The random seed
        augment (bool): Whether augementing 

    Returns:
        decks (np.ndarray): The augmented decks
        seed (int): The seed used
    """
    if augment and augment_decks > 0:
        decks, seed = store_decks(n_decks + augment_decks, seed, augment=True)
    else:
        decks, seed = store_decks(n_decks, seed, augment=False)
    return decks, seed