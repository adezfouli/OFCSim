from agent import Agent
from environment import Envrionment
from instrumental import Instrumental, Extinction, sPIT, Devaluation, Degredation, sPITLesion, DevaluationLesion, Inh, \
    InhLesion


def sim_sPIT(steps, RR, lr, tau, bias):
    return Envrionment().n_simulation(Agent.agent_factory(tau, lr),
                                     [Instrumental('init', RR), Extinction('ext'), sPIT('sPIT', bias)],
                                     [200, 50, 50],
                                     steps)


def sim_sPIT_lesion(steps, RR, lr, tau, bias):
    return Envrionment().n_simulation(Agent.agent_factory(tau, lr),
                                     [Instrumental('init', RR), Extinction('ext'), sPITLesion('sPIT', bias)],
                                     [200, 50, 50],
                                     steps)


def sim_dev(steps, RR, lr, tau):
    return Envrionment().n_simulation(Agent.agent_factory(tau, lr),
                                     [Instrumental('init', RR), Devaluation('deval')],
                                     [200, 50],
                                     steps)


def sim_dev_lesion(steps, RR, lr, tau):
    return Envrionment().n_simulation(Agent.agent_factory(tau, lr),
                                     [Instrumental('init', RR), DevaluationLesion('deval')],
                                     [200, 50],
                                     steps)


def sim_deg(steps, RR, lr, tau):
    return Envrionment().n_simulation(Agent.agent_factory(tau, lr),
                                     [Instrumental('init', RR), Degredation('deg1', RR), Degredation('deg2', RR)],
                                     [0, 1000, 200],
                                     steps)

def sim_inh(steps, RR, lr, tau):
    return Envrionment().n_simulation(Agent.agent_factory(tau, lr),
                                     [Inh('init', RR)],
                                     [200],
                                     steps)


def sim_inh_lesion(steps, RR, lr, tau, bias):
    return Envrionment().n_simulation(Agent.agent_factory(tau, lr),
                                     [InhLesion('init', RR, bias)],
                                     [200],
                                     steps)

def print_resutls(input):
    for expr, expr_v in input.iteritems():
        print 'phase: ', expr
        for state, state_v in expr_v.iteritems():
            print 'state: ', state
            for action, action_v in state_v.iteritems():
                print 'action: ', action, '%.2f' % action_v

if __name__ == '__main__':
    simulation_steps = 3000
    tau = 5.0
    lr = 0.01
    RR = 0.1
    pit_bias = 0.2
    inh_bias = 0.1

    print'************** sPIT sham *********************'
    print_resutls(sim_sPIT(simulation_steps, RR, lr, tau, pit_bias))

    print'************** sPIT lesion *******************'
    print_resutls(sim_sPIT_lesion(simulation_steps, RR, lr, tau, pit_bias))

    print'************** devaluation sham **************'
    print_resutls(sim_dev(simulation_steps, RR, lr, tau))

    print'************** devaluation lesion ************'
    print_resutls(sim_dev_lesion(simulation_steps, RR, lr, tau))

    print'************** degradation *******************'
    print_resutls(sim_deg(simulation_steps, RR, lr, tau))
    #
    print'************** inhibition ********************'
    print_resutls(sim_inh(simulation_steps, 0.5, lr, tau))

    print'************** inhibition lesion *************'
    print_resutls(sim_inh_lesion(simulation_steps, 0.5, lr, tau, inh_bias))