
from itertools import chain, combinations 

def input_space(element):
    return chain.from_iterable(combinations(element,dimension) for dimension in range(len(element) + 1))
    
domains = [
    # {'x1'},{'x2'},{'x3'}]
    "x1","x2","x3"]
for i in sorted(input_space(domains)):
    print(i) 
    
print(len(domains))
