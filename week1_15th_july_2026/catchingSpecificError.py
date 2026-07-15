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
    

# Cleaning Up After Execution With finally


try:
    print(0/0)
except RuntimeError as error:
    print(error)
else:
    try:
        with open("file.log") as file:
            read_data = file.read()
    except FileNotFoundError as fnf_error:
        print(fnf_error)
finally:
    print("Cleaning up, irrespective of any exceptions.")