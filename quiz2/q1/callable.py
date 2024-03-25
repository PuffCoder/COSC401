# callable: determine a function whether callable

# =================== basic function ===========================
def my_function():
    print("Hello, World!")

print(callable(my_function))  # 输出: True


# =================== Class ===========================
class MyClass:
    def __init__(self):
        print("创建了 MyClass 的一个实例")

print(callable(MyClass))  # 输出: True

# =================== Class instance ===========================
class MyCallableClass:
    def __call__(self):
        print("类的实例被调用")

my_instance = MyCallableClass()
print(callable(my_instance))  # 输出: True

# 实际调用实例
my_instance()  # 输出: "类的实例被调用"

# =================== lambda ===========================
my_lambda = lambda x: x * 2
print(callable(my_lambda))  # 输出: True
