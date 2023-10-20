def compute_x_y(index):
    n = 30  # The maximum value for the first integer (0 to 29)

    if index < 0 or index >= n * (n - 1) // 2:
        # Index out of range
        return None

    # Find the row and column in the triangular matrix
    row = 0
    col = 0
    while index >= n - 1 - row:
        index -= n - 1 - row
        row += 1
        col += 1

    x = row
    y = col + row + 1
    return x, y


# Example usage:
index = 50  # Replace with your desired index
x, y = compute_x_y(index)
print(f"For index {index}: x = {x}, y = {y}")
