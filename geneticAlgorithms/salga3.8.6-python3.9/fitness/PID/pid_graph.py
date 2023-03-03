#!/usr/bin/python3

# This file defines PID control for car velocity
# and defina fitness for adjust parameters Kp, Ti and Td of PID
import matplotlib.pyplot as plt

# how to use SALGA

# first, define a fenotype function (optional): given a chromosome returns an individual
# If defined, it's used only to print the best generation individual

import random

maxsetpoint = 7.0
#random.seed(43)
#learning = [maxsetpoint*random.random() for _ in range(30)]
#testing = [maxsetpoint*random.random() for _ in range(30)]

testing = [5.873687410057208, 2.073118484966126, 6.221265923524755, 3.6557690975416772, 0.7212849700273569, 5.989816030077931, 4.090639439060633, 6.529510815056114, 4.754761751199325, 0.6586909585711882, 4.35923364163896, 5.508202914372169, 6.292392731188021, 2.3189249210899803, 3.702239935463453, 4.908086009856498, 1.1677281996933098, 5.938517984457764, 5.466056937253434, 0.35068073969114444, 4.139858356691072, 2.576364860668913, 1.3020559229193096, 4.231362547669245, 6.784221112381168, 3.8637887659564116, 0.7931130757856578, 3.464496793564895, 5.45392680987738, 6.686601866267647]
learning = [0.2698628753616603, 4.873570258459369, 1.0075325497675272, 3.237725783803613, 4.701527348824369, 5.55065890158706, 3.1723245992634865, 3.4879056085863582, 0.13409975617043446, 3.0267218726600813, 2.6066227657464833, 5.966020432335971, 3.8288873300370394, 5.287217867784761, 3.0384769719656393, 1.233316729992827, 5.956126762562472, 5.741539909480978, 2.631007999735142, 0.6702017942392018, 3.587012423884575, 3.4718406714568277, 5.4061069392261105, 4.18051843231472, 3.5467320896949768, 4.02611247653423, 2.638476300572763, 0.34243819158431155, 0.428474748926875, 6.593325297756956]

print('\nUsed learning and testing setpoints')
print('---------------------------------')
print(learning)
print(testing)

def errors (chromosome, targets): # calcula el error se una secuencia de consignas
	return c.sequence(chromosome, targets)

# dependiente del controlador a usar sólo estas líneas
import controller
import importlib
importlib.reload(controller)

we = 0.0
import tkinter.simpledialog
strwe = tkinter.simpledialog.askstring('Energy weight (We)', 'Enter We', initialvalue=str(we))
we = float(strwe)
print(we)

npars = 3
levels = 1
# c = controller.controller([0.1, 5., 0.10, we]) // para mostrar en clase (we: 0.0, 2.0, 5.0)
c = controller.controller([0.1, 3.0, 0.05, we]) # problema propuesto 1
#c = controller.controller([0.5, 6.0, 0.25, we]) # problema propuesto 2

def globalerror (l): # calcula el error global de una lista de errores
	return sum(l) / len(l) # sumatorio de errores normalizado
	#return sum(l)+10.0*max(l) # sumatorio de errores penalizando el peor error

def globalerror_without_energy (errors): # remove energy errors
	res = []
	for i in range(len(errors)):
		if i%5!=4: # if isn't energy
			res.append(errors[i])
	return globalerror(res)

def globalerror2 (l):
	ts = 0
	d = 0
	overshot = 0
	ess = 0
	energy = 0
	for i in range(0,len(l),5):
		ts += l[i]
		d += l[i+1]
		overshot += l[i+2]
		ess += l[i+3]
		energy += l[i+4]
	n = len(l) // 5
	return (ts/n/c.w[0]*35, d/n/c.w[1], overshot/n/c.w[2], ess/n/c.w[3], energy/n)

def phenotype (chromosome):
	le = errors(chromosome, learning)
	e = globalerror(le)

	#l1.set_ydata(c.outputs)

	let = errors(chromosome, testing)
	et = globalerror(let)
	etp = globalerror_without_energy(let) # pure control error
	energy = c.total_energy/1000.0 # energía consumida en kws
	recenergy = c.total_recovered/1000.0 # energía recuperada por el motor en las frenadas
	print(energy)

	l2.set_ydata(c.outputs)
	l3.set_ydata(list(map(lambda x: maxsetpoint*((x - c.pid.utmin) / (c.pid.utmax-c.pid.utmin)), c.controls)))
	l4.set_ydata(list(map(lambda x: maxsetpoint*x/100 + maxsetpoint/2., c.energies))) # energía instantánea

	#plt.pause(0.001) # permite que funcione si se llama desde consola y no desde tkinter

	strch = str([f'{i:0.2f}' for i in chromosome])
	res = f'Genetic PID {strch} – Error: {e:.3f} – Test: {et:.3f} – Control: {etp:.3f} – Energy: {energy:.3f} $kws$ – Recov: {recenergy:.3f} $kws$ – $w_e$: {c.energy_weight_percent:.1f}%'
	plt.title(res, fontsize= 12)

	# imprime para comparación de métodos
	print('NPars: %d, Levels: %d, Error: %4.3f, Test: %4.3f, Control: %4.3f' % (npars,levels,e,et,etp))
	print(chromosome)
	print()

	return res


plt.ion()

def create_figure (labelx, labely):
	fig = plt.figure(figsize=[20.4, 4.8])
	axes = fig.add_subplot(111)
	ylim = axes.set_ylim(0.0,maxsetpoint)
	axes.set_xlabel(labelx)
	axes.set_ylabel(labely)

	for t in range(1,int(maxsetpoint),1):
		plt.axhline(y=t, color='gray', linestyle=':')
	plt.axhline(y=maxsetpoint/2., color='gray', linestyle=':')


points = 350*30
X = list(map(lambda x: x*c.model.T, range(points)))

create_figure('time (sec)','angular speed')

p0 = [0]*(npars*levels) # initial chromosome
e = globalerror(errors(p0,testing))
plt.plot(X, c.setpoints, 'black', linewidth=3, label='Test setpoints')

nodata = [0]*(350*30)
l3, = plt.plot(X, nodata, 'y',  label='Control signal')
l2, = plt.plot(X, nodata, 'r', label='Testing')
l4, = plt.plot(X, nodata, 'g', label='Energy')

plt.legend()


# second, define a fitness function (mandatory): given an chromosome, returns a number indicating the goodness of that chromosome

def fitness (chromosome):
	e = errors(chromosome, learning)
	error = globalerror(e)
	return 1.0 / (1.0 + error)

# third: force parameters

parameters = { 'alphabet':[0.0001, 100.0], 'normfactor': 0.95, 'type':'floating', 'norm':True, 'chromsize':npars*levels, 'pmut':1./(npars*levels), 'popsize':100, 'trace':1, 'tournament':6 }

# Explicar Goodhart Law
# probar ew = 1000
