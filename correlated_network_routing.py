import numpy as np
import pickle
from network_game.network_fcns import*


class NetworkGame():
    def __init__(self, action_profiles, u_offset):
        SiouxNetwork, self.SiouxNetwork_data = Create_Network()
        OD_demands = pandas.read_csv("network_game/SiouxFallsNet/SiouxFalls_OD_matrix.txt", header=None)
        OD_demands = OD_demands.values
        self.Strategy_vectors, OD_pairs = Compute_Strategy_vectors(OD_demands, self.SiouxNetwork_data.Freeflowtimes, SiouxNetwork,
                                                              self.SiouxNetwork_data.Edges)
        self.N = len(self.Strategy_vectors)  # number of agents in the network
        self.available_action_profiles = action_profiles
        self.u_offset = u_offset
        self.victim_player = 4

    def play(self, distribution):
        sample = np.random.choice(np.size(distribution), p=distribution)
        action = self.available_action_profiles[sample]
        action = np.int_(action)
        loss = Compute_traveltimes(self.SiouxNetwork_data, self.Strategy_vectors, action, 'all')
        utility = (-loss[self.victim_player] - self.u_offset)/1000
        total_occupancies = np.sum([ self.Strategy_vectors[i][action[i]] for i in range(self.N)])
        congestions = 0.15 * np.power(np.divide(total_occupancies, np.array(self.SiouxNetwork_data.Capacities)), 4)
        return utility, loss[self.victim_player], np.mean(congestions)

