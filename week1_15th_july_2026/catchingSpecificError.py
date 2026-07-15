#Problem:
# A bare except: catches every exception, including exceptions that are not actual errors in your program,
#such as KeyboardInterrupt (when the user presses Ctrl + C) and SystemExit.
#Example:

try: 
    num = int(input("Enter a number: ")) 
    print(100 / num) 
except: 
    print("Something went wrong!")
    

# Solution: Catch Specific Exceptions
try:
    num = int(input("Enter a number: "))
    print(100 / num)

except Exception as e:
    print(f"An unexpected error occurred: {e}")