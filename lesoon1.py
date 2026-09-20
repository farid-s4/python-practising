def fibonacci_generator():
    a = 0
    b = 1
    while True:
        yield a
        res = a + b
        a=b
        b=res

gen = fibonacci_generator()
my_numbers = []
for i in range(10):
    my_numbers.append(next(gen))

print(my_numbers)