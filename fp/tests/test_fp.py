import unittest
from src import (
    get_onemax_fitness,
    tournament_selection,
    one_point_crossover,
    bitflip_mutation,
    initialize_population
)

class TestFPGA(unittest.TestCase):
    """
    Unit tests for Functional Programming GA implementation.
    Focus on pure functions and immutability.
    """

    def test_onemax_fitness(self):
        self.assertEqual(get_onemax_fitness((1, 1, 0, 1)), 3)
        self.assertEqual(get_onemax_fitness((0, 0, 0)), 0)

    def test_knapsack_fitness_valid_and_over_capacity(self):
        from src.problems import get_knapsack_fitness
        items = ((10, 5), (20, 10), (30, 20)) # (value, weight)
        capacity = 15
        # (1, 1, 0) -> weight 15 <= 15 -> value 30
        self.assertEqual(get_knapsack_fitness((1, 1, 0), items, capacity), 30)
        # (1, 1, 1) -> weight 35 > 15 -> value 0
        self.assertEqual(get_knapsack_fitness((1, 1, 1), items, capacity), 0)

    def test_knapsack_item_generation_reproducibility(self):
        from src.problems import create_knapsack_items
        items1, cap1 = create_knapsack_items(10, seed=42)
        items2, cap2 = create_knapsack_items(10, seed=42)
        self.assertEqual(items1, items2)
        self.assertEqual(cap1, cap2)

    def test_tournament_selection(self):
        population = ((0, 0), (1, 1), (0, 1))
        fitnesses = (0, 2, 1)
        # If k=3, the best (1, 1) must be selected
        selected = tournament_selection(population, fitnesses, k=3, seed=42)
        self.assertEqual(selected, (1, 1))

    def test_one_point_crossover(self):
        p1 = (0, 0, 0, 0)
        p2 = (1, 1, 1, 1)
        c1, c2 = one_point_crossover(p1, p2, prob=1.0, seed=1)
        
        self.assertEqual(len(c1), 4)
        self.assertEqual(len(c2), 4)
        # Children should be a mix of parents
        self.assertTrue(0 in c1 and 1 in c1)
        self.assertTrue(0 in c2 and 1 in c2)
        # Total sum should be conserved
        self.assertEqual(sum(c1) + sum(c2), 4)

    def test_bitflip_mutation(self):
        chromosome = (0, 0, 0)
        # Force mutation on all bits
        mutated = bitflip_mutation(chromosome, prob=1.0, seed=42)
        self.assertEqual(mutated, (1, 1, 1))
        # Ensure original is not changed (redundant due to tuple but good for logic)
        self.assertEqual(chromosome, (0, 0, 0))

    def test_immutability_guarantee(self):
        """
        Special test to confirm that no input data is mutated.
        """
        # 1. Population immutability
        initial_pop = ((0, 0), (1, 1))
        pop_snapshot = tuple(initial_pop) # Deep copy of the outer tuple
        
        # Selection should not change population
        tournament_selection(initial_pop, (0, 1), k=2, seed=42)
        self.assertEqual(initial_pop, pop_snapshot, "Population was mutated by selection!")
        
        # 2. Chromosome immutability
        p1 = (0, 0, 0, 0)
        p1_snapshot = tuple(p1)
        p2 = (1, 1, 1, 1)
        p2_snapshot = tuple(p2)
        
        # Crossover should not change parents
        one_point_crossover(p1, p2, prob=1.0, seed=42)
        self.assertEqual(p1, p1_snapshot, "Parent 1 was mutated by crossover!")
        self.assertEqual(p2, p2_snapshot, "Parent 2 was mutated by crossover!")
        
    def test_evolution_improvement(self):
        """
        Tests if the FP GA improves fitness over generations.
        """
        from src import run_ga_fp, create_knapsack_items
        
        # Using OneMax for quick test
        initial_pop = initialize_population(size=20, length=20, seed=42)
        _, _, history = run_ga_fp(
            initial_pop=initial_pop,
            fitness_func=get_onemax_fitness,
            selection_op=tournament_selection,
            crossover_op=one_point_crossover,
            mutation_op=bitflip_mutation,
            generations=10,
            seed=42
        )
        
        # Assert that the best fitness in the last generation is >= the first
        self.assertGreaterEqual(history[-1]['best'], history[0]['best'])
        # For 10 generations on length 20, it should typically improve
        self.assertGreater(history[-1]['best'], history[0]['best'])

if __name__ == '__main__':
    unittest.main()
