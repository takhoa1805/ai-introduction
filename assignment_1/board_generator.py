import random

def generate_unique_random_numbers(N):
    if N < 0:
        raise ValueError("N must be a non-negative integer.")
    
    return random.sample(range(N), N)
