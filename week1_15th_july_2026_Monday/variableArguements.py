# *args: Multiple Positional args in a tuple
def fun(*args):
    return sum(args)

print(fun(1,2,3,4,5))

# **kwargs : Multiple keyword arguements in a dictionary
def fun(**kwargs):
    for k,val in kwargs.items():
        print(k,val)

fun(a=1,b=2,c=3)