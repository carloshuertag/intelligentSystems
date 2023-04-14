from models.Multilayer import Multilayer
import gymnasium as gym
import numpy as np
model = Multilayer(8, 6, 4) # 8 inputs, 6 hidden neurons, 4 outputs
CHROMSIZE = 8 * 6 + 6 + 6 * 4 + 4
N = 10  # number of episodes to average
env = gym.make("LunarLander-v2") # fitness environment
graphical_env = gym.make("LunarLander-v2", render_mode="human") # phenotype environment

def phenotype(chromosome):
  observation, info = graphical_env.reset()
  model = Multilayer(8, 6, 4)
  model.from_chromosome(chromosome)
  observation, info = graphical_env.reset()
  partial_reward = 0
  while True:
    graphical_env.render() # display the phenotype
    action = model.inference(observation)
    observation, reward, terminated, truncated, info = graphical_env.step(np.argmax(action))
    partial_reward += reward
    if terminated or truncated:
        break
  return f'reward: {partial_reward}'
  
def fitness(chromosome):
  model.from_chromosome(chromosome)
  observation, info = env.reset()
  total_reward = 0
  for _ in range(N):
    partial_reward = 0
    while True:
      action = model.inference(observation)
      observation, reward, terminated, truncated, info = env.step(np.argmax(action))
      partial_reward += reward
      if terminated or truncated:
          break
    partial_reward += 600 # add 600 points for each episode
    partial_reward /= 1200 # normalize to [0, 1]
    total_reward += partial_reward
  env.close()
  return total_reward / N if total_reward > 0 else 0

parameters = { 'alphabet':[-10, 10], 'type':'floating', 'norm':True, 'chromsize':CHROMSIZE, 'pmut':1./(CHROMSIZE), 'popsize':100, 'trace':10, 'tournament':6 }