#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import matplotlib.pyplot as plt

# Generate N cities

import random

cities = []
N2 = 10
for i in range(N2):
	for j in range(N2):
			c = [i/float(N2-1), j/float(N2-1)]
			cities.append(c)

N = len(cities)
print(N)


print(cities)

def dist (x, y):
	return ( (x[0]-y[0])**2 + (x[1]-y[1])**2 ) ** 0.5

def globaldist (chromosome):
	acum = 0.0
	for i in range(len(chromosome)):
		acum += dist(cities[chromosome[i-1]],cities[chromosome[i]]) # -1 is the last element
	return acum


# how to use genetics library
# first, define a fenotype function: given a chromosome returns an individual

# init graphics
plt.ion()
fig = plt.figure()
axes = fig.add_subplot(111)
xlim = axes.set_xlim(-0.05,1.05)
ylim = axes.set_ylim(-0.05,1.05)
x = []
y = []
l1, = axes.plot(x, y,'g')
l2, = axes.plot(x, y,'ro')

def orderedcities (chromosome):
	res = []
	x = []
	y = []
	for g in chromosome:
		res.append(cities[g])
		x.append(cities[g][0])
		y.append(cities[g][1])
	x.append(x[0])
	y.append(y[0])
	l1.set_data(x, y)
	l2.set_data(x, y)
	return res

def phenotype (chromosome):
	orderedcities(chromosome)
	s = 'Length=%5.3f' % globaldist(chromosome)
	plt.title(s)
	return s


# second, define a fitness function: given an chromosome, returns a number indicating the goodness of that chromosome

def fitness (chromosome): # priorize ordered genes
	score = globaldist(chromosome)
	return (1.0+N*0.1)/(1.0+score) # asume un promedio de distancia de 0.1 entre dos ciudades adyacentes en el óptimo para que en esas condiciones el optimo sea aprox. 1.0


# third: if desired, force parameters in UI
# valid parameters: alphabet, type, chromsize, elitism, norm, pmut, pemp, popsize

parameters = { 'alphabet':list(range(N)), 'type':'permutation' }
