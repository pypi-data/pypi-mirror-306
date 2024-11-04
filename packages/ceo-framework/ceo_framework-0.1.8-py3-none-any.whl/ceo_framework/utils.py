import numpy as np

def normalize_data(data, scale=1.0):
    """Normalizes numeric data by a given scale."""
    if isinstance(data, (int, float)):
        return data * scale
    elif isinstance(data, np.ndarray):
        return data * scale
    else:
        raise TypeError("Data must be an int, float, or np.ndarray")

def standardize_data(data):
    """Standardizes numeric data (mean = 0, std = 1) if it's a NumPy array."""
    if isinstance(data, np.ndarray):
        return (data - data.mean()) / data.std()
    else:
        raise TypeError("Data must be a NumPy array for standardization")

def text_contains_keywords(text, keywords):
    """Checks if a text contains any of the specified keywords."""
    return any(keyword.lower() in text.lower() for keyword in keywords)

def dynamic_threshold(data, factor=0.1):
    """Calculates a dynamic threshold based on the mean of data."""
    if isinstance(data, (list, np.ndarray)):
        threshold = np.mean(data) * factor
        return threshold
    else:
        raise TypeError("Data must be a list or NumPy array for dynamic thresholding")
