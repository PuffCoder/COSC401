import math

def probability_lower_bound(test_outcomes, deviation):
    n = len(test_outcomes)
    print(n)
    error_rate = sum(1 for outcome in test_outcomes if not outcome) / n
    exponent = -2 * n * deviation ** 2
    return math.exp(exponent)

print(probability_lower_bound([True, False] * 500, 0.05)) # 0.986524106001829