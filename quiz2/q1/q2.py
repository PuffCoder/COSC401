
class DTNode:
    def __init__(self, decision):
        self.decision = decision
        self.children = []

    def predict(self, input_object):
        if callable(self.decision):
            child_index = self.decision(input_object)
            print("child_index " , child_index)
            print("self_index " , len(self.children))
            if child_index < len(self.children):
                return self.children[child_index].predict(input_object)
            else:
                raise ValueError("Child index out of range. Check the decision function or children list.")
        else:
            return self.decision



# ==================== TEST CASE ====================
# Example usage
yes_node = DTNode("Yes")
no_node = DTNode("No")
tree_root = DTNode(lambda x: 0 if x[2] < 4 else 1)
tree_root.children = [yes_node, no_node]

print(tree_root.predict((False, 'Red', 3.5)))
print(tree_root.predict((False, 'Green', 6.1)))

# ==================== TEST CASE ====================
# The following (leaf) node will always predict True
node = DTNode(True) 

# Prediction for the input (1, 2, 3):
x = (1, 2, 3)
print(node.predict(x))

# Sine it's a leaf node, the input can be anything. It's simply ignored.
print(node.predict(None))
