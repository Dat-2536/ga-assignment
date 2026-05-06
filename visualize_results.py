import json
import matplotlib.pyplot as plt
import os

def load_results(path):
    if not os.path.exists(path):
        print(f"Warning: {path} not found.")
        return None
    with open(path, 'r') as f:
        return json.load(f)

def plot_convergence(oop_history, fp_history, title, output_path):
    if not oop_history or not fp_history:
        return

    plt.style.use('bmh')
    plt.figure(figsize=(10, 6))
    
    gen_oop = [h['generation'] for h in oop_history]
    best_oop = [h['best'] for h in oop_history]
    avg_oop = [h['average'] for h in oop_history]
    
    gen_fp = [h['generation'] for h in fp_history]
    best_fp = [h['best'] for h in fp_history]
    avg_fp = [h['average'] for h in fp_history]
    
    plt.plot(gen_oop, best_oop, label='OOP - Best', color='#2c3e50', linewidth=2.5)
    plt.plot(gen_fp, best_fp, label='FP - Best', color='#e74c3c', linestyle='--', linewidth=2.5)
    
    plt.plot(gen_oop, avg_oop, color='#2c3e50', alpha=0.3, linewidth=1, label='OOP - Average')
    plt.plot(gen_fp, avg_fp, color='#e74c3c', alpha=0.3, linewidth=1, linestyle='--', label='FP - Average')
    
    plt.title(f'GA Convergence: {title}', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Generation', fontsize=12)
    plt.ylabel('Fitness Score', fontsize=12)
    plt.legend(frameon=True, shadow=True)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Successfully generated plot: {output_path}")

if __name__ == "__main__":
    results_dir = "reports"
    oop_file = os.path.join(results_dir, "results_oop.json")
    fp_file = os.path.join(results_dir, "results_fp.json")
    
    oop_data = load_results(oop_file)
    fp_data = load_results(fp_file)
    
    if oop_data and fp_data:
        plot_convergence(
            oop_data['onemax']['history'],
            fp_data['onemax']['history'],
            "OneMax Problem",
            os.path.join(results_dir, "onemax_curve.png")
        )
        
        plot_convergence(
            oop_data['knapsack']['history'],
            fp_data['knapsack']['history'],
            "0/1 Knapsack Problem",
            os.path.join(results_dir, "knapsack_curve.png")
        )
