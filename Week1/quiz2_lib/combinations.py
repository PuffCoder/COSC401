
from itertools import combinations

# Define the iterable
iterable = [1, 2, 3]

# Length of the combinations
r = 2

# Generate combinations of length r from the iterable
comb = combinations(iterable, r)

# Print each combination
for c in comb:
    print(c)
