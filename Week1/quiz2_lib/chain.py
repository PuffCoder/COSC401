from itertools import chain, combinations

def all_subsets(s):
    """Generate all possible subsets of the set s."""
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

s = all_subsets(["green","purple"])
for i in s:
    print(i)
