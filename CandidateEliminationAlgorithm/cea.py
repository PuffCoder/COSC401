
# 定义初始的 S 和 G
S = [('None', 'None')]
G = [('?', '?')]

# 定义域
domains = [
    ('红色', '蓝色', '绿色'),  # 颜色
    ('大', '小')  # 大小
]

def update_S(S, example):
    """根据正例更新 S"""
    # return [tuple(example if s == 'None' else s for s, example in zip(S[0], example))]
    zipped = zip(S[0], example)
    new_values = []
    # for s, example_value in zipped:
    for _ in zipped:
        print(_)
        # print(F"S: ",{s})
        # print(F"example value ",{example_value})

def update_G(G, example, domains):
    """根据反例更新 G"""
    temp_G = []
    for g in G:
        for i, value in enumerate(g):
            if value == '?':
                # 对于每个 '?'，尝试将它替换为除了反例特征值之外的所有可能值
                for domain_value in domains[i]:
                    if domain_value != example[i]:
                        new_g = list(g)
                        new_g[i] = domain_value
                        temp_G.append(tuple(new_g))
    return minimize_G(temp_G, G)

def minimize_G(temp_G, G):
    """最小化 G，移除更特殊的假设"""
    minimized_G = []
    for g in temp_G:
        if all(not all(x==y or y=='?' for x,y in zip(g, other_g)) for other_g in temp_G if g != other_g):
            minimized_G.append(g)
    return minimized_G

# 处理正例
# print("Initial S:", S)
example = ('红色', '大')
S = update_S(S, example)
# print("最终的 S:", S)

# 处理反例
# print("Initial G:", G)
example = ('蓝色', '大')
G = update_G(G, example, domains)
# print("最终的 G:", G)
