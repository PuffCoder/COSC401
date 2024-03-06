
from itertools import product

def input_space(domains):
    """
    import lib product from itertools
    filter data base on 'active/inactive'
    return list all combinations
    """
    combinations = list(product(*domains))
    return combinations

domains = [
    {'red', 'green', 'blue'},
    {1, -1},
    {'active', 'inactive'}
]
# domains = [
# {0, 1, 2},
# {True, False},
# ]

# 生成并打印所有符合条件的组合
for element in sorted(input_space(domains)):
    print(element)
