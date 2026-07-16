
# Custom Exception Errors with Customly defined error functions

class MyCustomError(Exception):
    """Exception raised for custom error scenarios"""
    
    def __init__(self, message,error_code):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        
    def __str__(self):
        return f"{self.message} (Error Code: {self.error_code})"
    
err = MyCustomError("Invalid Operation",400)
print(err)

# Raising a Custom Exception
class MyCustomClass(Exception):
    pass

def divide(a,b):
    if b == 0:
        raise MyCustomClass("Division By Zero is Not Allowed")
    return a/b;

try:
    divide(10,0)
except MyCustomClass as e:
    print(f"Caught an Error: {e}")
    
    
# Chaining Errors
def func():
    raise ConnectionError

try:
    func()
except ConnectionError as exc:
    raise RuntimeError('Failed to Open Database') from exc

