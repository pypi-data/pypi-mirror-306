import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from scipy.integrate import quad

# Mock function to simulate performance test data collection
def run_performance_tests():
    # Replace with actual data collection logic
    # Here, we simulate performance data with random variation
    return np.random.normal(loc=140000, scale=5500, size=100)

# Function to calculate KL divergence with adjustments for stability
def kl_divergence(p, q, x_range, epsilon=1e-10):
    return quad(lambda x: p(x) * np.log((p(x) + epsilon) / (q(x) + epsilon)), x_range[0], x_range[-1])[0]


# PT4Cloud simplified function
def pt4cloud(stability_threshold = 0.01, max_intervals = 10):
    interval_data = []
    
    # Run initial test to create first KDE distribution
    data_1 = run_performance_tests()
    kde_1 = gaussian_kde(data_1)
    interval_data.append(data_1)
    
    for i in range(1, max_intervals):
        # Run another test to create second KDE distribution
        data_2 = run_performance_tests()
        interval_data.append(data_2)

        kde_2 = gaussian_kde(data_2)
        
        # Create a common range for KDE comparison
        x_range = np.linspace(min(data_1 + data_2) - 0.5, max(data_1 + data_2) + 0.5, 100)
        
        # Compute KL divergence between the two distributions
        kl_div = kl_divergence(lambda x: kde_1(x), lambda x: kde_2(x), x_range)
        
        print(f"Interval {i}: KL Divergence = {kl_div}")
        
        # If distributions are stable, break
        if kl_div < stability_threshold:
            print("Stable distribution found.")
            break
        
        # Update kde_1 with kde_2 for next comparison
        kde_1 = kde_2
        data_1 = data_2

    # Combine all data and show final KDE plot
    combined_data = np.concatenate(interval_data)
    report_performance_summary(combined_data)

def report_performance_summary(combined_data):
    # Compute final KDE
    kde = gaussian_kde(combined_data)

    # Define a range to evaluate the KDE
    x_range = np.linspace(min(combined_data) - 0.5, max(combined_data) + 0.5, 100)
    kde_values = kde(x_range)

    # Compute key metrics
    mean_performance = np.mean(combined_data)
    median_performance = np.median(combined_data)
    percentile_5 = np.percentile(combined_data, 5)
    percentile_50 = np.percentile(combined_data, 50)
    percentile_95 = np.percentile(combined_data, 95)

    # Report performance summary
    print("Performance Summary:")
    print(f"Mean Performance: {mean_performance:.2f}")
    print(f"Median Performance: {median_performance:.2f}")
    print(f"5th Percentile (Worst-case): {percentile_5:.2f}")
    print(f"50th Percentile (Typical): {percentile_50:.2f}")
    print(f"95th Percentile (Best-case): {percentile_95:.2f}")

    # Plot KDE with histogram
    plt.hist(combined_data, bins=20, density=True, alpha=0.3, label="Data Histogram")
    plt.plot(x_range, kde_values, label="Final KDE Estimate", color='blue')
    plt.axvline(percentile_5, color='red', linestyle='--', label="5th Percentile")
    plt.axvline(percentile_50, color='green', linestyle='--', label="50th Percentile")
    plt.axvline(percentile_95, color='purple', linestyle='--', label="95th Percentile")
    plt.xlabel('Performance Metric')
    plt.ylabel('Density')
    plt.legend()
    plt.title('Final Performance Distribution with Key Metrics')
    plt.show()

# Run the PT4Cloud function
pt4cloud()