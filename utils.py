import numpy as np


def tau_computation(pi, u, theta):
    exp_vector = np.exp(-(u*theta))
    temp = pi*exp_vector
    s = np.sum(temp)
    b_theta = np.log(s)
    tau = temp/s
    d_kl = np.sum((-(u*theta))*tau)-b_theta
    util = np.sum(tau*u)
    return d_kl, util, tau


def kl_compute(pi,tau):
    d_kl = np.sum(np.log(tau / pi) * tau)
    return d_kl


def utility_computation(tau,u):
    util = np.sum(tau*u)
    return util


def theta_min_ind(u_pi,epsilon, u_list):
    u_theta = u_pi - epsilon
    for i, u in enumerate(u_list):
        if u <= u_theta:
            break
    return i

