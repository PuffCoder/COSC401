def decode(code):
    # 是否符合条件 
    print("\n Decode")

    def hypothesis(x):
        # pairs = [f"iteration times: {len(code)} Hypo: {code[i]} x: {x[i]}" for i in range(len(code))]
        # for pair in pairs:
            # print(pair)
        return all(code[i] != None and (code[i] == "?" or code[i] == x[i]) for i in range(len(code)))
    return hypothesis

def match(code, x):
    res = decode(code)(x)
    print("matching result ",res)
    # for _ in len(rkes):
        # print(_)
    return res


def lge(code_a, code_b):
    return (code_a and code_b)


def initial_S(domains):
    return {tuple(None for _ in range(len(domains)))}
    
def initial_G(domains):
    # return {('?',)}
    return {tuple('?' for  _ in range(len(domains)))}
    
# \\\\\\\\\\\\
    
def minimal_generalisations(hypo, x):
    # 最小化 G ; 如果边界为 None，则改值为 x[i];
    # 如果 边界不为 None，则改值为 '？'
    print("\n Call minimal G")
    specialisations = set()
    g_hypothesis = list(hypo).copy()
    print(f"minmal_G 之前 {g_hypothesis}")
    
    for i, value in enumerate(g_hypothesis):
        # print(f"min_G times:{i}      G_hyp: {g_hypothesis[i]}    x: {x[i]}")
        if value == 'None':
            print("G_hypo is None")
            g_hypothesis[i] = x[i] 
        else:
            print("G_hypo is specified")
            g_hypothesis[i] = "?" 
        print(f"minmal_G 之后 {g_hypothesis}")
        
    specialisations.add(tuple(g_hypothesis))
    print("hypothesis set: ", specialisations)
    return specialisations
    
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
    

# ////// CEA 


def cea_trace(domains, D):
    S_trace, G_trace = [], []
    S = initial_S(domains)
    G = initial_G(domains)
    S_trace.append(S.copy())
    G_trace.append(G.copy())
    print(f"G length {len(G)}")
    for x, y in D:
        if y: # if positive
            print("                                     触发 POS\n检查G")
            G = {g for g in G if match(g,x)}
                
            # 检查 g 是否都 match(d); 
            print("检查S")
            for s in {s for s in S if not match(s,x)}:
                print(" 检查S 找到不符合条件的 s，从S中移除 s")
                S.remove(s)
                # print("check elements in S ")
                # for _ in S:
                    # print(_)
                # print(len(S))
                
                for h in minimal_generalisations(s,x):
                    if match(h,x) and any(lge(h,g) for g in G):
                        print(" 找到符合条件的 new H，加入 S")
                        S.add(h)
                        print("                                  完成 POS 检查")
                        
                        
            
        
        

        else: # if negative
            print("                                      触发 Neg")
            print("else s1: ", S)
            S = {s for s in S if not match(s,x)}
            print("else s2: ", S)
            for g in {g for g in G if match(g,x)}:
                print(" 检查G 找到不符合条件的 g，从G中移除 g")
                G.remove(g)
                for h in minimal_specialisations(g,domains,x):
                    if (not match(h,x)) and any(lge(s,h) for s in S):
                        print(" 找到符合条件的 new H，加入 G")
                        G.add(h)
            
            print("                                  完成 NEG 检查")
    
    # for _ in G:
        # print(_)
            
        S_trace.append(S.copy())
        G_trace.append(G.copy())

    print("\n")
    print(f"S length: {len(S)}" )
    print(f"G length: {len(G)}" )
    print(" end of CEA\n")

    print("S_trace" ) #,S_trace)
    for _ in S_trace:
        print(_)

    print("G_trace" ) #,G_trace)
    for _ in G_trace:
        print(_)
    # print("length of G_trace",len(G_trace))
    
    # print(S_trace[1] == S_trace[2])
    return S_trace, G_trace



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
