import numpy as np
from scipy.stats import gaussian_kde
from scipy.integrate import quad
import time

# Mock function to simulate one run of a benchmark
def single_benchmark_run():
    # Replace with actual logic to obtain a single performance measurement
    # Here, we simulate a single performance measurement with random variation
    return np.random.normal(loc=140000, scale=50500)


# Function to calculate KL divergence with adjustments for stability
def kl_divergence(kde_1, kde_2, num_points=100, epsilon=1e-10):
    # Estimate the range based on the KDEs’ evaluation limits
    min_value = min(kde_1.dataset.min(), kde_2.dataset.min())
    max_value = max(kde_1.dataset.max(), kde_2.dataset.max())
    
    # Define a range that spans slightly beyond the observed data in the KDEs
    range_padding = (max_value - min_value) * 0.1
    x_range = np.linspace(min_value - range_padding, max_value + range_padding, num_points)
    
    # Compute KL divergence
    return quad(lambda x: kde_1(x) * np.log((kde_1(x) + epsilon) / (kde_2(x) + epsilon)), x_range[0], x_range[-1])[0]


# Helper function to collect data for a specified time interval with sampling
def collect_data_for_interval(benchmark_function, interval_duration, sampling_portion):
    data = []
    start_time = time.time()
    
    # Loop through each hour within the interval duration
    while time.time() - start_time < interval_duration:
        # Run the benchmark only for the fraction of each hour defined by sampling_portion
        hour_start = time.time()
        sampling_duration = 3600 * sampling_portion  # Convert sampling portion to seconds
        
        while time.time() - hour_start < sampling_duration:
            data.append(benchmark_function())
        
        # Wait for the remainder of the hour if interval duration is not yet over
        while time.time() - hour_start < 3600 and time.time() - start_time < interval_duration:
            time.sleep(1)  # Sleep in 1-second increments to avoid busy waiting

    return data


def validate_stability(test_duration, benchmark_function, sampling_portion, stability_threshold, existing_kde):
    kde_1, kde_2, data_1, data_2 = collect_two_intervals(benchmark_function, test_duration, sampling_portion)

    kl_div = kl_divergence(existing_kde, kde_2)
    validate = kl_div < stability_threshold

    return validate, data_1 + data_2, kde_2


def collect_two_intervals(benchmark_function, interval_duration, sampling_portion):
    data_1 = collect_data_for_interval(benchmark_function, interval_duration, sampling_portion)
    data_2 = collect_data_for_interval(benchmark_function, interval_duration, sampling_portion)
    kde_1 = gaussian_kde(data_1)
    kde_2 = gaussian_kde(data_1 + data_2)
    return kde_1, kde_2, data_1, data_2


# PT4Cloud with time intervals of less than 7 days
def pt4cloud_lite(benchmark_function, stability_threshold=0.01, max_intervals=10, interval_duration=(60*60*24), interval_increase=0.2, sampling_portion=1.0, validate=True):

    data = []
    kde = None

    for i in range(0, max_intervals-1):
        # Increase the duration of the interval for each failed iteration
        test_duration = interval_duration + interval_duration * interval_increase * i

        # Collect data for two intervals
        kde_1, kde_2, data_1, data_2 = collect_two_intervals(benchmark_function, test_duration, sampling_portion)

        # Compute KL divergence between the two distributions
        kl_div = kl_divergence(kde_1, kde_2)

        print(f"Interval {i+1}: KL Divergence = {kl_div}")

        if kl_div < stability_threshold:
            print("Stable distribution found.")
            if(validate):
                # validate the stability of the distribution with more intervals
                is_stable, data_3, kde_3 = validate_stability(test_duration, benchmark_function, sampling_portion, stability_threshold, kde_2)
                if is_stable:
                    print("Stable distribution validated.")
                    data = data_1 + data_2 + data_3
                    kde = kde_3
                    break
            else:
                data = data_1 + data_2
                kde = kde_2
                break

    return data, kde
