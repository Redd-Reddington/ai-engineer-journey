def calculate_fee(amount):
    """Return a fee based on the transaction amount."""
    if amount <= 100:
        return 1.00
    elif amount <= 500:
        return amount * 0.01
    else:
        return amount * 0.005 + 3

print(calculate_fee(50))    # 1.0
print(calculate_fee(300))   # 3.0
print(calculate_fee(1000))  # 8.0