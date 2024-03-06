
def initial_S(domains):
    """Initial members of S as the most specific hypothesis."""
    # Correctly return a set containing the most specific hypothesis
    return {tuple('None' for _ in domains)}  # Each feature has 'None' indicating no generalization
    
def initial_G(domains):
    """Initial members of G as the most general hypothesis."""
    # Correctly return a set containing the most general hypothesis
    return {tuple('?' for _ in domains)}  # '?' indicates any value is acceptable for each feature

def match(code, x):
    """Takes a code and returns True if the corresponding hypothesis returns True (positive) for the given input."""
    return decode(code)(x)

def decode(code):
    """Takes a code and returns the corresponding hypothesis."""
    def h(x):
        # Returns True if all constraints in code match the corresponding values in x, or if the constraint is '?'
        return all(c == '?' or c == xi for c, xi in zip(code, x))
    return h

def minimal_generalisations(code, x):
    """Generalise the hypothesis minimally so that it matches x."""
    generalisations = set()
    for i, (c, xi) in enumerate(zip(code, x)):
        if c == 'None' or c == xi:
            new_code = list(code)
            new_code[i] = xi
            generalisations.add(tuple(new_code))
        elif c == '?':
            continue
        else:
            new_code = list(code)
            new_code[i] = '?'
            generalisations.add(tuple(new_code))
    return generalisations

def minimal_specialisations(code, domains, x):
    """Specialise the hypothesis minimally so that it does not match x."""
    specialisations = set()
    for i, (c, xi) in enumerate(zip(code, x)):
        if c == '?':
            for v in domains[i]:
                if v != xi:
                    new_code = list(code)
                    new_code[i] = v
                    specialisations.add(tuple(new_code))
    return specialisations

def all_agree(S, G, x):
    """
    Determines if all hypotheses in the version space agree on the classification of x.
    
    Parameters:
    - S: A set of the most specific hypotheses.
    - G: A set of the most general hypotheses.
    - x: An input example to classify.
    
    Returns:
    - True if all hypotheses agree on the classification of x; False otherwise.
    """
    # Determine the classification of x according to S and G
    classifications = {match(s, x) for s in S}.union({match(g, x) for g in G})
    
    # If all hypotheses agree, there will only be one classification (True or False)
    return len(classifications) == 1

def cea_trace(domains, training_examples):
    S_trace, G_trace = [], []
    S = initial_S(domains)  # Initialize S with the most specific hypothesis
    G = initial_G(domains)  # Initialize G with the most general hypothesis
    
    # Append initial S and G to their respective traces
    S_trace.append({S})
    G_trace.append({G})
 
    for x, y in training_examples:
        if y:  # Positive example
            G = {g for g in G if match(g, x)}  # Remove non-matching hypotheses from G
            new_S = set()
            for s in S:
                if not match(s, x):
                    new_S = new_S.union(minimal_generalisations(s, x, domains))
                else:
                    new_S.add(s)
            S = {s for s in new_S if any(match(g, s) for g in G)}
        else:  # Negative example
            S = {s for s in S if not match(s, x)}  # Remove matching hypotheses from S
            new_G = set()
            for g in G:
                if match(g, x):
                    new_G = new_G.union(minimal_specialisations(g, domains, x))
                else:
                    new_G.add(g)
            G = {g for g in new_G if any(match(s, g) for s in S)}
        
        # Append the current S and G to their traces
        S_trace.append(S)
        G_trace.append(G)

    return S_trace, G_trace


domains = [
    {'red', 'blue'},
]

training_examples = [
    (('red',), True),
]

S_trace, G_trace = cea_trace(domains, training_examples)
S, G = S_trace[-1], G_trace[-1]
print(all_agree(S, G, ('red',)))  # Expected to print True or False based on whether all agree
print(all_agree(S, G, ('blue',)))  # Expected to print True or False based on whether all agree
