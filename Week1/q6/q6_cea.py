
def decode(code):
    """Takes a code and returns the corresponding hypothesis."""
    def h(x):
        return all(c == '?' or c == xi for c, xi in zip(code, x))
    return h
        
def match(code, x):
    """Takes a code and returns True if the corresponding hypothesis returns
    True (positive) for the given input."""
    return decode(code)(x)
    
def lge(code_a, code_b):
    """Takes two codes and returns True if code_a is less general or equal
    to code_b."""
    for a, b in zip(code_a, code_b):
        if a != '?' and (b == '?' or a == b):
            continue
        elif a == '?' and b == '?':
            continue
        else:
            return False
    return True 

           
def initial_S(domains):
    """Initial members of S as the most specific hypothesis."""
    return {tuple('None' for _ in domains)}  # Each feature has 'None' indicating no generalization
    
def initial_G(domains):
    """Initial members of G as the most general hypothesis."""
    return {tuple('?' for _ in domains)}  # '?' indicates any value is acceptable for each feature
 


def minimal_generalisations(code, x):
    """Takes a code (corresponding to a hypothesis) and returns the set of all
    codes that are the minimal generalisations of the given code with respect
    to the given input x."""
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


def minimal_specialisations(cc, domains, x):
    """Takes a code (corresponding to a hypothesis) and returns the set of all
    codes that are the minimal specialisations of the given code with respect
    to the given input x."""
    specialisations = set()
    for i, (c, xi) in enumerate(zip(cc, x)):
        if c == '?':
            for v in domains[i]:
                if v != xi:
                    new_code = list(cc)
                    new_code[i] = v
                    specialisations.add(tuple(new_code))
    return specialisations


def cea_trace(domains, D):
    S_trace, G_trace = [], []
    S = initial_S(domains)
    G = initial_G(domains)
   # Append initial S and G to their respective traces
    S_trace.append(S)
    G_trace.append(G)
 
    for x, y in D:
        if y: # if positive
            
            # Complete
           # Remove hypotheses from G that do not cover the example
            G = {g for g in G if match(g, x)}

            # For each hypothesis in S that does not cover the example, replace it with minimal generalizations that do
            new_S = set()
            for s in S:
                if not match(s, x):
                    # Generate minimal generalizations of s that cover x
                    for generalization in minimal_generalisations(s, x):
                        # Add the generalization if it's not more general than something in G
                        if any(lge(generalization, g) for g in G):
                            new_S.add(generalization)
                else:
                    new_S.add(s)
            S = new_S 
        else: # if negative
            
            # Complete
            S = {s for s in S if not match(s, x)}

            # For each hypothesis in G that covers the example, replace it with minimal specializations that do not
            new_G = set()
            for g in G:
                if match(g, x):
                    # Generate minimal specializations of g that do not cover x
                    for specialization in minimal_specialisations(g, domains, x):
                        # Add the specialization if it's not less general than something in S
                        if any(lge(s, specialization) for s in S):
                            new_G.add(specialization)
                else:
                    new_G.add(g)
            G = new_G

        # Append the current state oRj mdt: G to their traces after processing the example
        S_trace.append(S)
        G_trace.append(G)

        # Append S and G (or their copy) to corresponding trace list

    return S_trace, G_trace

# TEST
# 000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
domains = [
    ('T', 'F'),
    ('T', 'F'),
]

training_examples = [
    (('F', 'F'), True),
    (('T', 'T'), False),
]

S_trace, G_trace = cea_trace(domains, training_examples)
print(len(S_trace), len(G_trace))
S, G = S_trace[-1], G_trace[-1]
print(len(S), len(G))


domains = [
    {'red', 'blue'}
]

training_examples = [
    (('red',), True)
]

S_trace, G_trace = cea_trace(domains, training_examples)
print(len(S_trace), len(G_trace))
print(all(type(x) is set for x in S_trace + G_trace))
S, G = S_trace[-1], G_trace[-1]
print(len(S), len(G))