import random
from .problem import Problem

class Knapsack(Problem):
    """
    0/1 Knapsack Problem:
    Maximize total value of items without exceeding capacity.
    """
    def __init__(self, n=100, capacity_ratio=0.4, seed=42):
        self.n = n
        # Use a local random instance to not affect global state if needed, 
        # but here we follow the "seed chung là 42" requirement.
        random.seed(seed)
        
        # Initialize 100 items with random values and weights
        self.items = []
        for _ in range(n):
            self.items.append({
                'value': random.randint(1, 100),
                'weight': random.randint(1, 50)
            })
            
        # Capacity is 40% of total weight
        total_weight = sum(item['weight'] for item in self.items)
        self.capacity = total_weight * capacity_ratio

    def evaluate(self, chromosome):
        """
        Fitness is total value. If total weight exceeds capacity, fitness is 0.
        """
        total_value = 0
        total_weight = 0
        
        for i in range(self.n):
            if chromosome[i] == 1:
                total_value += self.items[i]['value']
                total_weight += self.items[i]['weight']
                
        if total_weight > self.capacity:
            return 0
            
        return total_value

    def get_chromosome_length(self):
        return self.n
