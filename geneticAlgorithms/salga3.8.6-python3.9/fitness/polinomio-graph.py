#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# This file defines fitness to find the coeficients of a polinomial giving a set of values x, p(x)

# how to use SALGA

# first, define a fenotype function (optional): given a chromosome returns an individual
# If defined, it's used only to print the best generation individual

import matplotlib.pyplot as plt

def phenotype (chromosome):
	res = ''
	for g in chromosome:
		res += "%4.2f " % (g)
	res += '(MAE: %4.2f)' % MAE(chromosome)

	y2 = []
	for v in x:
		y2.append(poli(chromosome,v))
	l1.set_ydata(y1)
	l2.set_ydata(y2)

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

# target coeficients to search
target = [-0.1, 3.0, 5.0, 7.0, -11.0]

import tkinter.simpledialog
st = tkinter.simpledialog.askstring('Target', 'Enter coeficients', initialvalue=str(target))
target = eval(st)

# calculates set of points to evaluate error
x = [p * 0.1 for p in range(-100, 101)]
y = []
for v in x:
	y.append(poli(target,v))

# https://stackoverflow.com/questions/4098131/how-to-update-a-plot-in-matplotlib
plt.ion()
fig = plt.figure()
axes = fig.add_subplot(111)
y1 = y[:]
l1, = axes.plot(x,y1,'r')
l2, = axes.plot(x,y1,'b')

# here is the fitness function

def MAE (chromosome):
	error = 0.0
	for i in range(len(x)):
		error += math.fabs(y[i]-poli(chromosome,x[i]))
	return error / len(x)

def fitness (chromosome):
	error = MAE(chromosome)
	return 1.0 / (1.0 + error)


# third: force parameters

parameters = { 'alphabet':[-15, 15], 'type':'floating', 'elitism':False, 'norm':True, 'chromsize':5, 'pmut':0.1, 'pcross':0.5, 'target':0.999 }
