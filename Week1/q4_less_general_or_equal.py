def less_general_or_equal(ha, hb, X):
    """
    Determine if hypothesis ha is less general or equal to hypothesis hb given the input space X.

    Parameters:
    - ha: A hypothesis function that takes an input from X and returns True or False.
    - hb: Another hypothesis function with the same signature as ha.
    - X: The input space, a list of elements that can be consumed by both hypotheses.

    Returns:
    - True if ha is less general or equal to hb; False otherwise.
    """
    for x in X:
        if ha(x) and not hb(x):  # If ha is True but hb is False for any x, ha is not less general or equal to hb
            return False
    # If we never find an x for which ha is True and hb is False, then ha is less general or equal to hb
    return True 

# Example usage:
X = list(range(1000))

def h2(x): return x % 2 == 0
def h3(x): return x % 3 == 0
def h6(x): return x % 6 == 0

H = [h2, h3, h6]

for ha in H:
    for hb in H:
        print(ha.__name__, "<=", hb.__name__, "?", less_general_or_equal(ha, hb, X))
