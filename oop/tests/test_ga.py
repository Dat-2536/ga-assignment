import unittest
import random
from src import (
    OneMax, 
    GeneticAlgorithm, 
    TournamentSelection, 
    OnePointCrossover, 
    BitFlipMutation
)
from src.population import Population

class TestPopulationEncapsulation(unittest.TestCase):
    def test_individuals_immutability(self):
        problem = OneMax(length=10)
        pop = Population(size=5, chromosome_length=10, problem=problem)
        
        inds = pop.individuals
        
        self.assertIsInstance(inds, tuple)
        
        with self.assertRaises(TypeError):
            inds[0] = "mutated"

class TestGAImprovement(unittest.TestCase):
    """
    Tests if the GA actually improves fitness over generations.
    """
    def test_onemax_evolution(self):
        random.seed(42)
        problem = OneMax(length=50)
        
        ga = GeneticAlgorithm(
            problem=problem,
            population_size=50,
            selection_strategy=TournamentSelection(k=3),
            crossover_strategy=OnePointCrossover(0.9),
            mutation_strategy=BitFlipMutation(),
            elitism_count=2
        )
        
        best_ind, runtime, history = ga.run(generations=20)
        
        first_gen_best = history[0]['best']
        last_gen_best = history[-1]['best']
        
        self.assertGreaterEqual(last_gen_best, first_gen_best)
        self.assertGreater(last_gen_best, first_gen_best)

    def test_ga_generations_count(self):
        problem = OneMax(length=10)
        ga = GeneticAlgorithm(problem, 10, TournamentSelection(), OnePointCrossover(), BitFlipMutation())
        _, _, history = ga.run(generations=50)
        self.assertEqual(len(history), 50)

if __name__ == '__main__':
    unittest.main()
