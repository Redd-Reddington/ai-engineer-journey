def list_stats(numbers):
    """Return (smallest, largest, average) without using min() or max()."""
    smallest = numbers[0]
    largest = numbers[0]
    total = 0
    for n in numbers:
        if n < smallest:
            smallest = n
        if n > largest:
            largest = n
        total += n
    return smallest, largest, total / len(numbers)

print(list_stats([4, 9, 1, 7]))  # (1, 9, 5.25)