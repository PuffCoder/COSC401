def less_general_or_equal(ha, hb, X):
    for x in X:
        if ha(x) and not hb(x):  
            return False
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
