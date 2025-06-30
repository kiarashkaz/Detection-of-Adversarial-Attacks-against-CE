import numpy as np
import matplotlib.pyplot as plt
from utils import *
from detector import GenCususm
import pickle
from correlated_network_routing import NetworkGame


class Runner:
    def __init__(self, game, max_episode_length=10000, n_episode=1000, nu=1):
        self.game= game
        if game == "network_game":
            file = open("network_game\Stored_computations\correlated_play_player_4.pckl",
                        'rb')
            data = pickle.load(file)
            file.close()
            utilities = np.array(data[0])/1000
            pi = np.array(data[1])
            action_profiles = data[2]
            u_offset = data[3]
            self.network_game = NetworkGame(action_profiles, u_offset)
            self.theta_range = np.arange(-2, 1, 0.01)
        else:
            utilities = np.array([6, 9, 1, 5, 3, 7])
            pi = np.array([1 / 36, 1 / 3, 1 / 36, 1 / 36, 1 / 3, 1 / 4])
            self.theta_range = np.arange(-2, 1, 0.01)

        self.u = utilities
        self.pi = pi
        self.Max_episode_length = max_episode_length
        self.N_episode = n_episode
        self.nu = nu
        self.theta_list, self.kl_list, self.u_list = self.look_up_tables()

    def look_up_tables(self):
        theta_exponent_list = self.theta_range
        theta_list = 10 ** theta_exponent_list

        kl_list = np.zeros(theta_list.shape)
        u_list = np.zeros(theta_list.shape)

        for i, th in enumerate(theta_list):
            d_kl, util, tau = tau_computation(self.pi, self.u, th)
            kl_list[i] = d_kl
            u_list[i] = util
        return theta_list, kl_list, u_list

    def run(self, gamma, epsilon, adv_theta_offset=0, attack=True, attack_dist=None):

        u_pi = np.sum(self.u*self.pi)

        ind = theta_min_ind(u_pi, epsilon, self.u_list)
        theta_min = self.theta_list[ind]
        d_theta_min = self.kl_list[ind]

        theta_set = self.theta_list[ind:]
        kl_set = self.kl_list[ind:]
        u_set = self.u_list[ind:]

        mu = np.log(3*(d_theta_min+1)**2) - np.log(np.log(gamma)) + np.log(gamma)

        adv_theta = theta_min + adv_theta_offset
        if attack_dist is None:
            adv_kl, adv_u, tau_adv = tau_computation(self.pi, self.u, adv_theta)
        else:
            tau_adv = attack_dist
            adv_u = utility_computation(tau_adv, self.u)
            adv_kl = kl_compute(self.pi, tau_adv)

        stopping_time = GenCususm(mu, theta_set, kl_set, u_set)
        dist = self.pi
        total_u = np.zeros(self.N_episode)
        t_stop = np.zeros(self.N_episode)
        total_loss = np.zeros(self.N_episode)
        total_congestion = np.zeros(self.N_episode)
        for ep in range(self.N_episode):
            print("episode:{}".format(ep))
            for t in range (self.Max_episode_length):
                if t >= self.nu-1:
                    dist = tau_adv if attack is True else self.pi
                if self.game == "network_game":
                    U_t, loss, congestions = self.network_game.play(dist)
                    total_loss[ep] += loss
                    total_congestion[ep] += congestions
                else:
                    U_t = np.random.choice(self.u, p=dist)
                stop = stopping_time.stopping_rule(U_t)
                total_u[ep] += U_t
                if stop:
                    break
            t_stop[ep] = t+1

        out_dict = {"gamma":gamma, "adv_theta": adv_theta, "adv_kl": adv_kl, "adv_expected_u": adv_u,
                    "total_utility": np.mean(total_u), "t_stop": np.mean(t_stop), "average_u":  np.mean(total_u/t_stop),
                    "average congestion": np.mean(total_congestion/t_stop),
                    "average_loss": np.mean(total_loss/t_stop)}

        return out_dict





#plt.figure(1)
#plt.plot(theta_set, kl_set)
#plt.grid()
#plt.figure(2)
#plt.plot(theta_set, u_set)
#plt.grid()
#plt.show()