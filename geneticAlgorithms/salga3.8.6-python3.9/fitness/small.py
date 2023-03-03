#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import math

# define a function named fitness: given an chromosome, returns a number indicating the goodness of that chromosome (better when more zeroes)

def fitness (chromosome): # priorize small values
	score = 0
	for gene in chromosome:
		score += gene
	return 1.0/(1+score)
