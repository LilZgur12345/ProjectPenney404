import numpy as np
import os
from src.helpers import PATH_DATA

def store_results(results: np.ndarray, filename: str = 'penneyresults.npy') -> None:
    results_file = os.path.join(PATH_DATA, filename)
    os.makedirs(PATH_DATA, exist_ok=True)

    if os.path.exists(results_file):
        data = np.load(results_file, allow_pickle = True).item()
        if 'results' in data:
            data['results'] = np.append(data['results'], results)
        else:
            data['results'] = results
        np.save(results_file, data)

    else:
        data = {'results': results}
        np.save(results_file, data)