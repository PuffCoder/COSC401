
from itertools import chain, combinations

def all_subsets(s):
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def all_possible_functions(X):
    functions = set()

    for subset in all_subsets(X):
        def func(x, subset=set(subset)):
            return x in subset
        functions.add(func)

    # return functions
    for i in functions:
        print i 
        

# 输入空间示例
X = {"green", "purple"}

# 生成所有可能的函数
F = all_possible_functions(X)

# 存储每个函数的映射结果
images = set()
for h in F:
    images.add(tuple(h(x) for x in X))

# 打印结果
for image in sorted(images):
    print(image)


