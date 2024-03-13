
def decode(code):
    def h(x):
        return all(code[i] != None and (code[i] == "?" or code[i] == x[i]) for i in range(len(code)))
        # Complete this function for the conjunction of constraints
    return h
        
def match(code, x):
    return decode(code)(x)
    
def lge(code_a, code_b):
    return (code_a and code_b)


    # print("lge_codes:",code_a, code_b)
    # if None in code_a:
    #     return True 
    # print("zip(code_a, code_b):",tuple(zip(code_a, code_b)))
    # for ha, hb in zip(code_a, code_b):
    #     print("ha:", ha, "hb:", hb)
    #     if not(ha == hb or (ha != hb and hb == '?')):
    #         return False   
    # return True 
    
    # Complete this for the conjunction of constraints. You do not need to
    # decode the given codes.
    
    # if code_a and not code_b:  
    #         return False
    # return True 
            
def initial_S(domains):
    return {tuple(None for _ in range(len(domains)))}
    
    # Return an appropriate set

    
def initial_G(domains):
    return {tuple('?' for  _ in range(len(domains)))}
    
    # Return an appropriate set


def minimal_generalisations(code, x):
    print("code:", code)
    print("x:",x)
    h_hypothesis = set()
    # set 只保留不同元素
    g_hypothesis = list(code).copy()
    # Tuple 不可更改，所以用 list
    print("hypothesis before generalization:",code)
    
    for i in range(len(g_hypothesis)):
        if g_hypothesis[i] == None:
            g_hypothesis[i] = x[i]
        elif g_hypothesis[i] != x[i]:
            g_hypothesis[i] = "?"
        print("Hypothesis after generalization:", g_hypothesis)
        
    h_hypothesis.add(tuple(g_hypothesis))
    print("hypothesis set: ", h_hypothesis)
    return h_hypothesis
    
    # Return an appropriate set

def minimal_specialisations(code, domains, x):
    print("minimal_specialisations",code, domains, x)
    s_hypothesis = set()
    
    for i in range(len(code)):
        print(i)
        if code[i] == '?':
            for feature in domains[i]:
                if feature != x[i]:
                    h_hypothesis = list(code).copy()
                    print("hypothesis before specialization: ", h_hypothesis)
                    h_hypothesis[i] = feature
                    
                    print("hypothesis after specialization: ", h_hypothesis)
                    s_hypothesis.add(tuple(h_hypothesis))
    print("s_hypothesis: ", s_hypothesis)
    return s_hypothesis


def cea_trace(domains, D):
    S_trace, G_trace = [], []
    S = initial_S(domains)
    G = initial_G(domains)
    S_trace.append(S.copy())
    G_trace.append(G.copy())
    # Append S and G (or their copy) to corresponding trace list
    
    for x, y in D:
        print("For_D_x_y: ",x, 'D_y:', y)
        if y: # if positive
            G = {g for g in G if match(g,x)}
            for s in {s for s in S if not match(s,x)}:
                S.remove(s)
                
                for h in minimal_generalisations(s,x):
                    if match(h,x) and any(lge(h,g) for g in G):
                        print('yes')
                        S.add(h)

            
    #         # Complete
            
        else: # if negative
            print("else s1: ", S)
            S = {s for s in S if not match(s,x)}
            print("else s2: ",S)
            for g in {g for g in G if match(g,x)}:
                print('g that does not match with x', g)
                G.remove(g)
                
                for h in minimal_specialisations(g,domains,x):
                    if (not match(h,x)) and any(lge(s,h) for s in S):
                        G.add(h)
                        
                
        print('S:', S) 
        print('G:', G) 
        S_trace.append(S.copy())
        G_trace.append(G.copy())
        
    #         # Complete

    #     # Append S and G (or their copy) to corresponding trace list


    return S_trace, G_trace

# ======================== TEST 1 ======================================================================
# domains = [
#     {'red', 'blue'}
# ]

# training_examples = [
#     (('red',), True)
# ]

# S_trace, G_trace = cea_trace(domains, training_examples)
# print(len(S_trace), len(G_trace))

# for _ in S_trace:
#     print(_)

# print(all(type(x) is set for x in S_trace + G_trace))
# S, G = S_trace[-1], G_trace[-1]
# print(len(S), len(G))
# print('\n')

# ======================== TEST 1 ======================================================================
# domains = [
#     {'red', 'blue'}
# ]

# training_examples = [
#     (('red',), True)
# ]

# S_trace, G_trace = cea_trace(domains, training_examples)
# print(len(S_trace), len(G_trace))
# print(all(type(x) is set for x in S_trace + G_trace))
# S, G = S_trace[-1], G_trace[-1]
# print(len(S), len(G))
# print('\n')

# # ======================== TEST 2 ======================================================================
# domains = [
#     {'T', 'F'}
# ]

# training_examples = []  # no training examples

# S_trace, G_trace = cea_trace(domains, training_examples)
# print(len(S_trace), len(G_trace))
# S, G = S_trace[-1], G_trace[-1]
# print(len(S), len(G))
# print('\n')
# # ======================== TEST 3 ======================================================================


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
