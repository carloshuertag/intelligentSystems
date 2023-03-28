import gymnasium as gym

def expert_system(observation):
    x, y, vx, vy, angle, angular_velocity, left_leg, right_leg = observation
    
    won = left_leg == 1 and right_leg == 1
    vertical_break = (y < 0.9) and vy < 0.1
    
    inclined_right = angle < -0.3
    inclined_left = angle > 0.3
    
    too_fast_right = vx > 0.2
    too_fast_left = vx < -0.2
    
    
    too_righty = x > 0.2
    too_lefty = x < -0.2
    
    if won:
      return 0, True
    
    if vertical_break and not (inclined_left or inclined_right): #! freno
      return 2,False
    
    
    if inclined_left and not too_fast_left:
      return 3,False
    if inclined_right and not too_fast_right:
      return 1,False
    
    if too_righty and not inclined_left:
      return 3,False
    
    if too_lefty and not inclined_right:
      return 1,False
    
    
    if vx < -0.2:
      return 3,False
    if vx > 0.2:
      return 1,False
    
    return 0,False
    
       
  
env = gym.make("LunarLander-v2", render_mode="human")
observation, info = env.reset()
for _ in range(1000):
    action,won = expert_system(observation)  # agent policy that uses the observation and info
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



      
 if too_fast_left and not inclined_right:
      return 3,False
    if too_fast_right and not inclined_left:
      return 1,False
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