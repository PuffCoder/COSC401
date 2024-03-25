
class DTNode:
    def __init__(self, decision):
        self.decision = decision
        self.children = {}

    def predict(self, input_obj):
        if callable(self.decision):
            child_index = self.decision(input_obj)
            if child_index < len(self.children):
                return self.children[child_index].predict(input_obj)
            else:
                # raise ValueError("Child not found for the given decision output")
                print("error")
        else:
            return self.decision


# ==================== TEST CASE ====================

# Sine it's a leaf node, the input can be anything. It's simply ignored.
yes_node = DTNode("Yes")
no_node = DTNode("No")
tree_root = DTNode(lambda x: 0 if x[2] < 4 else 1)
tree_root.children = [yes_node, no_node]

print(tree_root.predict((False, 'Red', 3.5)))
print(tree_root.predict((False, 'Green', 6.1)))