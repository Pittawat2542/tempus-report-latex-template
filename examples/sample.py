def sample_mean(values):
    """Return the mean of a nonempty sequence."""
    if not values:
        raise ValueError("At least one value is required")
    return sum(values) / len(values)
