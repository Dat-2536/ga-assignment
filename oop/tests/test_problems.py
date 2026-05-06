import unittest
from src import OneMax, Knapsack

class TestProblems(unittest.TestCase):
    """
    Tests for GA problem definitions (OneMax and Knapsack).
    """
    def test_onemax_fitness(self):
        problem = OneMax(length=10)
        chromosome = [1, 1, 0, 1, 0, 1, 0, 1, 1, 0]
        self.assertEqual(problem.evaluate(chromosome), 6)
        
    def test_onemax_length(self):
        problem = OneMax(length=50)
        self.assertEqual(problem.get_chromosome_length(), 50)

    def test_knapsack_initialization(self):
        p1 = Knapsack(n=10, seed=42)
        p2 = Knapsack(n=10, seed=42)
        self.assertEqual(p1.items, p2.items)
        self.assertEqual(p1.capacity, p2.capacity)

    def test_knapsack_global_random_state(self):
        import random
        state_before = random.getstate()
        
        Knapsack(n=10, seed=42)
        
        state_after = random.getstate()
        self.assertEqual(state_before, state_after, "Knapsack initialization mutated global random state!")

    def test_knapsack_evaluation(self):
        problem = Knapsack(n=5, seed=42)
        self.assertEqual(problem.evaluate([0, 0, 0, 0, 0]), 0)
        
        heavy_chromosome = [1] * 5 
        total_weight = sum(item['weight'] for item in problem.items)
        if total_weight > problem.capacity:
            self.assertEqual(problem.evaluate(heavy_chromosome), 0)

if __name__ == '__main__':
    unittest.main()
