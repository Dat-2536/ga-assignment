import random
from functools import reduce

def initialize_population(size, length, seed=None):
    """Purely initializes a population as a tuple of tuples."""
    rng = random.Random(seed)
    return tuple(
        tuple(rng.randint(0, 1) for _ in range(length))
        for _ in range(size)
    )

def tournament_selection(population, fitnesses, k=3, seed=None):
    """Selects one individual using tournament selection."""
    rng = random.Random(seed)
    indices = rng.sample(range(len(population)), k)
    best_idx = max(indices, key=lambda i: fitnesses[i])
    return population[best_idx]

def one_point_crossover(parent1, parent2, prob=0.9, seed=None):
    """Performs one-point crossover between two parents."""
    rng = random.Random(seed)
    if rng.random() >= prob:
        return parent1, parent2
    length = len(parent1)
    if length < 2: return parent1, parent2
    point = rng.randint(1, length - 1)
    return tuple(parent1[:point] + parent2[point:]), tuple(parent2[:point] + parent1[point:])

def bitflip_mutation(chromosome, prob=None, seed=None):
    """Performs bit-flip mutation on a chromosome."""
    rng = random.Random(seed)
    p = prob if prob is not None else 1.0 / len(chromosome)
    return tuple(1 - g if rng.random() < p else g for g in chromosome)

def evolve_generation(population, fitnesses, selection_op, crossover_op, mutation_op, elitism_count=2, seed=None):
    """Evolves the population to the next generation using functional style."""
    rng = random.Random(seed)
    sorted_indices = sorted(range(len(population)), key=lambda i: fitnesses[i], reverse=True)
    elites = tuple(population[i] for i in sorted_indices[:elitism_count])
    
    num_needed = len(population) - elitism_count
    def create_offspring_pair(_):
        p1 = selection_op(population, fitnesses, seed=rng.random())
        p2 = selection_op(population, fitnesses, seed=rng.random())
        c1, c2 = crossover_op(p1, p2, seed=rng.random())
        return mutation_op(c1, seed=rng.random()), mutation_op(c2, seed=rng.random())
    
    pairs = tuple(map(create_offspring_pair, range((num_needed + 1) // 2)))
    offspring = tuple(ind for pair in pairs for ind in pair)
    return elites + offspring[:num_needed]

def run_ga_fp(initial_pop, fitness_func, selection_op, crossover_op, mutation_op, generations=300, seed=42):
    """Runs the full GA process using reduce."""
    rng = random.Random(seed)
    def generation_step(state, gen_idx):
        current_pop, history = state
        fitnesses = tuple(map(fitness_func, current_pop))
        new_history = history + ({"generation": gen_idx, "best": max(fitnesses), "average": sum(fitnesses)/len(fitnesses)},)
        next_pop = evolve_generation(current_pop, fitnesses, selection_op, crossover_op, mutation_op, seed=rng.random())
        return next_pop, new_history

    final_pop, full_history = reduce(generation_step, range(generations), (initial_pop, ()))
    final_fitnesses = tuple(map(fitness_func, final_pop))
    best_idx = max(range(len(final_pop)), key=lambda i: final_fitnesses[i])
    return final_pop[best_idx], final_fitnesses[best_idx], full_history
