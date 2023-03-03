#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# This file defines fitness to find the coeficients of a polinomial giving a set of values x, p(x)

# how to use SALGA

# first, define a fenotype function (optional): given a chromosome returns an individual
# If defined, it's used only to print the best generation individual

def phenotype (chromosome):
	res = ''
	for g in chromosome:
		res += "%4.2f " % (g)
	res += '(MAE: %4.2f)' % MAE(chromosome)
	return res


# second, define a fitness function (mandatory): given an chromosome, returns a number indicating the goodness of that chromosome

import math

def poli (chromosome,x): # evaluates a polinomial with coeficientes in chromosome for x
	res = 0.0
	l = len(chromosome)
	for t in range(l):
		exp = l-t-1
		res += chromosome[t]*math.pow(x,exp)
	return res
#	return chromosome[3]*math.pow(x,3) + chromosome[2]*math.pow(x,2) + chromosome[1]*x + chromosome[0]

# target coeficients to search
target = [2.0, 3.0, 5.0, 7.0, 11.0]

import tkinter.simpledialog
st = tkinter.simpledialog.askstring('Target', 'Enter coeficients', initialvalue=str(target))
target = eval(st)


# calculates set of points to evaluate error
x = [p * 0.1 for p in range(-100, 101)]
y = []
for v in x:
	y.append(poli(target,v))


# now is the fitness function

def MAE (chromosome):
	error = 0.0
	for i in range(len(x)):
		error += math.fabs(y[i]-poli(chromosome,x[i]))
	return error / len(x)

def fitness (chromosome):
	error = MAE(chromosome)
	return 1.0 / (1.0 + error)


# third: force parameters

parameters = { 'alphabet':[0, 15], 'type':'floating', 'elitism':False, 'norm':True, 'chromsize':5, 'pmut':0.1, 'pcross':0.5, 'target':0.999 }
