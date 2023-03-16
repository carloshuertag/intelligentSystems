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

alphabet, capacity = generate_random_knapsack_problem(n)

def phenotype(chromosome):
    return '\n'.join([f'{item[0]}: {item[1]}kg, {item[2]}€' for item in chromosome])

def fitness(chromosome):
    total_weight = 0
    total_value = 0
    for item in chromosome:
            total_weight += item[1]
            total_value += item[2]
    if total_weight > capacity:
        return 1.0 / (1.0 + abs(total_weight - capacity) / capacity)
    return 1.0 / (1.0 + (total_value / (20 * n)))

parameters = {'alphabet': alphabet, 'type': 'classic', 'elitism': False, 'norm': True, 'chromsize': random.randint(1,n), 'pmut': 0.2}
