#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# how to use genetics library
# first, define a fenotype function: given a chromosome returns an individual

# identity used
	
# second, define a firness function: given an chromosome, returns a number indicating the goodness of that chromosome

# resuelve cifras y letras, con algunas limitaciones
# 1) usa longitud fija en cronosomas
# 2) no comprueba que la división sea entera, y en todo caso hace división entera
# 3) los operadores se aplican en secuencia

def phenotype0 (chromosome): # operate
	res = cifras[0]
	for i in range(len(chromosome)):
		if not chromosome[i]=="nop": # permite ignorar un número
			res = eval("" + str(res) + chromosome[i] + str(cifras[i+1]))
	return res
	
def phenotype (chromosome):
	return '%s: %s' % (phenotype0(chromosome),chromosome)

cifras = [7, 12, 3, 2, 6, 23, 5]
print('given numbers are: %s' % cifras)

target = 2375 # (2+6)*3 - 12 + 7 = 19

import tkinter.simpledialog
target = int(tkinter.simpledialog.askstring('Target', 'Enter the target number (example 2375)'))
print('target is %d' % target)

def fitness (chromosome): # priorize ordered genes
	total = phenotype0(chromosome)
	return 1.0/(1.0+abs(target-total))

parameters = { 'alphabet':["+", "-", "*", "/", "nop"], 'type':'classic', 'elitism':True, 'norm':True, 'chromsize':6, 'pmut':0.2 }
