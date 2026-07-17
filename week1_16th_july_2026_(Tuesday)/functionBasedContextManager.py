from contextlib import contextmanager

@contextmanager
def helloContextManager():
    print("Entering the Context")
    yield "Hello World!"
    print("Leaving the COntect")
    
with helloContextManager() as hello:
    print(hello)
    
    
