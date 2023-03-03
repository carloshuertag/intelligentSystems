#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# resuelve problema de examen de enero de 2017

precios = [62,55,17,115,40,65,80,83,99,49,25,30,22,30,30,50,70,60,58,110]
estrellas = [1,4,3,2,5,1,1,2,5,4,3,4,4,3,2,3,5,4,4,5]
presupuesto = 300.0

[2,6,4,4,1]
[17,80,40,40,55]

def fitness0 (chromosome):
	coste = 0.0
	maxc = precios[chromosome[0]]
	minc = precios[chromosome[0]]
	for r in chromosome:
		coste += precios[r] # acumula el coste total
		if precios[r]<minc:
			minc = precios[r]
		if precios[r]>maxc:
			maxc = precios[r]

	diferencia = maxc - minc # calcula la diferencia entre el más caro y el más barato
	return (coste,diferencia)

def phenotype (chromosome): # describe el cromosoma de modo legible
	coste, diferencia = fitness0(chromosome)
	costes = []
	for r in chromosome:
		costes.append(precios[r])
	return 'Regalos: %s, Precios: %s, Coste: %s, Diferencia: %s' % (chromosome, costes, coste, diferencia)

def fitness (chromosome):
	coste, diferencia = fitness0(chromosome)
	if coste>presupuesto: # si se pasa del presupuesto, fitness 0
		return 0.0
	# si hay dos regalos iguales, fitness 0
	
	chromosomeSet = set(chromosome)
	if len(chromosome) != len(chromosomeSet):
		return 0.0
	
	error = (presupuesto - coste) + diferencia
	total = 1.0 / (1.0 + error) # mayor cuanto más cerca del presupuesto y menor la diferencia
	#if len(set(chromosome))<len(chromosome): # para evitar dos regalos iguales
	#	return 0.1 * total
	return total


alphabet = list(range(len(precios))) # crea el alfabeto desde 0 al número de regalos - 1

# fija parámetros del genético desde aquí
parameters = { 'alphabet':alphabet, 'type':'classic', 'elitism':True, 'norm':True, 'chromsize':10, 'pmut':0.2 }
#parameters = { 'alphabet':alphabet, 'type':'permutation', 'elitism':True, 'norm':True, 'chromsize':10, 'pmut':0.2 }

