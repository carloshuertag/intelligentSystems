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