#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# how to use genetics library
# first, define a fenotype function: given a chromosome returns an individual

def phenotype (chromosome):
	score = 0
	for i in range(len(chromosome)-1):
		score += abs(chromosome[i+1]-chromosome[i])
	return 'Length=%d; %s' % (score, chromosome)


# second, define a fitness function: given an chromosome, returns a number indicating the goodness of that chromosome

def fitness (chromosome): # priorize ordered genes
	score = 0
	for i in range(len(chromosome)-1):
		score += abs(chromosome[i+1]-chromosome[i])
	return float(len(chromosome)-1)/score


# third: if desired, force parameters in UI
# valid parameters: alphabet, type, chromsize, elitism, norm, pmut, pemp, popsize

parameters = { 'alphabet':list(range(100)), 'type':'permutation', 'norm':True, 'normfactor':0.3, 'elitism':True, 'pmut':0.01 }
