import numpy as np


class GenCususm:
    def __init__(self, mu, theta_set, kl_set, u_set):
        self.mu = mu
        self.theta_set = theta_set
        self.kl_set = kl_set
        self.u_set = u_set
        self.theta_min = self.theta_set[0]
        self.thresholds = self.threshold_calc()
        self.M = np.size(self.thresholds)
        self.b_theta_min = - self.theta_min*self.u_set[0]-self.kl_set[0]
        self.Q = np.zeros(self.M)
        self.cycle_t = 1
        self.Cusum_R = 0

    def threshold_calc(self):
        t=1
        threshold_kls = []
        threshold_thetas = []
        threshold_u = []
        cursor = np.size(self.theta_set)-1
        while True:
            if t*self.kl_set[cursor] > self.mu:
                while cursor >= 0:
                    cursor -= 1
                    if t*self.kl_set[cursor] <= self.mu:
                        threshold_kls.append(self.kl_set[cursor])
                        threshold_thetas.append(self.theta_set[cursor])
                        threshold_u.append(self.u_set[cursor])
                        break
            else:
                threshold_kls.append(self.kl_set[cursor])
                threshold_thetas.append(self.theta_set[cursor])
                threshold_u.append(self.u_set[cursor])
            t += 1
            if cursor == 0:
                break
        b = -np.array(threshold_thetas)*np.array(threshold_u)-np.array(threshold_kls)
        k = np.arange(1, t)
        thresholds = (self.mu+ k*b)/threshold_thetas
        return thresholds

    def stopping_rule(self, new_u):
        S = self.Cusum_R - self.theta_min*new_u - self.b_theta_min
        if S>0:
            self.Cusum_R = S
            if self.Cusum_R > self.mu:
                self.Cusum_R = 0
                self.Q = np.zeros(self.M)
                self.cycle_t = 1
                return True
        else:
            self.Cusum_R = 0
            self.Q = np.zeros(self.M)
            self.cycle_t = 1
            return False
        self.Q = np.roll(self.Q, 1)
        self.Q[0] = 0
        self.Q[0:self.cycle_t] -= new_u
        tests = np.multiply((self.Q[0:self.cycle_t] > self.thresholds[0:self.cycle_t]), 1)
        if self.cycle_t < self.M:
            self.cycle_t += 1
        if np.sum(tests) > 0.5:
            self.Cusum_R = 0
            self.Q = np.zeros(self.M)
            self.cycle_t = 1
            return True


