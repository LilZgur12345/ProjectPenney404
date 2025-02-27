import numpy as np
import os
from src.helpers import PATH_DATA

HALF_DECK_SIZE = 26

def get_decks(n_decks: int,
              seed: int, 
              half_deck_size: int = HALF_DECK_SIZE 
              ) -> tuple[np.ndarray, np.ndarray]:
    """
    Efficiently generate `n_decks` shuffled decks using NumPy.
    
    Returns:
        decks (np.ndarray): 2D array of shape (n_decks, num_cards), 
        each row is a shuffled deck.
    """
    init_deck = [0]*half_deck_size + [1]*half_deck_size
    decks = np.tile(init_deck, (n_decks, 1))
    rng = np.random.default_rng(seed)
    rng.permuted(decks, axis=1, out=decks)
    return decks

def store_decks(n_decks: int, seed: int, filename: str = 'penneydecks.npy', augment: bool = False) -> tuple[np.ndarray, int]:
   # Joining the paths of filename and PATH_DATA directory
    decks_file = os.path.join(PATH_DATA, filename)
    os.makedirs(PATH_DATA, exist_ok=True)

    # Check if file penneydecks.npy exists
    if os.path.exists(decks_file):
        # Loads the file as a dictionary
        data = np.load(decks_file, allow_pickle = True).item()
        # Return the decks and seed from file
        existing_decks = data['decks']
        current_seed = data['seed']
    
        if augment: # If augmenting the decks
            additional_decks = get_decks(n_decks, seed = current_seed)
            updated_decks = np.concatenate((existing_decks, additional_decks), axis=0)
            data['decks'] = updated_decks  # Update the decks in the data dictionary
            np.save(decks_file, data)  # Save the updated decks
            return updated_decks, current_seed
        else:
            return existing_decks, current_seed
    else:
        # If not, create the decks and seed using get_decks
        decks = get_decks(n_decks, seed=seed)
        data = {'decks': decks, 'seed': seed}
        # Save and return the decks and seed
        np.save(decks_file, data)
        return decks, seed