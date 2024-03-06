# Import necessary lib
from itertools import chain, combinations

# all possible set
def all_subsets(s):
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

# check element x whether in the subset
# return (T,F)
def all_possible_functions(X):
    functions = set()

    for subset in all_subsets(X):
        def func(x, subset=set(subset)):
            return x in subset
        functions.add(func)

    return functions

# Global variables
X = {"green", "purple"} # an input space with two elements
D = {("green", True)} # the training data is a subset of X * {True, False}
F = all_possible_functions(X)
H = F # H must be a subset of (or equal to) F

def version_space(H,D):
    """

    Args:
        H (_type_): A set of hypotheses, where each hypothesis is a function that takes an input and reutrn True or False
        D (_type_): A set of 2-tuples, where each tuple is an (input, output) pair.
    """
    # Initialize the version space as an empty set
    VS = set()

    # Iterate throught each hypothesis in H
    for hypothesis in H:
        # Assum the hypothesis is consistent until proven otherwise
        consistent = True
        
        # Checko the hypothesis against each (input,output) pair in D
        for x,y in D:
            # If the hypothesis does not correctly classify an example, mark it as inconsistent
            if hypothesis(x) != y:
                consistent = False
                break
        if consistent:
            VS.add(hypothesis)
    return VS
    
    
VS = version_space(H, D)

for i in VS:
    print(i)
print(len(VS))

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