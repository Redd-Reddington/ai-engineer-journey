def is_valid_password(password):
    """True if 8+ chars, with at least one digit and one uppercase letter."""
    long_enough = len(password) >= 8
    has_digit = any(ch.isdigit() for ch in password)
    has_upper = any(ch.isupper() for ch in password)
    return long_enough and has_digit and has_upper

print(is_valid_password("hello"))        # False
print(is_valid_password("Hello1234"))    # True