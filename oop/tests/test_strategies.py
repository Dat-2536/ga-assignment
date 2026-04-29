import unittest
import random
from src import (
    Chromosome, 
    TournamentSelection, 
    OnePointCrossover, 
    BitFlipMutation
)

class TestStrategies(unittest.TestCase):
    """
    Tests for GA strategies (Selection, Crossover, Mutation).
    """
    def setUp(self):
        random.seed(42)

    def test_chromosome_encapsulation(self):
        genes = [1, 0, 1]
        c = Chromosome(genes)
        # Check if genes property returns a copy
        genes_copy = c.genes
        genes_copy[0] = 0
        self.assertEqual(c.genes[0], 1) # Original should not change

    def test_tournament_selection(self):
        c1 = Chromosome([1])
        c1.fitness = 10
        c2 = Chromosome([0])
        c2.fitness = 50
        c3 = Chromosome([1])
        c3.fitness = 20
        
        population = [c1, c2, c3]
        selection = TournamentSelection(k=3)
        
        # In a tournament of 3 with these 3, c2 must win
        selected = selection.select(population)
        self.assertEqual(selected.fitness, 50)

    def test_one_point_crossover(self):
        p1 = Chromosome([0, 0, 0, 0, 0])
        p2 = Chromosome([1, 1, 1, 1, 1])
        
        # Force crossover with probability 1.0
        crossover = OnePointCrossover(probability=1.0)
        child1, child2 = crossover.crossover(p1, p2)
        
        self.assertEqual(len(child1), 5)
        self.assertEqual(len(child2), 5)
        
        # Check if they are different from parents
        self.assertNotEqual(child1.genes, p1.genes)
        self.assertNotEqual(child1.genes, p2.genes)
        
        # Total number of 1s in children should equal total 1s in parents (5)
        self.assertEqual(sum(child1.genes) + sum(child2.genes), 5)

    def test_bit_flip_mutation(self):
        c = Chromosome([0, 0, 0, 0, 0])
        # Force mutation on every bit
        mutation = BitFlipMutation(gene_mutation_prob=1.0)
        mutated = mutation.mutate(c)
        
        self.assertEqual(mutated.genes, [1, 1, 1, 1, 1])

if __name__ == '__main__':
    unittest.main()
