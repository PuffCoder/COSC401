from itertools import chain, combinations

def all_subsets(s):
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def all_possible_functions(X):
    functions = set()

    for subset in all_subsets(X):
        def func(x, subset=set(subset)):
            return x in subset
        functions.add(func)

    return functions


def version_space(H, D):
    VS = set()
    for hypothesis in H:
        consistent = True
        for x, y in D:
            if hypothesis(x) != y:
                consistent = False
                break  # No need to check further for this hypothesis
        if consistent:
            VS.add(hypothesis)
    return VS



D = {
    ((False, True), False),
    ((True, True), True),
}

def h1(x): return True
def h2(x): return False
def h3(x): return x[0] and x[1]
def h4(x): return x[0] or x[1]
def h5(x): return x[0]
def h6(x): return x[1]

H = {h1, h2, h3, h4, h5, h6}

VS = version_space(H, D)
print(sorted(h.__name__ for h in VS))

for h in VS:
    for x, y in D:
        if h(x) != y:
            print("You have a hypothesis in VS that does not agree with the set D!")
            break
    else:
        continue
    break
else:
    print("OK")