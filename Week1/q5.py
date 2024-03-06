def decode(code):
    x1, y1, x2, y2 = code
    def hypothesis(point):
        x, y = point
        return min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2)
    return hypothesis

# Example usage:
import itertools

# Decode a rectangle code into a hypothesis
h = decode((-1, -1, 1, 1))

# Test the hypothesis with points in the 2D space
for x in itertools.product(range(-2, 3), repeat=2):
    print(x, h(x))
