from random import random


class Instrumental:
    def __init__(self, name, ratio):
        self.ratio = ratio
        self.name = name
        pass

    def setup_agent(self, agent):
        agent.T, agent.R, agent.terminals = {
                   'S0': {
                       'L': {'O1': 0.0, 'O2': 0.0, 'NO': 1.0},
                       'R': {'O1': 0.0, 'O2': 0.0, 'NO': 1.0},
                       'OA': {'O1': 0.0, 'O2': 0.0, 'NO': 1.0},
                   }}, \
               {'O1': 1., 'O2': 1., 'NO': 0.}, \
               ['O1', 'O2', 'NO']

    def state_reward(self, state, action):
        if state == 'S0':
            if action == 'L':
                if random() < self.ratio:
                    return 'O1', 0
                else:
                    return 'NO', 0
            if action == 'R':
                if random() < self.ratio:
                    return 'O2', 0
                else:
                    return 'NO', 0
            if action == 'OA':
                return 'NO', 0
        else:
            return 'S0'

    def init_state(self):
        return 'S0'

    def is_terminal(self, state):
        if state in ['O1', 'O2', 'NO']:
            return True
        return False

    def get_states(self):
        return ['S0']

    def __str__(self):
        return 'instrumental' + self.name


class Extinction(Instrumental):

    def __init__(self, name):
        Instrumental.__init__(self, name, 0.0)

    def setup_agent(self, agent):
        pass


class sPIT(Instrumental):
    def __init__(self, name, bias):
        Instrumental.__init__(self, name, 0.0)
        self.bias = bias

    def setup_agent(self, agent):
        agent.T['S0']['L']['O1'] += self.bias
        agent.T['S0']['L']['NO'] -= self.bias


class sPITLesion(Instrumental):
    def __init__(self, name, bias):
        Instrumental.__init__(self, name, 0.0)
        self.bias = bias

    def setup_agent(self, agent):
        agent.T['S0']['L']['O1'] += self.bias
        agent.T['S0']['L']['NO'] -= self.bias
        agent.T['S0']['R']['O1'] += self.bias
        agent.T['S0']['R']['NO'] -= self.bias

class Devaluation(Instrumental):
    def __init__(self, name):
        Instrumental.__init__(self, name, 0.0)

    def setup_agent(self, agent):
        agent.R['O1'] = -1.0

class DevaluationLesion(Instrumental):
    def __init__(self, name):
        Instrumental.__init__(self, name, 0.0)

    def setup_agent(self, agent):
        agent.R['O1'] = -0.5
        agent.R['O2'] = -0.5

class Degredation(Instrumental):
    def __init__(self, name, ratio):
        Instrumental.__init__(self, name, ratio)

    def setup_agent(self, agent):
        agent.causual_power_coef = 10.0

    def state_reward(self, state, action):
        if state == 'S0':
            if action == 'L':
                if random() < self.ratio:
                    return 'O1', 0
                else:
                    return 'NO', 0
            if action == 'R':
                if random() < self.ratio:
                    return 'O2', 0
                else:
                    return 'NO', 0
            if action == 'OA':
                if random() < self.ratio:
                    return 'O2', 0
                else:
                    return 'NO', 0
        else:
            return 'S0', 0


class Inh(Instrumental):
    def __init__(self, name, ratio):
        Instrumental.__init__(self, name, ratio)
        self.ratio = ratio
        self.name = name

    def setup_agent(self, agent):
        agent.T, agent.R, agent.terminals = {
                   'S0': {
                       'L': {'O1': 0.5, 'O2': 0.0, 'NO': 0.5},
                       'R': {'O1': 0.0, 'O2': 0.5, 'NO': 0.5},
                   }}, \
               {'O1': 0.0, 'O2': 0.1, 'NO': 0.0}, \
               ['O1', 'O2', 'NO']


class InhLesion(Instrumental):
    def __init__(self, name, ratio, bias):
        Instrumental.__init__(self, name, ratio)
        self.ratio = ratio
        self.name = name
        self.bias = bias

    def setup_agent(self, agent):
        agent.T, agent.R, agent.terminals = {
                   'S0': {
                       'L': {'O1': 0.5, 'O2': 0.0, 'NO': 0.5},
                       'R': {'O1': 0.0, 'O2': 0.5, 'NO': 0.5},
                   }}, \
               {'O1': 1.0, 'O2': 1.0, 'NO': 0.0}, \
               ['O1', 'O2', 'NO']
        agent.T['S0']['L']['O1'] += self.bias
        agent.T['S0']['L']['NO'] -= self.bias