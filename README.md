# Project Penney: Overview

This project simulates Penney's Game, named after Walter Penney, and involves two players choosing a sequence of three cards - either black or red. There are two methods of scoring, one based on tricks (whoever's sequence appears first) & the other based on total cards (total number of appearences). The probabilities of player 2 winnning for all 56 possible games are presented in the two heatmaps. 

The goal of this project is to compute the probability of winning/losing/drawing for player 2 while also visualizing these results in a clear & effective manner. Player 2 has an advantage due to their ability to know player 1's sequence before choosing their own. With the information in the heatmaps, player 2 can achieve the highest probability of winning Penney's Game.


# Quick Start Guide:

To view the probabilities & heatmaps, no setup is necessary. However, uv & the required libraries must be installed for the code to work. To augment the existing data, 'augment_decks' can be assigned a quantity in main.py. The number of decks can also be altered to easily debug/test things. Run the files in the following order to prevent NameError or ImportError. Visualization.py creates two pngs called cards_penney_heatmaps & tricks_penney_heatmaps. For reference, example heatmaps produced with 1,000,000 decks & no augmentation are also included in the heatmaps folder of the GitHub main directory.

First, clone the repository. Run main.py after editing the following code to acheive the desired number of decks/augmentation:

```python
from visualization import fill_heatmaps
fill_heatmaps(seed=42, n_decks=500_000, augment_decks=10_000)
```

# Files Included:

`src/`

- datagen.py: Code related to data generation & augmentation/storage of the decks in an npy file.

- helpers.py: The helper function debugger_factory & PATH_DATA, which are needed & imported across various other modules.

- processing.py: Code related to scoring the games, both by tricks & cards.

- visualization.py: Code related to creating two heatmaps, both of which utilize a blue color gradient & present the win/draw probabilities rounded to the nearest whole number.

- main.py: Code to actually run the simulations.

---

This project is maintained using the [uv package manager](https://docs.astral.sh/uv/).


 
