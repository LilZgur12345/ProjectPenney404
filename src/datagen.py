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
    # Generate the initial deck with 0's and 1's
    init_deck = [0] * half_deck_size + [1] * half_deck_size
    decks = np.tile(init_deck, (n_decks, 1))
    # Shuffle the decks using a random number generator
    rng = np.random.default_rng(seed)
    # Use permutation function to fill the decks with shuffled cards
    rng.permuted(decks, axis = 1, out = decks)
    return decks

def store_decks(n_decks: int, 
                seed: int, 
                filename: str = 'penneydecks.npy', 
                augment: bool = False
                ) -> tuple[np.ndarray, int]:
    """
    Store and/or load the shuffled decks in a NumPy file

    Args:
        n_decks (int): The number of decks to generate
        seed (int): The random seed
        filename (str): The name of the file thats stores the decks
        augment (bool): Option to augment the data

    Returns:
        decks (np.ndarray): 2D array of shape (n_decks, num_cards), 
        where each row is a shuffled deck
        seed (int): The seed used to generate the shuffled decks
    """
    # Specify the path for decks_file
    decks_file = os.path.join(PATH_DATA, filename)
    os.makedirs(PATH_DATA, exist_ok=True)

    # Check if the file already exists
    if os.path.exists(decks_file):
        data = np.load(decks_file, allow_pickle = True).item() 
        # Load decks/seeds from the file
        existing_decks = data['decks']
        current_seed = data['seed']

        # If choosing to augment with additional decks
        if augment:
            additional_decks = get_decks(n_decks, seed = current_seed + 1)
            # Append new decks to existing decks
            updated_decks = np.concatenate((existing_decks, additional_decks), axis = 0)
            # Update data with new decks and save
            data['decks'] = updated_decks 
            data['seed'] = current_seed + 1
            np.save(decks_file, data)
            return updated_decks, current_seed + 1
        else:
            return existing_decks, current_seed
    # If the file does not exist, generate the decks
    else:
        decks = get_decks(n_decks, seed = seed)
        data = {'decks': decks, 'seed': seed}
        # Save the decks/seeds
        np.save(decks_file, data)
        return decks, seed

def augmenting_decks(n_decks: int, 
                     augment_decks: int, 
                     seed: int, 
                     augment: bool
                     ) -> np.ndarray:
    """
    Carry out augmentation with additional decks

    Args:
        n_decks (int): The number of decks 
        augment_decks (int): The number of additional decks to augment
        seed (int): The random seed
        augment (bool): Whether augementing or not

    Returns:
        decks (np.ndarray): The augmented decks
        seed (int): The seed used to generate the shuffled decks
    """
    if augment:
        # Augment the decks with the specified number (augment_decks)
        new_decks = get_decks(n_decks = augment_decks, seed = seed)
        return new_decks
    else:
        # Do not augment the decks
        return get_decks(n_decks = n_decks, seed = seed)