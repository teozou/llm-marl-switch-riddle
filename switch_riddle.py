import numpy as np

class SwitchRiddleEnv:
    def __init__(self, n_agents=3):
        self.n_agents = n_agents
        self.light = 0
        self.visited = set()
        self.current_agent = np.random.randint(self.n_agents)
        self.steps = 0
        self.max_steps = 4 * n_agents ** 2

    def reset(self):
        self.light = 0
        self.visited = set()
        self.current_agent = np.random.randint(self.n_agents)
        self.steps = 0
        return (self.light, self.current_agent)
    
    def step(self, action ):
        reward = 0
        done = False
        if action == 0:
            pass
        elif action == 1:
            self.light = 1 - self.light
        elif action == 2:
            if len(self.visited) == self.n_agents:
                reward = 1
            else:
                reward = -1
            done = True
        self.steps += 1
        if self.steps >= self.max_steps:
            done = True
        self.visited.add( self.current_agent)   
        self.current_agent = np.random.randint(self.n_agents)
        observation=(self.light, self.current_agent)
        return observation, reward, done, {}




