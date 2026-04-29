class Chromosome:
    """
    Encapsulates the genetic data (genes) and its fitness value.
    """
    def __init__(self, genes):
        self._genes = list(genes)
        self._fitness = 0.0

    @property
    def genes(self):
        """Returns a copy of the genes to maintain encapsulation."""
        return list(self._genes)

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, value):
        self._fitness = value

    def __len__(self):
        return len(self._genes)

    def __getitem__(self, index):
        return self._genes[index]

    def __repr__(self):
        return f"Chromosome(fitness={self._fitness})"
