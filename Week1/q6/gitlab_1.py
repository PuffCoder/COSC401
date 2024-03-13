
def initial_S(domains):
    return {tuple(None for _ in range(len(domains)))}
#   return [tuple([min(domain) for domain in domains] + [max(domain) for domain in domains])]


def initial_G(domains):
    return {tuple('?' for _ in range(len(domains)))}

def decode(code):
    def h(x):
        return all(code[i] is not None and (code[i] == "?" or code[i] == x[i]) for i in range(len(code)))
    return h

def consistent(code, x):
    return decode(code)(x)


def lge(code_a, code_b):
    if None in code_a:
        return True
    for ha, hb in zip(code_a, code_b):
        if not (ha == hb or (ha != hb and hb == '?')):
            return False
    return True

def minimal_generalisations(code, x):
    h_hypothesis = set()
    g_hypothesis = list(code).copy()
    for i in range(len(g_hypothesis)):
        if g_hypothesis[i] is None:
            g_hypothesis[i] = x[i]
        elif g_hypothesis[i] != x[i]:
            g_hypothesis[i] = "?"
    h_hypothesis.add(tuple(g_hypothesis))
    return h_hypothesis

def minimal_specialisations(code, domains, x):
    s_hypothesis = set()
    for i in range(len(code)):
        if code[i] == '?':
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
    print(S)
    
    S_trace.append(S.copy())
    G_trace.append(G.copy())

    for x, y in D:
        if y:  # 如果是正例
            G = {g for g in G if consistent(g, x)}  # 从 G 中移除与 x 不一致的假设
            S_to_remove = set()
            for s in S:
                if not consistent(s, x):  # 找到 S 中所有与 x 不一致的假设
                    S.remove(s)
                    for h in minimal_generalisations(s, x):
                        if all(consistent(h, xi) for xi, yi in D if yi):  # 确保 h 与所有正例一致
                            S.add(h)
            S = {h for h in S if not any(lge(h2, h) and h2 != h for h2 in S)}  # 移除更一般的假设
        else:  # 如果是反例
            S = {s for s in S if consistent(s, x)}  # 从 S 中移除与 x 一致的假设
            G_to_remove = set()
            for g in G.copy():  # 使用 G.copy() 进行迭代
                if consistent(g, x):
                    G.remove(g)
                    for h in minimal_specialisations(g, domains, x):
                        # 确保新假设 h 与所有已知反例不一致
                        if not any(consistent(h, xi) and not yi for xi, yi in D):
                            G.add(h)
            G = {h for h in G if not any(lge(h, h2) and h2 != h for h2 in G)}  # 移除更特殊的假设
        
        S_trace.append(S.copy())
        G_trace.append(G.copy())

    return S_trace, G_trace












# ======================== TEST 1 ======================================================================
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

# # # ======================== TEST 2 ======================================================================
# domains = [
#     {'T', 'F'}
# ]

# training_examples = []  # no training examples

# S_trace, G_trace = cea_trace(domains, training_examples)
# print(len(S_trace), len(G_trace))
# S, G = S_trace[-1], G_trace[-1]
# print(len(S), len(G))

# # # ======================== TEST 3 ======================================================================


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