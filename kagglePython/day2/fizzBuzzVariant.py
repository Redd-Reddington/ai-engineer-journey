def fizzbuzz(start, stop):
    """Return FizzBuzz results for numbers from start up to (not including) stop."""
    results = []
    for n in range(start, stop):
        if n % 15 == 0:
            results.append("FizzBuzz")
        elif n % 3 == 0:
            results.append("Fizz")
        elif n % 5 == 0:
            results.append("Buzz")
        else:
            results.append(n)
    return results

print(fizzbuzz(1, 16))
# [1, 2, 'Fizz', 4, 'Buzz', 'Fizz', 7, 8, 'Fizz', 'Buzz', 11, 'Fizz', 13, 14, 'FizzBuzz']