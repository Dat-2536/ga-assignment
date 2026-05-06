from abc import ABC, abstractmethod
import random

class SelectionStrategy(ABC):
    """
    Interface for selection strategies.
    """
    @abstractmethod
    def select(self, population):
        """
        Select an individual from the population.
        """
        pass

class TournamentSelection(SelectionStrategy):
    """
    Tournament Selection: Select k individuals randomly and choose the best one.
    """
    def __init__(self, k=3):
        self._k = k

    def select(self, population):
        if not population:
            return None
        participants = random.sample(population, min(self._k, len(population)))
        return max(participants, key=lambda x: x.fitness)
