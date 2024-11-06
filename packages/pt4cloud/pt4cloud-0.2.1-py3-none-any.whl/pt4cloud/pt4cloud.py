import numpy as np
from scipy.stats import gaussian_kde
from scipy.integrate import quad
import time

def pt4cloud(benchmark_function, stability_threshold=0.01, max_intervals=10, 
             interval_duration=(60*60*24*7), sampling_portion=1.0):
    """
    Performance Testing for Cloud - Analyzes performance stability over extended periods.
    
    Args:
        benchmark_function (callable): Function that returns a single benchmark measurement
        stability_threshold (float, optional): Maximum KL divergence to consider distribution stable. 
            Defaults to 0.01
        max_intervals (int, optional): Maximum number of intervals to try before giving up. 
            Defaults to 10
        interval_duration (int, optional): Base duration of each interval in seconds. 
            Defaults to 7 days
        sampling_portion (float, optional): Fraction of time to spend collecting samples 
            (0.0 to 1.0). Defaults to 1.0
            
    Returns:
        tuple: (
            list: All collected benchmark measurements,
            scipy.stats.gaussian_kde: Final kernel density estimate of the stable distribution
        )
    """
    # Step 1-1: Execute tests for first interval
    print("Step 1-1: Collecting first interval samples...")
    s1 = collect_extended_interval(benchmark_function, interval_duration, sampling_portion)
    
    # Step 1-2: Calculate performance distribution
    print("Step 1-2: Calculating first distribution...")
    d1 = calculate_distribution(s1)
    
    for iteration in range(max_intervals):
        # Step 2-1: Execute tests for another interval
        print(f"Step 2-1: Collecting interval {iteration + 2} samples...")
        s2 = collect_extended_interval(benchmark_function, interval_duration, sampling_portion)
        
        # Step 2-2: Combine samples and calculate new distribution
        print("Step 2-2: Calculating combined distribution...")
        s = s1 + s2
        d2 = calculate_distribution(s)
        
        # Step 3: Compare distributions
        kl_div = calculate_kl_divergence(d1, d2)
        print(f"Step 3: KL Divergence = {kl_div}")
        
        if kl_div < stability_threshold:
            print("Stable distribution found.")
            return s, d2
        
        # Step 4: Update for next iteration
        print("Step 4: Updating samples and distribution for next iteration...")
        s1 = s
        d1 = d2
    
    print("Warning: Maximum iterations reached without achieving stability")
    return s1, d1

def collect_extended_interval(benchmark_function, interval_duration, sampling_portion):
    """
    Collect benchmark data over an extended time interval.
    """
    data = []
    start_time = time.time()
    total_active_time = 0
    
    while time.time() - start_time < interval_duration:
        elapsed_total = time.time() - start_time
        target_active_time = elapsed_total * sampling_portion
        
        if total_active_time < target_active_time:
            benchmark_start = time.time()
            data.append(benchmark_function())
            total_active_time += time.time() - benchmark_start
        else:
            sleep_duration = min(
                60.0,  # Maximum sleep of 60 seconds for long intervals
                (total_active_time - target_active_time) / sampling_portion
            )
            time.sleep(sleep_duration)
    
    return data

def calculate_distribution(samples):
    """
    Calculate the kernel density estimate from samples.
    """
    return gaussian_kde(samples)

def calculate_kl_divergence(dist1, dist2, num_points=1000, epsilon=1e-10):
    """
    Calculate KL divergence between two distributions.
    """
    min_value = min(dist1.dataset.min(), dist2.dataset.min())
    max_value = max(dist1.dataset.max(), dist2.dataset.max())
    
    range_padding = (max_value - min_value) * 0.1
    x_range = np.linspace(min_value - range_padding, max_value + range_padding, num_points)
    
    return quad(lambda x: dist1(x) * np.log((dist1(x) + epsilon) / (dist2(x) + epsilon)), 
               x_range[0], x_range[-1])[0]