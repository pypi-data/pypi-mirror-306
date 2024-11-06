import numpy as np
from scipy.stats import gaussian_kde
from scipy.integrate import quad
import time


def kl_divergence(kde_1, kde_2, num_points=100, epsilon=1e-10):
    """
    Calculate the Kullback-Leibler divergence between two kernel density estimates.
    
    Args:
        kde_1 (scipy.stats.gaussian_kde): First kernel density estimate
        kde_2 (scipy.stats.gaussian_kde): Second kernel density estimate
        num_points (int, optional): Number of points to use in the numerical integration. Defaults to 100
        epsilon (float, optional): Small constant added to prevent numerical instability. Defaults to 1e-10
        
    Returns:
        float: The KL divergence value between the two distributions
        
    Notes:
        - The function adds padding to the range of integration to ensure proper coverage
        - Uses numerical integration via scipy.integrate.quad
        - Adds epsilon to prevent log(0) scenarios
    """

    # Estimate the range based on the KDEs’ evaluation limits
    min_value = min(kde_1.dataset.min(), kde_2.dataset.min())
    max_value = max(kde_1.dataset.max(), kde_2.dataset.max())
    
    # Define a range that spans slightly beyond the observed data in the KDEs
    range_padding = (max_value - min_value) * 0.1
    x_range = np.linspace(min_value - range_padding, max_value + range_padding, num_points)
    
    return quad(lambda x: kde_1(x) * np.log((kde_1(x) + epsilon) / (kde_2(x) + epsilon)), x_range[0], x_range[-1])[0]


def collect_data_for_interval(benchmark_function, interval_duration, sampling_portion):
    """
    Collect benchmark data for a specified time interval using periodic sampling.
    
    Args:
        benchmark_function (callable): Function that returns a single benchmark measurement
        interval_duration (float): Total duration to collect data in seconds
        sampling_portion (float): Fraction of the interval to spend collecting samples (0.0 to 1.0)
        
    Returns:
        list: Collected benchmark measurements
        
    Notes:
        - Actively collects samples during sampling_portion of the interval
        - Adapts to long-running benchmark functions
        - Ensures sampling_portion is respected over the total interval
        - Sleeps during non-sampling periods to reduce system load
    """
    data = []
    start_time = time.time()
    total_active_time = 0
    
    while time.time() - start_time < interval_duration:
        # Calculate whether we should run another benchmark
        elapsed_total = time.time() - start_time
        target_active_time = elapsed_total * sampling_portion
        
        if total_active_time < target_active_time:
            # Run benchmark and track how long it took
            benchmark_start = time.time()
            data.append(benchmark_function())
            benchmark_duration = time.time() - benchmark_start
            total_active_time += benchmark_duration
            
        else:
            sleep_duration = min(
                1.0,  # Maximum sleep of 1 second
                (total_active_time - target_active_time) / sampling_portion
            )
            time.sleep(sleep_duration)
    
    return data


def validate_stability(test_duration, benchmark_function, sampling_portion, stability_threshold, existing_kde):
    """
    Validate the stability of a performance distribution by comparing it with new data.
    
    Args:
        test_duration (float): Duration of the test interval in seconds
        benchmark_function (callable): Function that returns a single benchmark measurement
        sampling_portion (float): Fraction of each hour to spend collecting samples (0.0 to 1.0)
        stability_threshold (float): Maximum allowed KL divergence to consider distribution stable
        existing_kde (scipy.stats.gaussian_kde): Existing kernel density estimate to compare against
        
    Returns:
        tuple: (
            bool: True if distribution is stable, False otherwise,
            list: Combined data from both collection intervals,
            scipy.stats.gaussian_kde: Updated kernel density estimate
        )
    """

    kde_1, kde_2, data_1, data_2 = collect_two_intervals(benchmark_function, test_duration, sampling_portion)

    kl_div = kl_divergence(existing_kde, kde_2)
    validate = kl_div < stability_threshold

    return validate, data_1 + data_2, kde_2


def collect_two_intervals(benchmark_function, interval_duration, sampling_portion):
    """
    Collect benchmark data over two consecutive intervals and compute their distributions.
    
    Args:
        benchmark_function (callable): Function that returns a single benchmark measurement
        interval_duration (float): Duration of each interval in seconds
        sampling_portion (float): Fraction of each hour to spend collecting samples (0.0 to 1.0)
        
    Returns:
        tuple: (
            scipy.stats.gaussian_kde: KDE for first interval,
            scipy.stats.gaussian_kde: KDE for combined intervals,
            list: Data from first interval,
            list: Data from second interval
        )
    """

    data_1 = collect_data_for_interval(benchmark_function, interval_duration, sampling_portion)
    data_2 = collect_data_for_interval(benchmark_function, interval_duration, sampling_portion)
    kde_1 = gaussian_kde(data_1)
    kde_2 = gaussian_kde(data_1 + data_2)
    return kde_1, kde_2, data_1, data_2


def pt4cloud_lite(benchmark_function, stability_threshold=0.01, max_intervals=10, interval_duration=(60*60*24), interval_increase=0.2, sampling_portion=1.0, validate=True):
    """
    Performance Testing for Cloud (Lite Version) - Analyzes performance stability over time.
    
    Args:
        benchmark_function (callable): Function that returns a single benchmark measurement
        stability_threshold (float, optional): Maximum KL divergence to consider distribution stable. 
            Defaults to 0.01
        max_intervals (int, optional): Maximum number of intervals to try before giving up. 
            Defaults to 10
        interval_duration (int, optional): Base duration of each interval in seconds. 
            Defaults to 24 hours
        interval_increase (float, optional): Factor to increase interval duration by after each 
            failed attempt. Defaults to 0.2
        sampling_portion (float, optional): Fraction of each hour to spend collecting samples 
            (0.0 to 1.0). Defaults to 1.0
        validate (bool, optional): Whether to perform additional validation of stability. 
            Defaults to True
            
    Returns:
        tuple: (
            list: All collected benchmark measurements,
            scipy.stats.gaussian_kde: Final kernel density estimate of the stable distribution
        )
        
    Notes:
        - Designed for performance testing intervals of less than 7 days
        - Uses KL divergence to measure distribution stability
        - Progressively increases interval duration until stability is achieved
        - Can perform additional validation of stability if requested
        - Returns None for both values if stability is not achieved within max_intervals
    """

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
                    kde = gaussian_kde(data)
                    break
            else:
                data = data_1 + data_2
                kde = kde_2
                break

    return data, kde
