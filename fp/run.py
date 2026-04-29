import time
import json
import os
import random
from src import (
    initialize_population,
    tournament_selection,
    one_point_crossover,
    bitflip_mutation,
    run_ga_fp,
    get_onemax_fitness,
    get_knapsack_fitness,
    create_knapsack_items
)

def save_results(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def run_experiment_fp(fitness_func, length, name, seed=42):
    print(f"\n--- Running FP GA for {name} ---")
    start_time = time.time()
    
    # Initialize population
    initial_pop = initialize_population(size=100, length=length, seed=seed)
    
    # Run GA
    best_chrom, best_fit, history = run_ga_fp(
        initial_pop=initial_pop,
        fitness_func=fitness_func,
        selection_op=tournament_selection,
        crossover_op=one_point_crossover,
        mutation_op=bitflip_mutation,
        generations=300,
        seed=seed
    )
    
    runtime = time.time() - start_time
    print(f"Best Fitness: {best_fit}")
    print(f"Runtime: {runtime:.4f} seconds")
    
    return {
        "best_fitness": best_fit,
        "runtime": runtime,
        "history": list(history)
    }

if __name__ == "__main__":
    results = {}
    
    # 1. OneMax
    results["onemax"] = run_experiment_fp(
        get_onemax_fitness, 
        100, 
        "OneMax"
    )
    
    # 2. Knapsack
    items, capacity = create_knapsack_items(n=100, seed=42)
    # Create a partial function for fitness
    knapsack_fitness = lambda chrom: get_knapsack_fitness(chrom, items, capacity)
    
    results["knapsack"] = run_experiment_fp(
        knapsack_fitness,
        100,
        "Knapsack"
    )
    
    # Save to reports/results_fp.json
    report_path = os.path.join("..", "reports", "results_fp.json")
    if not os.path.exists("../reports") and os.path.exists("reports"):
        report_path = os.path.join("reports", "results_fp.json")
        
    save_results(results, report_path)
    print(f"\nResults saved to {report_path}")
