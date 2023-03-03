#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# how to use SALGA

# first, define a fenotype function: given a chromosome returns an individual

import math

def fun (chromosome):
	x = chromosome[0]
	y = chromosome[1]	
	#return 5 * math.cos(x) + 1.1 * math.sin(y)
	return math.cos(x) + math.sin(y)

def phenotype (chromosome):
	res = 'f ( '
	for g in chromosome:
		res += "%4.2f " % (g)
	return res + ") = %4.2f" % fun(chromosome)

# second, define a fitness function: given an chromosome, returns a number indicating the goodness of that chromosome

def fitness (chromosome):
		return 1.0 / (1.0 + fun(chromosome)**2) # maximum value when res == 0


# third: load this .py in SALGA and learn

parameters = { 'alphabet':[0, 10], 'type':'floating', 'elitism':True, 'norm':True, 'chromsize':2, 'pmut':0.5 }
