# Quickest Detection of Adversarial Attacks Against Correlated Equilibria

# Running Experiments

* ```main_test.py``` is the main script for running an adversarial game. The game is specified using the ```game_name argument```, and the minimum per-step attack budget is set using ```epsilon```. The script outputs two JSON files that summarize the statistics for both the attacked and non-attacked scenarios. ```adv_attack_offset``` determies the the attack parameter (θ) relative to θ_min.

* To evaluate a different victim agent in the routing game, first, run ```roting_dist_finder.py``` with the ```victim_player``` parameter set to x, where x is the desired player number. This will generate ```correlated_play_player_x.pckl```, which can then be used in ```repeated_game_runner.py```. 

# Reference
K. Kazari, A. Kanellopoulos, and G. Dán, “Quickest Detection of Adversarial Attacks Against Correlated Equilibria”, AAAI, Apr. 2025. 
