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
        
        # Mutation should not change original
        bitflip_mutation(p1, prob=1.0, seed=42)
        self.assertEqual(p1, p1_snapshot, "Chromosome was mutated by mutation function!")

if __name__ == '__main__':
    unittest.main()
