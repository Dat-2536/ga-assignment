import time
from .population import Population

class GeneticAlgorithm:
    """
    Orchestrates the Genetic Algorithm evolution cycle.
    """
    def __init__(self, problem, population_size, selection_strategy, crossover_strategy, mutation_strategy, elitism_count=2):
        self._problem = problem
        self._population_size = population_size
        self._selection = selection_strategy
        self._crossover = crossover_strategy
        self._mutation = mutation_strategy
        self._elitism_count = elitism_count
        self._history = []

    def run(self, generations=300):
        """
        Executes the GA for a fixed number of generations.
        """
        start_time = time.time()
        
        # Initialize population
        population = Population(
            self._population_size, 
            self._problem.get_chromosome_length(), 
            self._problem
        )
        
        self._history = []
        
        for gen in range(generations):
            # Record current generation stats
            best_ind = population.get_best()
            avg_fit = population.get_average_fitness()
            self._history.append({
                "generation": gen,
                "best": best_ind.fitness,
                "average": avg_fit
            })
            
            # Sort population for elitism (best first)
            current_individuals = sorted(population.individuals, key=lambda x: x.fitness, reverse=True)
            
            # 1. Elitism: Directly pass the best e individuals to the next generation
            next_generation = current_individuals[:self._elitism_count]
            
            # 2. Reproduction: Fill the rest of the population
            while len(next_generation) < self._population_size:
                # Selection
                parent1 = self._selection.select(current_individuals)
                parent2 = self._selection.select(current_individuals)
                
                # Crossover
                child1, child2 = self._crossover.crossover(parent1, parent2)
                
                # Mutation
                child1 = self._mutation.mutate(child1)
                child2 = self._mutation.mutate(child2)
                
                # Evaluation
                child1.fitness = self._problem.evaluate(child1.genes)
                child2.fitness = self._problem.evaluate(child2.genes)
                
                # Add to next generation
                next_generation.append(child1)
                if len(next_generation) < self._population_size:
                    next_generation.append(child2)
            
            # Update population
            population.individuals = next_generation
            
        runtime = time.time() - start_time
        final_best = population.get_best()
        
        return final_best, runtime, self._history
