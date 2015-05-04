import math
from random import random
import numpy as np

class Agent:
    def __init__(self, tau, lr):
        self.T ={}
        self.R = {}
        self.terminals = []
        self.transitionLR = lr
        self.tau = tau
        self.causual_power_coef = False

    def learn(self, from_state, to_state, action, r):
            SPE = 1 - self.T[from_state][action][to_state]
            self.T[from_state][action][to_state] += SPE * self.transitionLR
            for s in self.T[from_state][action].keys():
                if not (s == to_state):
                    self.T[from_state][action][s] *= (1 - self.transitionLR)

    def getBeta(self, k, s):
        return self.tau

    def aciton_probabilities(self, state):
        props = {}
        expos = np.zeros(len(self.T[state]))

        keys = self.T[state].keys()
        for k1 in keys:
            t = 0
            for k2 in keys:
                expos[t] = (
                    self.getBeta(k2, state) * self.action_value(state, k2) -
                    self.getBeta(k1, state) * self.action_value(state, k1) +
                    (0.0 if self.causual_power_coef == 0 else self.causual_power_coef * self.causal_power(state, k2)) -
                    (0.0 if self.causual_power_coef == 0 else self.causual_power_coef * self.causal_power(state, k1))
                )
                t += 1

            # for numerical stability
            maxExpos = expos.max()
            sum = 0.0
            for comp in expos:
                sum += math.exp(comp - maxExpos)
            sum = maxExpos + math.log(sum)
            props[k1] = -sum
        return props

    def other_factors(self, state, action):
        return 0.0


    def sample_action_from_props(self, p):
        d = random()
        total = 0
        for k,v in p.iteritems():
            total += math.exp(v)
            if d < total:
                return k


    def action_value(self, state, action):
        if state in self.terminals:
            return self.R[state]
        else:
            val = 0
            for s2 in self.T[state][action]:
                val += self.T[state][action][s2] * self.state_value(s2)
            return val

    def state_value(self, state):
        if state in self.terminals:
            return self.R[state]
        return max([self.action_value(state, a) for a in self.T[state].keys()])

    def causal_power(self, state, action):
        outcomes = ['O1', 'O2']
        cp = 0
        for o in outcomes:
            if self.T[state][action][o] > 0:
                cp += self.T[state][action][o]
                for other_actions in self.T[state].keys():
                    if not (other_actions == action):
                        cp -= self.T[state][other_actions][o]
        # print state, action, cp, self.T[state]
        return cp


    def sample_action(self, state):
        p = self.aciton_probabilities(state)
        d = random()
        total = 0
        for k,v in p.iteritems():
            total += math.exp(v)
            if d < total:
                return k

    @staticmethod
    def agent_factory(tau, lr):
        return lambda: Agent(tau, lr)


class prettyfloat(float):
    def __repr__(self):
        if isinstance(self, float):
            return "%0.2f" % self
        return self
