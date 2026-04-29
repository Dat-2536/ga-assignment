from .problem import Problem

class OneMax(Problem):
    """
    One Max Problem: Maximize the number of 1s in a binary string.
    """
    def __init__(self, length=100):
        self.length = length

    def evaluate(self, chromosome):
        """
        Fitness is the sum of bits (count of 1s).
        """
        return sum(chromosome)

    def get_chromosome_length(self):
        return self.length
