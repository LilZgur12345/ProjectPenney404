# Project Penney: Overview

Penney's Game, named after Walter Penney, involves two players choosing a sequence of three cards - either black or red. There are two methods of scoring, one based on tricks (whoever's sequence appears first) and the other based on total cards (total number of appearences). The probabilities of player 2 winnning for all 64 possible games are presented in two heatmaps. 

The goal of this project is to compute the probability of winning/losing/drawing for player 2 while also visualizing these results in a clear and effective manner. Player 2 has an advantage due to their ability to know player 1's sequence before choosing their own. With the information in the heatmaps, player 2 can achieve the highest probability of winning Penney's Game.


# Quick Start Guide:

To view the probabilities and heatmaps, no setup is necessary. However, uv and the required libraries must be installed for the code to work. To augment the existing data, the 'augment' boolean can be set to True and 'augment_decks' can be assigned a quantity. The number of decks can be altered to easily debug/test things. Run the files in the following order to prevent NameError or ImportError. Visualization.py creates two pngs called totals_penney_game and tricks_penney_game. For reference, the heatmaps produced with 100,000 decks and an augmentation of 1,000 decks are also included in the GitHub main.

First, clone the repository and then run the following code in a new module with the desired number of decks/augmentation:

from visualization import fill_heatmaps
fill_heatmaps(seed=42, n_decks=100000, augment_decks=1000)


# Files Included:

`src/`

- datagen.py: Code related to data generation and storage of the decks in an npy file.

- helpers.py: The helper function debugger_factory and PATH_DATA, which are needed and imported across various other modules.

- processing.py: Code related to scoring the games, both by tricks and totals.

- visualization.py: Code related to creating two heatmaps, both of which utilize a blue color gradient and present the probabilities with one decimal point.

---

This project is maintained using the [uv package manager](https://docs.astral.sh/uv/).


 
