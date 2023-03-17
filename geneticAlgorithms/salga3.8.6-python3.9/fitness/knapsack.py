"""
Authors: Juan Jose Urioste (@juanurioste), Carlos Huerta García (@huerta2502)
Date: March 17, 2023

fitness and phenotype functions for the knapsack problem
"""

import random

n = 50

def generate_random_knapsack_problem(num_items):
    items = []
    for i in range(num_items):
        weight = random.randint(1, 10)
        value = random.randint(1, 20)
        items.append((f'item{i}', weight, value))
    knapsack_capacity = random.randint(num_items*2, num_items*10)
    return items, knapsack_capacity

def knapsackDp(items, capacity):
    n = len(items)
    dp = [[0 for _ in range(capacity+1)] for _ in range(n+1)]
    for i in range(1, n+1):
        for j in range(1, capacity+1):
            if items[i-1][1] > j:
                dp[i][j] = dp[i-1][j]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i-1][j-items[i-1][1]] + items[i-1][2])
    return dp[n][capacity]

items, capacity = generate_random_knapsack_problem(n)
maxValue = knapsackDp(items, capacity)

def phenotype(chromosome):
    total_weight = 0
    total_value = 0
    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            total_weight += items[i][1]
            total_value += items[i][2]
    return f'weight: {total_weight} / {capacity}, value: {total_value}'

def fitness(chromosome):
    total_weight = 0
    total_value = 0
    for i in range(len(chromosome)):
        if chromosome[i] == 1:
            total_weight += items[i][1]
            total_value += items[i][2]
    if total_weight > capacity:
        return 0.0
    return 1.0 / (1.0 + ((maxValue - total_value) / maxValue))

parameters = {'alphabet': [0,1], 'type': 'classic', 'elitism': False, 'norm': True, 'chromsize': n, 'pmut': 0.2}
