#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# how to use SALGA

# first, define a fenotype function: given a chromosome returns an individual

import math

def fun (chromosome):
	x = chromosome[0]
	y = chromosome[1]
	return -math.cos(x)*math.cos(y)*math.exp(-((x-math.pi)**2 + (y - math.pi)**2 )) # Easom function

def phenotype (chromosome):
	res = 'f ( '
	for g in chromosome:
		res += "%4.2f " % (g)
	return res + ") = %4.2f" % fun(chromosome)

# second, define a fitness function: given an chromosome, returns a number indicating the goodness of that chromosome

print(phenotype([math.pi, math.pi]))

def fitness (chromosome):
		return (1 - fun(chromosome)) / 0.99999

# third: load this .py in SALGA and learn

parameters = { 'alphabet':[-100, 100], 'type':'floating', 'elitism':True, 'norm':True, 'chromsize':2, 'pmut':0.5, 'target':2.0 }
