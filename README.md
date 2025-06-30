# Quickest Detection of Adversarial Attacks Against Correlated Equilibria

# Running Experiments

* ```main_test.py``` is the main script for running an adversarial game. The game is specified using the ```game_name argument```, and the minimum per-step attack budget is set using ```epsilon```. The script outputs two JSON files that summarize the statistics for both the attacked and non-attacked scenarios. ```adv_attack_offset``` determies the the attack parameter (\theta), relative to \theta_min.

* To run an experiment, for example, for DAA (Dynamic Adversary)  with 𝑤=10, 𝛽=−3, and for 100 episodes:

### In SMAC-MMM, run:
```
python main.py --config=qmix --env-config=sc2 with env_args.map_name=MMM test_nepisode=100 attack_type="DAA" thresholds=[-3] tracker_window=[-1,10] adv_load_adr=[Model Address]

```

* For the “no window” case (window=∞), set `tracker_window=[-1]`
* To start the attack at a random time, set `attack_start_t=-1`
* [Model Address] is the address of the attack model in “src/Trained Models/DAA”

## Some Notes:
* The default config file is located in “src/config”. For the OBS attacks, set “attack_type” to “OA”, and set the DAA model to the corresponding DAA file with 𝝀=0 using `adv_load_adr`. (Note that “OA” runs slowly)
* To run an experiment without attack, set `attack_active=False`
* To train a new tracker model, set `attack_active=False` and `tracker_train=True`
* To train a new DAA (dynamic adversary) model for 𝝀=[𝑎,𝑏,𝑐,𝑑], set `adv_test_mode=False` and `lambda_DAA=[a,b,c,d]`

# Reference
Kiarash Kazari, Ezzeldin Shereen, György Dán. "Decentralized Anomaly Detection in Cooperative Multi-Agent Reinforcement Learning". In Proceedings of IJCAI, Aug. 2023
