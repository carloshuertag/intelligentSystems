#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# how to use genetics library
# first, define a fenotype function: given a chromosome returns an individual

# identity used
	
# second, define a firness function: given an chromosome, returns a number indicating the goodness of that chromosome

# resuelve un laberinto utilizando cromosomas de longitud variable
# alfabeto ["L", "R", "A"] (Left, Right, Advance]

solution = ['A', 'A', 'A', 'L', 'A', 'A', 'A', 'R', 'A', 'A', 'A', 'L', 'A', 'A', 'A', 'R', 'A', 'A', 'A']
print('Solution is ', solution)

def fitness (chromosome): # priorize ordered genes
	res = 0
	lc = len(chromosome)
	ls = len(solution)
	for i in range(lc):
		if i<ls and chromosome[i]==solution[i]:
			res += 1
		else:
			break
	if lc>ls: # si el camino se pasa de la solución
		res -= lc-ls
	return res / float(ls)

parameters = { 'alphabet':["L", "R", "A"], 'type':'variable', 'elitism':True, 'norm':True, 'chromsize':1, 'pmut':0.2 }
