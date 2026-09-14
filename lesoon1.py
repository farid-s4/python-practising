def fibonacci_generator():
    a = 0
    b = 1
    while(b>0):
        newb = a + b
        res = newb + b
        a=b
        b=newb
        yield res

gen = fibonacci_generator()
my_numbers = []
for i in range(10):
    my_numbers.append(next(gen))

print(my_numbers)