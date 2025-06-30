from repeated_game_runner import *
import json

game_name = "toy_example"  # "toy_example" or "network_game"


epsilon = 0.5

no_attack_results = {"gamma": [], "total_utility": [], "t_stop": [], "average_u": [],
                     "average congestion": [], "average_loss": []}
attack_results = {"gamma": [], "total_utility": [], "t_stop": [], "average_u": [],
                  "adv_theta": [], "adv_kl": [], "adv_expected_u": [], "average congestion": [],
                  "average_loss": []}

runner = Runner(game_name)

adv_attack_offset_list = [0]  # adversary's theta = theta min + offset
gamma_exponent_list = np.arange(3, 5.4, 0.33)  # list of gamma values (1/alpha) to be tested in log domain
#np.random.seed(7)
#random_dist=np.random.random_sample(6)
#random_dist = random_dist/np.sum(random_dist)


for gamma_exponent in gamma_exponent_list:
    gamma = 10 ** gamma_exponent
    no_attack_out = runner.run(gamma, epsilon, attack=False)
    for k in no_attack_results:
        no_attack_results[k].append(no_attack_out[k])
    for offset in adv_attack_offset_list:
        attack_out = runner.run(gamma, epsilon, offset, attack=True)  #, attack_dist=random_dist
        for k in attack_results:
            attack_results[k].append(attack_out[k])

name_1 = "{}_no_attack_epsilon_{}".format(game_name, epsilon)
with open(name_1+".json", 'w') as fp1:
    json.dump(no_attack_results, fp1, indent=4)

name_2 = "{}_attack_epsilon_{}".format(game_name, epsilon)
with open(name_2+".json", 'w') as fp2:
    json.dump(attack_results, fp2, indent=4)

