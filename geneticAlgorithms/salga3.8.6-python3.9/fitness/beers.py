def profit(production):
    return 4 * production[0] + 7 * production[1] + 3 * production[2]

def phenotype (chromosome):
    return 'Producción: %d negras, %d rubias y %d baja graduación. Beneficio: %1.1f' % (chromosome[0],
    chromosome[1], chromosome[2], profit(chromosome))

def fitness (chromosome):
    malt = 2 * chromosome[0] + chromosome[1] + 2 * chromosome[2]
    if malt > 30:
        return 0.0
    yeast = chromosome[0] + 2 * chromosome[1] + 2 * chromosome[2]
    if yeast > 45:
        return 0.0
    prof = profit(chromosome)
    if (prof == 0):
        prof += 0.00001
    error = 1.0 / prof
    return 1.0 / (1.0 + error)

alphabet = list(range(0,45))

parameters = { 'alphabet':alphabet, 'type':'classic', 'elitism':False, 'norm':True, 'chromsize':3, 'pmut':0.2 }
