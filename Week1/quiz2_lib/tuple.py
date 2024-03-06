def create_function_from_tuple(rule):
    """根据元组规则创建函数"""
    
    def func(x):
        if rule == "even":
            return x % 2 == 0
        elif rule == "odd":
            return x % 2 != 0
        # 可以根据需要添加更多规则
        else:
            raise ValueError("Unknown rule")
    
    return func

rules = ("even", "odd")  # 定义规则
functions = {create_function_from_tuple(rule) for rule in rules}  # 创建函数集合

# 测试输入空间X
X = [1, 2, 3, 4, 5, 6]

# 对于函数集合中的每个函数，测试所有X中的元素
for func in functions:
    results = [func(x) for x in X]
    print(results)
