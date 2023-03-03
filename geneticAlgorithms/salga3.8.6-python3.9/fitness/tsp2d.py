#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# Generate N cities

import random
N = 100

cities = []

for i in range(N):
	c = [random.random(), random.random()]
	cities.append(c)

'''
N2 = N**0.5
for i in range(int(N2)):
	for j in range(int(N2)):
		c = [i/N2, j/N2]
		cities.append(c)
'''

#print(cities)

def dist (x, y): # euclidean distance
	return ( (x[0]-y[0])**2 + (x[1]-y[1])**2 ) ** 0.5

def globaldist (chromosome):
	acum = 0.0
	for i in range(len(chromosome)):
		acum += dist(cities[chromosome[i-1]],cities[chromosome[i]])
	return acum


# how to use genetics library
# first, define a fenotype function: given a chromosome returns an individual

def orderedcities (chromosome):
	res = []
	for g in chromosome:
		res += [cities[g]]
	return res

def phenotype (chromosome):
	s = ''
	s = 'Length=%5.3f\n' % globaldist(chromosome)
	for c in orderedcities(chromosome):
		s += str(c[0]) + '\t' + str(c[1]) + '\n'
	return s
	#return 'Length=%5.3f; %s' % (globaldist(chromosome), orderedcities(chromosome))


# second, define a fitness function: given an chromosome, returns a number indicating the goodness of that chromosome

def fitness (chromosome): # priorize ordered genes
	score = globaldist(chromosome)
	return (1.0+N*0.1)/(1.0+score) # asume un promedio de distancia de 0.1 entre dos ciudades adyacentes en el óptimo para que en esas condiciones el optimo sea aprox. 1.0


# third: if desired, force parameters in UI
# valid parameters: alphabet, type, chromsize, elitism, norm, pmut, pemp, popsize

parameters = { 'alphabet':list(range(N)), 'type':'permutation' }
