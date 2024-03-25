from math import log2

class DTNode:
    def __init__(self, decision=None, label=None):
        self.decision = decision  
        self.label = label 
        self.children = {} 

    def predict(self, input_obj):
        if self.decision is None:  
            return self.label
        else: 
            feature_value = self.decision(input_obj)
            if feature_value in self.children:
                return self.children[feature_value].predict(input_obj)
            return None
        
def partition_by_feature_value(dataset, feature_index):
    partitions = {}
    for features, label in dataset:
        feature_value = features[feature_index]
        if feature_value not in partitions:
            partitions[feature_value] = []
        partitions[feature_value].append((features, label))
    return partitions
    

def calculate_proportions(dataset):
    counts = {}
    for _, classification in dataset:
        counts[classification] = counts.get(classification, 0) + 1
    total = len(dataset)
    return {k: v / total for k, v in counts.items()}

def misclassification(dataset):
    proportions = calculate_proportions(dataset)
    return 1 - max(proportions.values())

def train_tree(dataset, criterion, feature_index=0, depth=0):
    classifications = [y for _, y in dataset]
    if len(set(classifications)) == 1:
        return DTNode(label=classifications[0])

    best_feature = feature_index  
    partitions = partition_by_feature_value(dataset, best_feature)
    node = DTNode(decision=lambda x: x[best_feature])
    for feature_value, partition in partitions.items():
        if len(partition) > 0:
            child = train_tree(partition, criterion, feature_index + 1, depth + 1)
            node.children[feature_value] = child
        else:
            pass

    return node

