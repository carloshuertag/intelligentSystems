#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# how to use SALGA

# first, define a fenotype function: given a chromosome returns an individual

def phenotype (chromosome): # computes the decimal number represented by the chromosome
	res = 0
	l = len(chromosome)
	for v in range(l):
		if chromosome[l-v-1] != 0:
			res += 2**v
	return res
	
	
# second, define a fitness function: given an chromosome, returns a number indicating the goodness of that chromosome

target = 315*315
target = 3152*3152
target = 699050*699050

import math

def fitness (chromosome): # aproximates x^2 = target
	fen = phenotype(chromosome)
	return 1.0 / (1.0 + pow(abs(target-fen**2),0.1)) # maximum value when fen**2 == target!; pow atenuates differences

# third: load this .py in SALGA and learn

parameters = { 'alphabet':[0,1], 'type':'classic', 'chromsize':20 }
