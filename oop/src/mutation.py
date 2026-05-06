from abc import ABC, abstractmethod
import random
from .chromosome import Chromosome

class MutationStrategy(ABC):
    """
    Interface for mutation strategies.
    """
    @abstractmethod
    def mutate(self, chromosome):
        """
        Perform mutation on a chromosome.
        """
        pass

class BitFlipMutation(MutationStrategy):
    """
    Bit-flip Mutation: Flip bits with a certain probability.
    """
    def __init__(self, gene_mutation_prob=None):
        self._gene_mutation_prob = gene_mutation_prob

    def mutate(self, chromosome):
        genes = chromosome.genes
        length = len(genes)
        
        prob = self._gene_mutation_prob if self._gene_mutation_prob is not None else 1.0 / length
        
        mutated_genes = []
        for gene in genes:
            if random.random() < prob:
                mutated_genes.append(1 - gene)
            else:
                mutated_genes.append(gene)
                
        return Chromosome(mutated_genes)
