
class DTNode:
    def __init__(self, decision):
        self.decision = decision
        self.children = []

    def predict(self, input_object):
        if callable(self.decision):
            child_index = self.decision(input_object)
            if child_index < len(self.children):
                return self.children[child_index].predict(input_object)
            else:
                raise ValueError("Child index out of range. Validate the decision function or the enumeration of children.")
        else:
            return self.decision

    def leaves(self):
        # If the node is a leaf, return 1
        if not callable(self.decision):
            return 1
        else:
            # Sum the number of leaves for each child recursively
            return sum(child.leaves() for child in self.children)

# ==================== TEST CASE ====================
n = DTNode(True)
print(n.leaves())

# ==================== TEST CASE ====================
t = DTNode(True)
f = DTNode(False)
n = DTNode(lambda v: 0 if not v else 1)
n.children = [t, f]
print(n.leaves())

# ==================== TEST CASE ====================
tt = DTNode(False)
tf = DTNode(True)
ft = DTNode(True)
ff = DTNode(False)
t = DTNode(lambda v: 0 if v[1] else 1)
f = DTNode(lambda v: 0 if v[1] else 1)
t.children = [tt, tf]
f.children = [ft, ff]
n = DTNode(lambda v: 0 if v[0] else 1)
n.children = [t, f]

print(n.leaves())
