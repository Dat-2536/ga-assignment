from abc import ABC, abstractmethod
import random
from .chromosome import Chromosome

class CrossoverStrategy(ABC):
    """
    Interface for crossover strategies.
    """
    @abstractmethod
    def crossover(self, parent1, parent2):
        """
        Perform crossover between two parents and return two children.
        """
        pass

class OnePointCrossover(CrossoverStrategy):
    """
    One-point Crossover: Swap segments of parents at a random point.
    """
    def __init__(self, probability=0.9):
        self._probability = probability

    def crossover(self, parent1, parent2):
        # With probability P, perform crossover
        if random.random() < self._probability:
            length = len(parent1)
            if length < 2:
                return Chromosome(parent1.genes), Chromosome(parent2.genes)
            
            point = random.randint(1, length - 1)
            
            genes1 = parent1.genes
            genes2 = parent2.genes
            
            child1_genes = genes1[:point] + genes2[point:]
            child2_genes = genes2[:point] + genes1[point:]
            
            return Chromosome(child1_genes), Chromosome(child2_genes)
        
        # Otherwise, return copies of parents
        return Chromosome(parent1.genes), Chromosome(parent2.genes)
