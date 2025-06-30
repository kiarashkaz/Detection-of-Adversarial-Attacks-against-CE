import numpy as np
import pickle
from matplotlib import pyplot as plt

file = open("network_game\Stored_computations\stored_data_GPMW_version0_run0.pckl", 'rb')

data = pickle.load(file)

file.close()

incurred_losses = data[0]
played_actions = data[1]
addit_Congestions = data[2]
Total_occupancies = data[3]
idxs_controlled = data[4]

victim_player = 4
N_quant = 1000
incurred_losses = np.array(incurred_losses)
played_actions = np.array(played_actions)
player_losses = incurred_losses[:, victim_player]
plt.plot(np.arange(np.size(player_losses)), player_losses)
plt.show()
player_utility_hist = -player_losses
utility_lower_bound = np.min(player_utility_hist)
player_utility_hist = player_utility_hist - utility_lower_bound #Making utilities positive
min_u = np.min(player_utility_hist)
max_u = np.max(player_utility_hist)
quant_step = (max_u - min_u)/N_quant

utility_list = np.zeros(N_quant)
empirical_dist = np.zeros(N_quant)
action_profiles = np.zeros((N_quant, played_actions.shape[1]))
for i in range(np.size(player_utility_hist)):
    quant_element = min(int((player_utility_hist[i] - min_u) / quant_step), N_quant - 1)
    utility_list[quant_element] = quant_element*quant_step + min_u
    empirical_dist[quant_element] += 1
    action_profiles[quant_element, :] = played_actions[i, :]
unused_inds = np.zeros(N_quant, dtype=bool)
for j in range(N_quant):
    if empirical_dist[j] == 0:
        unused_inds[j] = 1
utility_list = np.delete(utility_list, unused_inds)
empirical_dist = np.delete(empirical_dist, unused_inds)
action_profiles = np.delete(action_profiles, unused_inds, 0)

empirical_dist = empirical_dist/np.sum(empirical_dist)

file = open('network_game\Stored_computations\correlated_play_player_{}'.format(idxs_controlled[victim_player]) + '.pckl',
            'wb')
pickle.dump(
    [utility_list, empirical_dist, action_profiles, utility_lower_bound], file)
file.close()

