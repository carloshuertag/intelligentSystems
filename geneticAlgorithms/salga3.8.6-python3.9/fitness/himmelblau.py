# función de Himmelblau

import matplotlib.pyplot as plt

plt.ion()
fig = plt.figure()
axes = fig.add_subplot(111)
xlim = axes.set_xlim(-4.0,4.0)
ylim = axes.set_ylim(-4.0,4.0)

def phenotype (ch, g):
	axes.cla()
	xlim = axes.set_xlim(-4.0,4.0)
	ylim = axes.set_ylim(-4.0,4.0)

	for ind in g.population:
		plt.plot(ind[0],ind[1],'ro')
	plt.plot(ch[0],ch[1],'bo')

	# plot 4 solutions in green
	plt.plot(3,2,'g+')
	plt.plot(-2.805,3.13,'g+')
	plt.plot(-3.77,-3.28,'g+')
	plt.plot(3.58,-1.84,'g+')

	return [round(ch[0],2), round(ch[1],2)]

onlyone = False
def himmelblau (ch):
	x = ch[0]
	y = ch[1]
	fxy = (x**2 + y - 11)**2 + (x + y**2 -7)**2
	if onlyone and (x>0 or y>0): # himmelblau modified to have only one global minimum (-3.77, -3.28)
		fxy += 0.5
	return fxy

def fitness (ch):
	return 1 / (1 + himmelblau(ch))

parameters = { 'alphabet':[-4, 4], 'chromsize': 2, 'type':'swarm', 'pmut':0.1, 'pcross':0.2, 'trace':100, 'target':0.999}

# 4 soluciones idénticas en (3,2), (-2.805..., 3.13...), (-3.77..., -3.28...), (3.58..., -1.84...)
# https://es.wikipedia.org/wiki/Función_de_Himmelblau
