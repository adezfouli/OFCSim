import scipy
from scipy.stats import itemfreq
from agent import Agent


class Envrionment:
    def __init__(self):
        pass

    @staticmethod
    def n_simulation(agent_factory, envs, n_trials, n_repeat):
        simulations = {}
        for e in envs:
            simulations[str(e)] = []
        for i in range(n_repeat):
            for e, v in Envrionment.simulate(agent_factory(), envs, n_trials).iteritems():
                simulations[str(e)].append(v)
        return Envrionment.summerize_traces(simulations)

    @staticmethod
    def simulate(agent, envs, n_trials):
        traces = {}
        for env, n_trial in zip(envs, n_trials):
            state = env.init_state()
            env.setup_agent(agent)
            trace = {}
            for s in env.get_states():
                trace[s] = []
            for t in range(n_trial):
                action = agent.sample_action(state)
                (new_state, reward) = env.state_reward(state, action)
                agent.learn(state, new_state, action, reward)
                trace[state].append(action)
                if env.is_terminal(new_state):
                    state = env.init_state()
            traces[str(env)] = trace
        return traces

    @staticmethod
    def summarize_single_trace(trace):
        output = {}
        for s, v in trace.iteritems():
            output[s] = {}
            c = itemfreq(v)
            for ac in c:
                output[s][ac[0]] = float(ac[1]) / len(v)
        return output

    @staticmethod
    def summerize_traces(traces_env):
        env_traces_sum = {}
        for env, traces in traces_env.iteritems():
            traces_sum = {}
            for trace in traces:
                trace_sum = Envrionment.summarize_single_trace(trace)
                for ts, tv in trace_sum.iteritems():
                    if not ts in traces_sum.keys():
                        traces_sum[ts] = {}
                    for tsa, tvs in tv.iteritems():
                        if not tsa in traces_sum[ts].keys():
                            traces_sum[ts][tsa] = tvs / len(traces)
                        else:
                            traces_sum[ts][tsa] += tvs / len(traces)
            env_traces_sum[str(env)] = traces_sum
        return env_traces_sum

