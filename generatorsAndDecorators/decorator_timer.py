import time                          # gives us a clock


def timer(func):                     # func = the function we are wrapping
    def wrapper(*args, **kwargs):
        start = time.time()          # look at the clock BEFORE (like pressing start on a stopwatch)
        func(*args, **kwargs)        # run the real function
        end = time.time()            # look at the clock AFTER (like pressing stop)
        print(f"Took {end - start:.2f} seconds ⏱️")   # after minus before = time taken
    return wrapper


def count_to(n):                     # Generator starting from 1 to n
    count = 1
    while count <= n:
        yield count
        count += 1


@timer                               # Decorator applied to the function
def show_numbers(n):
    for number in count_to(n):
        pass                         # do nothing, just go through the numbers


show_numbers(5_000_000)             #The timer starts a stopwatch, runs show_numbers(5_000_000) (which makes the generator hand out 5 million numbers one by one), stops the stopwatch, and prints the difference.