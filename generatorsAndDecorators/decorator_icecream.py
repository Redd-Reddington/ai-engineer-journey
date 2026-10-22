import time                          # gives us a clock


def add_sprinkles(func):                # func = the function we are wrapping
    def wrapper(*args, **kwargs):
        print("Adding sprinkles 🍬")
        func(*args, **kwargs)           # run the real function
    return wrapper

def add_fudge(func):                    # func = the function we are wrapping
    def wrapper(*args,**kwargs):
        print("Adding fudge 🍫")
        func(*args, **kwargs)            # run the real function
    return wrapper

def timer(func):                     # func = the function we are wrapping
    def wrapper(*args, **kwargs):
        start = time.time()          # look at the clock BEFORE (like pressing start on a stopwatch)
        func(*args, **kwargs)        # run the real function
        end = time.time()            # look at the clock AFTER (like pressing stop)
        print(f"Took {end - start:.2f} seconds ⏱️")   # after minus before = time taken
    return wrapper

def flavors():                          # Generator
    print("getting vanilla...")
    time.sleep(1)                       # wait 1 second
    yield "vanilla"
    print("getting chocolate...")
    time.sleep(1)                       # wait 1 second
    yield "chocolate"
    print("getting strawberry...")
    yield "strawberry"
    print("getting mango...")
    yield "mango"



def read_file(file_path):             # generator 2: file lines 
    with open(file_path, encoding="utf-8") as file:
        for line in file:
            yield line.strip()


@timer                                 # Decorator applied to the function
@add_sprinkles                         # Decorator applied to the function
@add_fudge                             # Decorator applied to the function
def serve_all():
    for flavor in flavors():           # each loop asks the generator for the next flavor
        print(f"Here is your {flavor} ice cream 🍨")


#@timer                              
#def show_anthem():
#    for line in read_file(r"C:\Users\yduos\OneDrive\Desktop\National Anthem.txt"):
#        print(line)


serve_all()
#show_anthem()