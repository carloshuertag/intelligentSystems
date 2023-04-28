from typing import Callable, List, NamedTuple, Sequence, SupportsFloat, Union
from collections import deque
import random
import gymnasium as gym
import tensorflow as tf
import numpy as np

class Transition(NamedTuple):
    prev_state: Any
    next_state: Any
    action: Any
    reward: SupportsFloat
    terminated: bool

class Memory:
    def __init__(self, size: int):
        self.max_size = int(size)
        self.transitions: deque = deque(maxlen=self.max_size)

    def remember(self, transition: Transition):
        self.transitions.append(transition)

    def batch(self, n: int) -> List[Transition]:
        n = min(len(self.transitions), n)
        return random.sample(self.transitions, n)

    def __len__(self) -> int:
        return len(self.transitions)

    def __getitem__(self, key: Union[int, slice]
    ) -> Union[Transition, Sequence[Transition]]:
        return self.transitions.__getitem__(key)

class Agent:
    def __init__(self, *,
        env: gym.Env,
        model: Union[Callable[[int, int], tf.keras.Model], tf.keras.Model, str],
        batch_size: int = 32,
        memory_size: int = 1e5,
        gamma: float = 0.99
    ):
        self.env = env
        self.inputs = env.observation_space.shape[0]
        self.actions = env.action_space.n
        self.batch_size = batch_size
        self.gamma = gamma
        self.memory = Memory(memory_size)
        self.current_state = None
        self.assign_model(model)
        
    def assign_model(self, model: Union[Callable[[int, int], tf.keras.Model], tf.keras.Model, str]) :
        if(callable(model)):
            self.model = model(self.inputs, self.actions)
        elif(isinstance(model, tf.keras.Model)):
            self.model = model
        elif(isinstance(model, str)):
            self.model = tf.keras.models.load_model(model)
        else:
            raise ValueError("model must be a function, tf.keras.Model, or a path to a model")

    def task(self, max_iterations: int = None) -> float:
        self.current_state, _ = self.env.reset()
        max_iterations = max_iterations or np.inf
        reward = 0
        running = True
        while running and max_iterations > 0:
            self.current_step += 1
            perception = self.perceive()
            action = self.decide(perception)
            transition = self.act(action)
            reward += transition.reward
            running = not transition.terminated
        return reward
    
    def perceive(self):
        return self.current_state
    
    def decide(self, perception):
        if random.random() < self.epsilon:
            return self.env.action_space.sample()
        else:
            perception = perception[np.newaxis, ...]
            q_values = self.model.predict(perception, verbose = 0)
            return np.argmax(q_values[0])
        
    def act(self, action):
        next_state, reward, terminated, _, _ = self.env.step(action)
        self.memory.remember(Transition(
            prev_state = self.current_state,
            next_state = next_state, 
            action = action,
            reward = reward,
            terminated = terminated))
        self.current_state = next_state
        return self.memory[-1]
    
class IOModel:
    def __init__(self, inputs, outputs) -> tf.keras.Model:
