import numpy as np

def probability_lower_bound(test_res, deviations):
    test_res= np.array(test_res)
    n = test_res.size
    error_rate = np.sum(~test_res) / n
    exponent = -2 * n * deviations ** 2
    return 1 - 2 * np.exp(exponent)

print(probability_lower_bound([True, False] * 500, 0.05))