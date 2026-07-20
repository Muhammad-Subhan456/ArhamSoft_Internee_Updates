# # problem: Stores the Reference of the variable
def create():
    funcs = []
    
    for i in range(3):
        def f():
            print(i)
        
        funcs.append(f)
    
    return funcs

functions = create()
for fun in functions:
    fun()
            
            
# Solution:
# TO capture value at each iteration use a defaulr arguement
def create():
    funcs = []
    
    for i in range(3):
        def f(i=i):
            print(i)
        
        funcs.append(f)
    
    return funcs

functions = create()
for fun in functions:
    fun()


# Explaination: Default arguements are evaluated when the function is created, not when it is called
# def f(i=0):
#     print(i)

# def f(i=1):
#     print(i)

# def f(i=2):
#     print(i)