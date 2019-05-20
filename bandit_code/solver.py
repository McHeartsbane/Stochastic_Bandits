from __future__ import division

from typing import Type

from bandit_code.environment import bernoulli_env
import numpy as np

from bandit_code.environment import BernoulliEnv


class Solver(object):
    def __init__(self, bernoulli_env: Type[BernoulliEnv] = bernoulli_env):
        """The target Environment (env) to solve."""

        # The environment.py initialization
        self.bernoulli_env = bernoulli_env

        # To count the number of times each arm is selected, let's create an empty vector at the size of number of arms
        self.counts = np.zeros(shape=self.bernoulli_env.N_arm)

    def run(self, num_steps):
        for _ in range(num_steps):
            self.run_one_step()


class EpsilonGreedy(Solver):
    def __init__(self, eps):
        # Running env from the parent class
        super(EpsilonGreedy, self).__init__(bernoulli_env)
        # The probability to explore at each time step
        self.eps = eps
        # Initial estimates
        self.estimates = np.random.normal(0, 1, self.bernoulli_env.N_arm)

    def arm_selection(self):
        sample = np.random.binomial(n=1, p=self.eps)
        if sample == 0:
            # Do a random exploration
            i = np.random.choice(self.bernoulli_env.N_arm)
        else:
            # Pick the best one
            i = np.argmax(self.estimates)
        self.counts[i] += 1
        return i

    def reward_observation(self, arm):
        # Generate a reward from environment.py
        reward = self.bernoulli_env.generate_reward(arm)
        return reward

    def estimate_update(self, arm, reward):
        self.estimates[arm] += 1. / (self.counts[arm] + 1) * (reward - self.estimates[arm])

    def run_one_step(self):
        arm = self.arm_selection()
        reward = self.reward_observation(arm)
        self.estimate_update(arm, reward)