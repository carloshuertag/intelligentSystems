#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# programa para optimización de horarios con genéticos

alpha = [ 'Mat', 'Mat', 'Mat', 'Len', 'Len', 'Len', 'Len', 'Ing', 'Ing', 'Ing', 'Soc', 'Soc', 'Soc', 'Bio', 'Bio', 'Fis', 'Fis', 'Tec', 'Tec', 'Tec', 'Qui', 'Qui', 'Pla', 'Pla', 'EdF', 'EdF', 'Mus', 'Mus', 'MAE', 'Tut' ]
print(alpha)
print('Use permutation type')
print('Set Target Fit. to 50')

# 30 clases por semana, 6h diarias

def porfranjas (chromosome):
	return [ chromosome[0:5], chromosome[5:10], chromosome[10:15], chromosome[15:20], chromosome[20:25], chromosome[25:30] ]

def phenotype (chromosome):
	f = porfranjas(chromosome)
	res = ""
	for e in f:
		for d in e:
			res += "%4s" % (d)
		res += "\n"
	return res


def pordias (chromosome):
	res = []
	for i in range(5): # para cada día
		dia = []
		for j in range(6): # para cada franja horaria
			dia.append(chromosome[i+j*5])
		res.append(dia)
	return res

# second, define a fitness function: given an chromosome, returns a number indicating the goodness of that chromosome

def fitness (chromosome): # priorize ordered genes
	franjas = porfranjas(chromosome)
	dias = pordias(chromosome)

	score = 0.0

	score += 50.0*franjas[0].count('Mat')/5.0 # matemáticas a primera hora (max: 50)

	for franja in franjas: # prioriza menos asignaturas en la misma franja (max: 5)
		diferentes = set(franja)
		score += 1.0 / float(len(diferentes))

	# se prioriza que no haya repetidos en un mismo día (max: 50)
	for dia in dias:
		diferentes = set(dia)
		score += 10.0 * float(len(diferentes))

	if 'Tut' not in dias[4]:
		return 0.0

	return score / len(franjas) # divide por el número de horas al día

# third, force parameters

parameters = { 'alphabet':alpha, 'type':'permutation', 'target':60, 'elitism':True, 'pmut': 1/25.0 }

# modificar para que:
# MAE sea los lunes
# Plástica sea a última hora
