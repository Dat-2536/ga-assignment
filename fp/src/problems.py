import random

def get_onemax_fitness(chromosome):
    """Pure fitness function for OneMax."""
    return sum(chromosome)

def get_knapsack_fitness(chromosome, items, capacity):
    """
    Pure fitness function for 0/1 Knapsack.
    Items: Tuple of (value, weight)
    """
    total_value = 0
    total_weight = 0
    for i, gene in enumerate(chromosome):
        if gene == 1:
            total_value += items[i][0]
            total_weight += items[i][1]
            
    if total_weight > capacity:
        return 0
    return total_value

def create_knapsack_items(n=100, seed=42):
    """Generates immutable items and capacity for Knapsack."""
    rng = random.Random(seed)
    # (value, weight)
    items = tuple(
        (rng.randint(1, 100), rng.randint(1, 50))
        for _ in range(n)
    )
    total_weight = sum(item[1] for item in items)
    capacity = total_weight * 0.4
    return items, capacity
