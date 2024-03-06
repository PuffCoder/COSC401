def decode(code):
    """Takes a code and returns the corresponding hypothesis."""
    def h(x):
        return all(c == '?' or c == xi for c, xi in zip(code, x))
    return h
        
def match(code, x):
    """Takes a code and returns True if the corresponding hypothesis returns
    True (positive) for the given input."""
    return decode(code)(x)

def all_agree(S, G, x):
    """
    Determines whether all hypotheses in the version space agree on the classification of x.
    
    Parameters:
    - S: The final set of the most specific hypotheses.
    - G: The final set of the most general hypotheses.
    - x: An input point to classify.
    
    Returns:
    - True if all hypotheses agree on the classification of x; False otherwise.
    """
    s_pred = set(match(s, x) for s in S)
    g_pred = set(match(g, x) for g in G)

    # If there's only one unique prediction across S and G, then they all agree.
    return len(s_pred.union(g_pred)) == 1

def cea_trace(domains, training_examples):
    S = {tuple(['None'] * len(domains))}  # Initialize S with the most specific hypothesis.
    G = {tuple(['?'] * len(domains))}     # Initialize G with the most general hypothesis.
    
    S_trace = [S]
    G_trace = [G]

    for x, label in training_examples:
        if label:  # Positive example
            S = {s for s in S if match(s, x)}
            G = {g for g in G if match(g, x)} if S else G
        else:  # Negative example
            G = {g for g in G if not match(g, x)}
            S = {s for s in S if not match(s, x)} if G else S

        # Ensure S and G are within each other's bounds after each update.
        S_trace.append(S)
        G_trace.append(G)

    return S_trace, G_trace


domains = [{'red', 'blue'}]

training_examples = [(('red',), True)]

S_trace, G_trace = cea_trace(domains, training_examples)
S, G = S_trace[-1], G_trace[-1]

print(all_agree(S, G, ('red',)))   # Expected output depends on the agreement within the version space
print(all_agree(S, G, ('blue',)))  # Expected output depends on the agreement within the version space
