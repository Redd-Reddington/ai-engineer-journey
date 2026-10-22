def add_stars(func):                   # func = the function we are wrapping
    def wrapper(*args, **kwargs):
        print("⭐ Start ⭐")
        func(*args, **kwargs)          # run the real function
        print("⭐ End ⭐")
    return wrapper


def count_to(n):                       # Generator Starting from 1 to n
    count = 1
    while count <= n:
        yield count
        count += 1


@add_stars                             # Decorator applied to the function
def show_numbers(n):
    for number in count_to(n):
        print(number)


show_numbers(5)                       # Output 1-5 in between decorated  stars