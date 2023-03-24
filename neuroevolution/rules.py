import gymnasium as gym

def expert_system(observation):
    x, y, vx, vy, angle, angular_velocity, left_leg, right_leg = observation
    
    # Regla 1: Si la nave está a la izquierda de la plataforma y tiene un ángulo menor que -0.2 radianes, gira a la derecha
    if left_leg == 1 and right_leg == 1:
      return 0, True
    if vy < -0.1 and y < 0.8:
      return 2,False
    if x < -0.3:
      return 3,False
    if x > 0.3:
      return 1,False
    
    if angle < -0.3:
      return 1,False
    if angle > 0.3:
      return 3,False
    
    if vx < -0.1:
      return 3,False
    if vx > 0.1:
      return 1,False
    return 0,False
    
       
  
env = gym.make("LunarLander-v2", render_mode="human")
observation, info = env.reset()
won = False
for _ in range(1000):
    action,wins = expert_system(observation)  # agent policy that uses the observation and info
    observation, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
      if won: print("Landed!") 
      observation, info = env.reset()
env.close()
"""

 if event.key == pygame.K_LEFT:
                action = 3
            elif event.key == pygame.K_RIGHT:
                action = 1
            elif event.key == pygame.K_UP:
                action = 2
            else:
                action = 0 
"""

# # Rule 2: If the Lunar Lander is moving too fast, slow it down
#         elif vx > 0.05:
#             action = 2
#         elif vx < -0.05:
#             action = 0

#         # Rule 3: If the Lunar Lander is too high, thrust downwards
#         elif y > 0.25:
#             action = 0
#         else:
#             action = 2

#         observation, reward, done, info = env.step(action)

#         if done:
#             print("Episode finished after {} timesteps".format(t+1))
#             break

#! x, y, vx, vy, angle, vangle, left_leg, right_leg = observation

#! Y -> para abajo es negativo X -> para la derecha es positivo 0,0 -> ???
#! para la velocidad es lo mismo pero con vx y vy
#! angulo es anti horario y la velang tambien
#! los ultimos dos son las patas