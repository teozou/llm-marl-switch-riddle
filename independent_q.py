from switch_riddle import SwitchRiddleEnv
import numpy as np

env = SwitchRiddleEnv(n_agents=3)

obs= env.reset()
Q = np.zeros((6,3))

alpha = 0.1      
gamma = 0.99     
epsilon = 1.0    
epsilon_decay = 0.999
epsilon_min = 0.05
n_episodes = 10000

for episode in range(n_episodes):
    obs = env.reset()
    state = obs[0] * 3 + obs[1]
    done = False
    while not done:
        if np.random.random() < epsilon:
            action = np.random.randint(3)
        else:
            action = np.argmax(Q[state])
        next_obs, reward, terminated, info = env.step(action)
        done = terminated
        next_state = next_obs[0] * 3 + next_obs[1]
        Q[state, action] = Q[state, action] + alpha * (reward + gamma * np.max(Q[next_state]) - Q[state, action])
        obs = next_obs
        state = next_state
    epsilon = max(epsilon_min, epsilon * epsilon_decay)

wins = 0
for _ in range(1000):
    obs = env.reset()
    state = obs[0] * 3 + obs[1]
    done = False
    while not done:
        action = np.argmax(Q[state])
        next_obs, reward, terminated, info = env.step(action)
        done = terminated
        next_state = next_obs[0] * 3 + next_obs[1]
        state = next_state
    if reward == 1.0:
        wins += 1
print(f"Success rate: {wins/100}%")