import random
from .chromosome import Chromosome

class Population:
    """
    Manages a collection of Chromosomes.
    """
    def __init__(self, size, chromosome_length, problem):
        self._size = size
        self._problem = problem
        self._individuals = []
        
        for _ in range(size):
            genes = [random.randint(0, 1) for _ in range(chromosome_length)]
            chromosome = Chromosome(genes)
            chromosome.fitness = self._problem.evaluate(chromosome.genes)
            self._individuals.append(chromosome)

    @property
    def individuals(self):
        """Returns an immutable view of the population to maintain encapsulation."""
        return tuple(self._individuals)

    def replace(self, new_individuals):
        """Replaces the entire population with a new set of individuals safely."""
        self._individuals = list(new_individuals)

    def get_best(self):
        """Returns the best individual in the population."""
        return max(self._individuals, key=lambda x: x.fitness)

    def get_average_fitness(self):
        """Returns the average fitness of the population."""
        if not self._individuals:
            return 0
        return sum(ind.fitness for ind in self._individuals) / len(self._individuals)

    def __len__(self):
        return len(self._individuals)
