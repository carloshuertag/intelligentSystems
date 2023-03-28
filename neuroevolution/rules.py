import gymnasium as gym

def expert_system(observation):
    x, y, vx, vy, angle, angular_velocity, left_leg, right_leg = observation
    isRotating = abs(angular_velocity) > 0.15
    isMoving = abs(vx) > 0.15
    isLeaving = vy > 0.15
    isLeft = x < -0.15
    isRight = x > 0.15
    isForward = angle > 0.3
    isBackward = angle < -0.3
    isAtBase = y < 0.025
    isUp = y < 0.8
    won = left_leg == 1 and right_leg == 1 and isAtBase and not isLeft and not isRight
    if won:
      return 0, True
    if isRotating:
      if isForward:
        return 3, False
      elif isBackward:
        return 1, False
    if not isAtBase and isUp and not isLeaving:
      return 2, False
    if isMoving:
      if isRight:
        return 3, False
      else:
        return 1, False
    """
    vertical_break = (vy < -0.1) and vy < 0.01 and y < 0.9
    inclined_right = angle < -0.3
    inclined_left = angle > 0.3
    too_fast_right = vx > 0.2
    too_fast_left = vx < -0.2
    too_righty = x > 0.15
    too_lefty = x < -0.15
    too_xd = angular_velocity > 0.3
    if won:
      return 0, True
    if vertical_break and not (inclined_left or inclined_right) and not too_xd: #! freno
      return 2,False
    if inclined_left and not too_righty and not too_fast_right:
      return 3,False
    if inclined_right and not too_lefty and not too_fast_left:
      return 1,False
    if too_righty and not inclined_left:
      return 1,False
    if too_lefty and not inclined_right:
      return 3,False
    """
    return 0,False
    
  
env = gym.make("LunarLander-v2", render_mode="human")
observation, info = env.reset()
count = 0
while(count < 10):
    action,won = expert_system(observation)  # agent policy that uses the observation and info
    observation, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
      count += 1
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