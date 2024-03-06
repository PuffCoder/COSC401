def decode(code):
    """
    Decode a 4-tuple of integers into a hypothesis function representing a rectangle.

    Parameters:
    - code: A 4-tuple (x1, y1, x2, y2) where (x1, y1) and (x2, y2) are the coordinates
            of two opposing corners of the rectangle.

    Returns:
    - A function that takes a point (x, y) and returns True if the point lies within
      or on the boundary of the rectangle defined by `code`, and False otherwise.
    """
    # Unpack the coordinates from the code
    x1, y1, x2, y2 = code
    
    # Define the hypothesis function for the rectangle
    def hypothesis(point):
        x, y = point
        # Check if the point lies within or on the boundary of the rectangle
        # This works by ensuring x is between the x-coordinates and y is between the y-coordinates of the rectangle
        return min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2)

    return hypothesis

# Example usage:
import itertools

# Decode a rectangle code into a hypothesis
h = decode((-1, -1, 1, 1))

# Test the hypothesis with points in the 2D space
for x in itertools.product(range(-2, 3), repeat=2):
    print(x, h(x))
