import statistics

def filter_within_mad_range_and_remove_2digits(numbers):
    if not numbers:
        return numbers  # Return the original list if it's empty

    # Filter out two-digit numbers
    numbers = [x for x in numbers if x >= 100]

    if not numbers:
        return numbers  # Return the modified list if it's now empty

    median = statistics.median(numbers)
    mad = statistics.median([abs(x - median) for x in numbers])
    
    # Define the MAD multiplier (adjust this value to control the range)
    mad_multiplier = 2.0  # For example, within 2 times the MAD
    
    # Define the lower and upper limits
    lower_limit = median - mad_multiplier * mad
    upper_limit = median + mad_multiplier * mad

    # Filter the numbers within the range [lower_limit, upper_limit]
    filtered_numbers = [x for x in numbers if lower_limit <= x <= upper_limit]
    removed_numbers = [x for x in numbers if x not in filtered_numbers]
    print(f"Removed prices from : {removed_numbers}",flush=True)

    return filtered_numbers

