"""
Authors: Juan Jose Urioste (@juanurioste), Carlos Huerta García (@huerta2502)
Date: March 17, 2023

fitness and phenotype functions for the n-queens problem
"""

n = 12
alphabet = [(x,y) for x in range(n) for y in range(n)]

def phenotype (chromosome):
    emptyRow = ['□'] * n
    board = ''
    currentRow = ''
    for i in range(n):
        currentRow = emptyRow[:]
        for j in range(n):
            if (i,j) in chromosome:
                currentRow[j] = '■'
        board += ' '.join(currentRow)
        board += '\n'
    return board

def fitness (chromosome):
    if len(chromosome) != len(set(chromosome)):
        return 0.0 # repeated queens are not allowed
    error = 0.0
    for i in range(len(chromosome)):
        for j in range(i+1, len(chromosome)):
            if chromosome[i][0] == chromosome[j][0] or chromosome[i][1] == chromosome[j][1]:
                error += 1.0 / n # queens in the same row or column are not allowed
            if abs(chromosome[i][0] - chromosome[j][0]) == abs(chromosome[i][1] - chromosome[j][1]):
                error += 1.0 / n # queens in the same diagonal are not allowed
    return 1.0 / (1.0 + error)

parameters = { 'alphabet':alphabet, 'type':'classic', 'elitism':False, 'norm':True, 'chromsize':n, 'pmut':0.2 }
