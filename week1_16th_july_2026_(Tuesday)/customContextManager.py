class HelloContextManager:
    def __enter__(self):
        print("Entering the Context...")
        self.middleWare()
        return "Hello World"
    
    def middleWare(self):
        print("A Function in mid between setup and teardown")
    
    def __exit__(self,exc_type,exc_value,exc_tb):
        print("Leaving the Context")
        print(f"{exc_type = }")
        print(f"{exc_value =  }")
        print(f"{exc_tb = }")
        
with HelloContextManager() as hello:
    print(hello)
    hello[100]