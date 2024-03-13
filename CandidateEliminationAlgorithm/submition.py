def decode(code):
    def h(x):
        return all(code[i] != None and (code[i] == "?" or code[i] == x[i]) for i in range(len(code)))
    return h
        
def match(code, x):
    return decode(code)(x)
    
def lge(code_a, code_b):
    if None in code_a:
        return True
        
    for a, b in zip(code_a, code_b):
        if a != '?' and (b == '?' or a == b):
            continue
        elif a == '?' and b == '?':
            continue
        else:
            return False
    return True 

            
def initial_S(domains):
    return {tuple(None for _ in range(len(domains)))}
    
    
def initial_G(domains):
    return {tuple('?' for  _ in range(len(domains)))}
    

def minimal_generalisations(code, x):
    specialisations = set()
    g_hypothesis = list(code).copy()
    
    for i,value in enumerate(g_hypothesis):
        if value == None:
            g_hypothesis[i] = x[i]
        elif value != x[i]:
            g_hypothesis[i] = "?"
        
    specialisations.add(tuple(g_hypothesis))
    return specialisations 
    

def minimal_specialisations(code, domains, x):
    s_hypothesis = set()

    for i, c in enumerate(code):
        if c == '?':  
            for feature in domains[i]:
                if feature != x[i]:
                    h_hypothesis = list(code).copy()
                    h_hypothesis[i] = feature  
                    s_hypothesis.add(tuple(h_hypothesis))
    return s_hypothesis

 

def cea_trace(domains, D):
    S_trace, G_trace = [], []
    S = initial_S(domains)
    G = initial_G(domains)
    S_trace.append(S.copy())
    G_trace.append(G.copy())
    
    for x, y in D:
        if y: # if positive
            G = {g for g in G if match(g,x)}
            for s in {s for s in S if not match(s,x)}:
                S.remove(s)
                
                for h in minimal_generalisations(s,x):
                    if match(h,x) and any(lge(h,g) for g in G):
                        S.add(h)

        else: # if negative
            S = {s for s in S if not match(s,x)}
            for g in {g for g in G if match(g,x)}:
                G.remove(g)
                for h in minimal_specialisations(g,domains,x):
                    if (not match(h,x)) and any(lge(s,h) for s in S):
                        G.add(h)
                        
        S_trace.append(S.copy())
        G_trace.append(G.copy())

    return S_trace, G_trace


# # ======================== TEST 6 ======================================================================
print("\n")
domains = [{'Y', 'N'} for _ in range(10)]

def read_training_csv(string):
    examples = []
    for line in string.splitlines():
        *x, label = [value.strip() for value in line.split(',')]
        y = label == '+'
        examples.append((x, y))
    return examples


training_examples = read_training_csv("""\
Y, N, N, N, Y, Y, Y, N, Y, N, -
N, N, Y, Y, Y, N, Y, Y, Y, N, -
N, N, Y, N, Y, Y, N, Y, Y, Y, -
Y, N, Y, N, Y, N, N, N, Y, N, -
Y, Y, Y, Y, N, Y, Y, Y, Y, N, -
Y, Y, Y, Y, N, N, Y, N, N, N, -
Y, N, Y, N, Y, Y, Y, N, Y, N, -
Y, N, Y, Y, Y, N, N, Y, N, N, -
N, Y, Y, Y, Y, N, N, Y, Y, Y, -
Y, Y, Y, N, Y, Y, Y, N, Y, Y, -
Y, N, N, N, N, Y, N, Y, N, Y, +
Y, N, N, Y, Y, Y, N, N, Y, Y, +
N, N, Y, Y, N, N, N, N, Y, N, -
Y, N, Y, N, Y, Y, N, N, Y, Y, -
""")

S_trace, G_trace = cea_trace(domains, training_examples)
print(len(S_trace) == len(G_trace) == 15)
print(len(S_trace))
