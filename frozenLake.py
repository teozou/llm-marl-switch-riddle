import gymnasium as gym
import numpy as np

env = gym.make('FrozenLake-v1', is_slippery=False)

obs, info = env.reset()
print("Starting state:", obs)
print("Number of states:", env.observation_space.n)
print("Number of actions:", env.action_space.n)

Q = np.zeros((16,4))

alpha = 0.1      
gamma = 0.99     
epsilon = 1.0    
epsilon_decay = 0.999
epsilon_min = 0.05
n_episodes = 10000

for episode in range(n_episodes):
    obs, info = env.reset()
    done = False
    while not done:
        if np.random.random() < epsilon:
            action = env.action_space.sample()
        else:
            action = np.argmax(Q[obs])
        next_obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        Q[obs, action] = Q[obs, action] + alpha * (reward + gamma * np.max(Q[next_obs]) - Q[obs, action])
        obs = next_obs
    epsilon = max(epsilon_min, epsilon * epsilon_decay)

wins = 0
for _ in range(100):
    obs, info = env.reset()
    done = False
    while not done:
        action = np.argmax(Q[obs])
        obs, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
    if reward == 1.0:
        wins += 1
print(f"Success rate: {wins}%")