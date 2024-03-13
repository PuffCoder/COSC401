def decode(code):
    def h(x):
        return all(code[i] != None and (code[i] == "?" or code[i] == x[i]) for i in range(len(code)))
    return h

def consistent(code, x):
    return decode(code)(x)

def initial_S(domains):
    return {tuple(None for _ in range(len(domains)))}

def initial_G(domains):
    return {tuple('?' for  _ in range(len(domains)))}

def lge(code_a, code_b):
    print("lge_codes:",code_a, code_b)
    if None in code_a:
        return True 
    print("zip(code_a, code_b):",tuple(zip(code_a, code_b)))
    for ha, hb in zip(code_a, code_b):
        print("ha:", ha, "hb:", hb)
        if not(ha == hb or (ha != hb and hb == '?')):
            return False   
    return True 

def more_specific(h, H):
    for other_h in H:
        print("more_specific")
        if lge(h, other_h) and other_h != h:
            return True
    return False 

def more_general(h, H):
    for other_h in H:
        # print("more_general")
        # print('other h', other_h)
        # print('h', h)
        # print(lge(other_h, h))
        if lge(other_h, h) and other_h != h:
            return True
    return False 
        
def minimal_generalisations(code, x):
    print("code:", code)
    print("x:", x)
    h_hypothesis = set()
    g_hypothesis = list(code).copy()
    print("hypothesis before generalization:", code)

    for i in range(len(g_hypothesis)):
        if g_hypothesis[i] == None:
            g_hypothesis[i] = x[i]
        elif g_hypothesis[i] != x[i]:
            g_hypothesis[i] = "?"
    print("hypothesis after generalization:", g_hypothesis)

    h_hypothesis.add(tuple(g_hypothesis))
    print("hypothesis set:", h_hypothesis)
    return h_hypothesis

def minimal_specialisations(code, domains, x):
    print("minimal_specialisations", code, domains, x)
    s_hypothesis = set()

    for i in range(len(code)):
        print(i)
        if code[i] == '?':
            for features in domains[i]:
                if features != x[i]:
                    h_hypothesis = list(code).copy()
                    print("hypothesis before specialization:", h_hypothesis)
                    h_hypothesis[i] = features

                    print("hypothesis after specialization:", h_hypothesis)
                    s_hypothesis.add(tuple(h_hypothesis))
    print("s_hypothesis:", s_hypothesis)
    return s_hypothesis

def cea_trace(domains, D):
    S_trace, G_trace = [], []
    S = initial_S(domains)
    G = initial_G(domains)
    print('initial_S:', S)
    print('initial_G:', G)
    S_trace.append(S.copy())
    G_trace.append(G.copy())
   
    for x, y in D:
        print('FOR_D_X_Y:', x, 'D_y:', y)
        if y:
            G = {g for g in G if consistent(g, x)}
            for s in {s for s in S if not consistent(s, x)}:
                # print("s that does not match with x:", s)
                S.remove(s)

                for h in minimal_generalisations(s, x):
                    if consistent(h, x) and any(lge(h, g) for g in G):
                        print('yes')
                        S.add(h)
                # print('S after adding h (minimal generalization hypothesis):', S)

            for h in S.copy():
                if more_general(h, S):
                    print("more_general_h:", h)
                    # print("h that is more general than any another hypothesis in S:", h)
                    S.remove(h)
            
        else:
            print("else s1:", S)
            S = {s for s in S if not consistent(s, x)}
            print("else s2:", S)
            for g in {g for g in G if consistent(g, x)}:
                print('g that does match with x', g)
                G.remove(g)

                for h in minimal_specialisations(g, domains, x):
                    if (not consistent(h, x)) and any(lge(s, h) for s in S):
                        G.add(h)
                        # print('G after adding h (minimal specialization hypothesis):', G)

            for h in G.copy():
                if more_specific(h, G):
                    G.remove(h)
                    # print("h that is more specific than any another hypothesis in G:", h)
      
        print('S:', S)
        print('G:', G)
        S_trace.append(S.copy())
        G_trace.append(G.copy())
        # print('S trace', S_trace)
        # print('G_trace', G_trace)

    return S_trace, G_trace

# def lge(code_a, code_b):
#     less_general_equal = True
#     code_a_count, code_b_count = 0, 0

#     for ha, hb in zip(code_a, code_b):
#         print(ha, hb)
#         if ha != hb and (ha != "?" and hb != "?" and ha != None):
#             less_general_equal = False
#             break
        
#         else:
#             if ha in ("?", hb):
#                 code_a_count += 1
#             if hb in ('?', ha):
#                 code_b_count += 1
#             if ha == None:
#                 code_a_count -= 1
#             less_general_equal = code_a_count <= code_b_count
    
#     return (code_a_count, code_b_count, less_general_equal)


# test case 1
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
                
# test case 2
# domains = [
#     ('T', 'F'),
#     ('T', 'F'),
# ]

# training_examples = [
#     (('F', 'F'), True),
#     (('T', 'T'), False),
# ]

# S_trace, G_trace = cea_trace(domains, training_examples)
# print(len(S_trace), len(G_trace))
# S, G = S_trace[-1], G_trace[-1]
# print(len(S), len(G))

# test case 3
# domains = [
#     {'red', 'green', 'blue'}
# ]

# training_examples = [
#     (('red',), True),
#     (('green',), False),
# ]

# S_trace, G_trace = cea_trace(domains, training_examples)

# S, G = S_trace[-1], G_trace[-1]
# print(len(S), len(G))

# hs_code, hg_code = S.pop(), G.pop()
# print(hs_code == hg_code)

# test case 4
# domains = [
#     {'big', 'small'},
#     {'red', 'blue'},
#     {'circle', 'triangle'}
# ]

# training_examples = [
#     (('big', 'red', 'circle'), False),
#     (('small', 'red', 'triangle'), False),
#     (('small', 'red', 'circle'), True),
#     (('big', 'blue', 'circle'), False),
#     (('small', 'blue', 'circle'), True)
# ]

# S_trace, G_trace = cea_trace(domains, training_examples)
# print(len(S_trace) == len(G_trace) == 5)

# test case 5
# domains = [
#     {'red', 'green', 'blue'}
# ]

# training_examples = [
#     (('green',), False),
#     (('red',), True),
# ]

# S_trace, G_trace = cea_trace(domains, training_examples)

# S, G = S_trace[-1], G_trace[-1]
# print(len(S), len(G))

# hs_code, hg_code = S.pop(), G.pop()
# print(hs_code == hg_code)

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

# A case where the target function is not in H

domains = [
    {'red', 'green', 'blue'}
]

training_examples = [
    (('red',), True),
    (('green',), True),
    (('blue',), False),
]

S_trace, G_trace = cea_trace(domains, training_examples)
S, G = S_trace[-1], G_trace[-1]
print(len(S)==len(G)==0)


# # ======================== TEST 1 ======================================================================
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


# domains = [
#     ('T', 'F'),
#     ('T', 'F'),
# ]

# training_examples = [
#     (('F', 'F'), True),
#     (('T', 'T'), False),
# ]

# S_trace, G_trace = cea_trace(domains, training_examples)
# print(len(S_trace), len(G_trace))
# S, G = S_trace[-1], G_trace[-1]
# print(len(S), len(G))

# # # ======================== TEST 4 ======================================================================
# domains = [
#     {'red', 'green', 'blue'}
# ]

# training_examples = [
#     (('green',), False),
#     (('red',), True),
# ]

# S_trace, G_trace = cea_trace(domains, training_examples)

# S, G = S_trace[-1], G_trace[-1]
# print(len(S), len(G))

# hs_code, hg_code = S.pop(), G.pop()
# print(hs_code == hg_code)


# # # ======================== TEST 6 ======================================================================
# domains = [{'Y', 'N'} for _ in range(10)]

# def read_training_csv(string):
#     examples = []
#     for line in string.splitlines():
#         *x, label = [value.strip() for value in line.split(',')]
#         y = label == '+'
#         examples.append((x, y))
#     return examples


# training_examples = read_training_csv("""\
# Y, N, N, N, Y, Y, Y, N, Y, N, -
# N, N, Y, Y, Y, N, Y, Y, Y, N, -
# N, N, Y, N, Y, Y, N, Y, Y, Y, -
# Y, N, Y, N, Y, N, N, N, Y, N, -
# Y, Y, Y, Y, N, Y, Y, Y, Y, N, -
# Y, Y, Y, Y, N, N, Y, N, N, N, -
# Y, N, Y, N, Y, Y, Y, N, Y, N, -
# Y, N, Y, Y, Y, N, N, Y, N, N, -
# N, Y, Y, Y, Y, N, N, Y, Y, Y, -
# Y, Y, Y, N, Y, Y, Y, N, Y, Y, -
# Y, N, N, N, N, Y, N, Y, N, Y, +
# Y, N, N, Y, Y, Y, N, N, Y, Y, +
# N, N, Y, Y, N, N, N, N, Y, N, -
# Y, N, Y, N, Y, Y, N, N, Y, Y, -
# """)

# S_trace, G_trace = cea_trace(domains, training_examples)
# print(len(S_trace) == len(G_trace) == 15)

# if len(S_trace) == len(G_trace) == 15:
#     _check_answer(S_trace, G_trace)
# else:
#     print("Incorrect number of snapshots in S_trace or G_trace.")