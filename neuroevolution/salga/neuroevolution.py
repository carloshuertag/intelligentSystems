from models.Multilayer import Multilayer
import gymnasium as gym
import numpy as np
CHROMSIZE = 8 * 6 + 6 + 6 * 4 + 4

def phenotype(chromosome):
    return f'{chromosome}'
  
def fitness(chromosome):
  model = Multilayer(8, 6, 4)
  model.from_chromosome(chromosome)
  env = gym.make("LunarLander-v2")
  observation, info = env.reset()
  total_reward = 0
  for _ in range(1000):
    action = model.inference(observation)
    observation, reward, terminated, truncated, info = env.step(np.argmax(action))
    total_reward += reward
    
    if terminated or truncated:
        observation, info = env.reset()
  env.close()
  return total_reward


parameters = { 'alphabet':[-1, 1], 'type':'floating', 'norm':True, 'chromsize':CHROMSIZE, 'pmut':1./(CHROMSIZE), 'popsize':100, 'trace':1, 'tournament':6 }