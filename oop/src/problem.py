from abc import ABC, abstractmethod

class Problem(ABC):
    """
    Abstract base class for Genetic Algorithm problems.
    """
    @abstractmethod
    def evaluate(self, chromosome):
        """
        Calculate the fitness of a chromosome.
        """
        pass

    @abstractmethod
    def get_chromosome_length(self):
        """
        Return the required length of the chromosome.
        """
        pass
