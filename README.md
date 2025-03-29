# Project Penney: Overview

This project simulates Penney's Game, named after Walter Penney, and involves two players choosing a sequence of three cards - either black or red. There are two methods of scoring, one based on tricks (whoever's sequence appears first) & the other based on total cards (total number of appearences). The probabilities of player 2 winnning for all 56 possible games are presented in the two heatmaps. 

The goal of this project is to compute the probability of winning/losing/drawing for player 2 while also visualizing these results in a clear & effective manner. Player 2 has an advantage due to their ability to know player 1's sequence before choosing their own. With the information in the heatmaps, player 2 can achieve the highest probability of winning Penney's Game. More information about the game can be found here: [Wikipedia](https://en.wikipedia.org/wiki/Penney%27s_game).


# Quick Start Guide:

To view the probabilities & heatmaps, no setup is necessary. However, uv & the required libraries must be installed for the code to work. Run the files in the following order to prevent NameError or ImportError. The initial number of decks can be altered to easily debug & test things in visualization.py, which creates two PNGs called cards_1000000_decks & tricks_1000000_decks with timestamps. For reference, the heatmaps produced with 1,000,000 decks & no augmentation are included in the heatmaps folder of the GitHub main directory. 

To augment this existing data, first clone the repository. Run main.py after editing the following code (seed & augment_decks variables) to achieve the desired total number of decks/augmentation:

```python
seed = 42
augment_decks = 100
fill_heatmaps(seed = current_seed, n_decks = initial_num_decks, 
              augment_decks = augment_decks, output_file = output_file)

```

# Files Included:

`src/`

- datagen.py: Code related to data generation & augmentation/storage of the decks in an npy file.

- helpers.py: The helper function debugger_factory & PATH_DATA, which are needed & imported across various other modules.

- processing.py: Code related to scoring the games, both by tricks & cards.

- visualization.py: Code related to creating the initial & augmented heatmaps, both of which utilize a blue color gradient & present the win/draw probabilities rounded to the nearest whole number.

- main.py: Code to actually run the simulation & augment the existing data.

---

This project is maintained using the [uv package manager](https://docs.astral.sh/uv/).


 
