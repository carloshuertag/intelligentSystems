import random
import gymnasium as gym
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np
from collections import deque

class DQLAgent:
    def __init__(self, env):
        self.state_size = env.observation_space.shape[0]
        self.action_size = env.action_space.n
        self.epsilon = 1
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.9993
        self.gamma = 0.99
        self.learning_rate = 0.0001
        self.memory = deque(maxlen=4000)
        self.model = self.build_model()
        self.target_model = self.build_model()

    def build_model(self):
        model = Sequential()
        model.add(Dense(64, input_dim=self.state_size, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, s):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        act_values = self.model.predict(s)
        return np.argmax(act_values[0])

    def replay(self,batch_size):
        "vectorized replay method"
        if len(agent.memory) < batch_size:
            return

        minibatch = random.sample(self.memory, batch_size)
        minibatch = np.array(minibatch)
        not_done_indices = np.where(minibatch[:, 4] == False)
        y = np.copy(minibatch[:, 2])

        if len(not_done_indices[0]) > 0:
            predict_sprime = self.model.predict(np.vstack(minibatch[:, 3]))
            predict_sprime_target = self.target_model.predict(np.vstack(minibatch[:, 3]))
            
            y[not_done_indices] += np.multiply(self.gamma, predict_sprime_target[not_done_indices, np.argmax(predict_sprime[not_done_indices, :][0], axis=1)][0])

        actions = np.array(minibatch[:, 1], dtype=int)
        y_target = self.model.predict(np.vstack(minibatch[:, 0]))
        y_target[range(batch_size), actions] = y
        self.model.fit(np.vstack(minibatch[:, 0]), y_target, epochs=1, verbose=0)
        

            
    def adaptiveEGreedy(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def targetModelUpdate(self):
        self.target_model.set_weights(self.model.get_weights())
            
if __name__ == "__main__":
    env = gym.make('LunarLander-v2')

    state, _ = env.reset()

    agent = DQLAgent(env)
    state_number = env.observation_space.shape[0]
    
    batch_size = 32
    episodes = 5
    for e in range(episodes):
        
        state,_ = env.reset()
        state = np.reshape(state, [1, state_number])

        total_reward = 0
        for time in range(1000):
            

            action = agent.act(state)
            
            next_state, reward, done, _,_ = env.step(action)
            next_state = np.reshape(next_state, [1, state_number])

            agent.remember(state, action, reward, next_state, done)

            state = next_state

            agent.replay(batch_size)

            total_reward += reward
            
            if done:
                agent.targetModelUpdate()
                break

        agent.adaptiveEGreedy()

        print('Episode: {}, Reward: {}'.format(e,total_reward))
        

env = gym.make('LunarLander-v2', render_mode='human')

state, _ = env.reset()

terminated = truncated = False
while not (terminated or truncated):
    # Seleccionamos una acción dado el actual estado ...
    action = agent.act(state)
    # ... y la ejecutamos, obteniendo el nuevo estado
    state, _, terminated, truncated, _ = env.step(action)
env.close()