words = ["apple", "fig", "banana", "kiwi", "cherry"]

# With a loop
result = []
for w in words:
    if len(w) > 4:
        result.append(w.upper())
print(result)  # ['APPLE', 'BANANA', 'CHERRY']

# With a comprehension
result = [w.upper() for w in words if len(w) > 4]
print(result)  # ['APPLE', 'BANANA', 'CHERRY']