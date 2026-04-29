import random
import json
import os
from src import OneMax, Knapsack, GeneticAlgorithm, TournamentSelection, OnePointCrossover, BitFlipMutation

def save_results(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def run_ga_experiment(problem, name):
    print(f"\n--- Running GA for {name} ---")
    
    selection = TournamentSelection(k=3)
    crossover = OnePointCrossover(probability=0.9)
    mutation = BitFlipMutation() # Default is 1/L
    
    ga = GeneticAlgorithm(
        problem=problem,
        population_size=100,
        selection_strategy=selection,
        crossover_strategy=crossover,
        mutation_strategy=mutation,
        elitism_count=2
    )
    
    best_ind, runtime, history = ga.run(generations=300)
    
    print(f"Best Fitness: {best_ind.fitness}")
    print(f"Runtime: {runtime:.4f} seconds")
    
    return {
        "best_fitness": best_ind.fitness,
        "runtime": runtime,
        "history": history
    }

if __name__ == "__main__":
    # Ensure random seed is 42
    random.seed(42)
    
    # Initialize problems
    onemax_problem = OneMax(length=100)
    knapsack_problem = Knapsack(n=100, capacity_ratio=0.4, seed=42)
    
    results = {}
    
    # Run experiments
    results["onemax"] = run_ga_experiment(onemax_problem, "OneMax")
    results["knapsack"] = run_ga_experiment(knapsack_problem, "Knapsack")
    
    # Save to reports/results_oop.json
    report_path = os.path.join("..", "reports", "results_oop.json")
    # If running from root, path is different. Let's handle both.
    if not os.path.exists("../reports") and os.path.exists("reports"):
        report_path = os.path.join("reports", "results_oop.json")
        
    save_results(results, report_path)
    print(f"\nResults saved to {report_path}")
