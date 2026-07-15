from pathlib import Path

# ------------------------------------------------------------------
# TODO:
#imported path from pathlib, it will be used to get the path of our file
# ------------------------------------------------------------------
file_path = Path(__file__).parent / "data.txt"

try:
    # ------------------------------------------------------------------
    # TODO:
    #   In try block the code will be exected, if any error occurs 
    #   it will be caught in the except block
    # ------------------------------------------------------------------
    with open(file_path, "r") as f:

        # ------------------------------------------------------------------
        # TODO:
        #   i used with open() context manager so the file automatically closes in case of error
        # ------------------------------------------------------------------
        print("File opened successfully.\n")

        # ------------------------------------------------------------------
        # TODO:
        #   At this point file will be opened successfully
        # ------------------------------------------------------------------
        number = int(f.readline())

        # ------------------------------------------------------------------
        # TODO:
        #   Reads a single line from the file and stores it in the number
        # ------------------------------------------------------------------
        print(f"Number read from file: {number}")

        # ------------------------------------------------------------------
        # TODO:
        #Prints the number written in the file and stored in the variable number
        # ------------------------------------------------------------------
        result = 100 / number

        # ------------------------------------------------------------------
        # TODO:
        # Divides 100 by the user entered number.If the number is 0 it will raise an error.
        #  and the execution moves to the except block where specific error gets caught.
        # As i have used the context manager so file will also be closed automatically
        # ------------------------------------------------------------------
        print(f"Result = {result}")

except FileNotFoundError:
    # ------------------------------------------------------------------
    # TODO:
    #   this is a specific error related to FileNotFound
    #   it is necessary to get the specific error so it is easy to debug and mark the point of failure
    #   with bare except the error is not defined and takes long hours of debugging
    # ------------------------------------------------------------------
    print("Error: data.txt was not found.")

except ValueError:
    # ------------------------------------------------------------------
    # TODO:
    #   its the error related to our data, if the data in the file in not a number 
    #   we will immediately know that we have mistakenly entered the wrong datatype
    #
    # ------------------------------------------------------------------
    print("Error: First line is not a valid integer.")

except ZeroDivisionError:
    # ------------------------------------------------------------------
    # TODO:
    #   In case of division by zero we exactly get to know that the user entered zero
    #   The error is handled gracefully
    #
    # ------------------------------------------------------------------
    print("Error: Cannot divide by zero.")

except Exception as e:
    # ------------------------------------------------------------------
    # TODO:
    #   any exception other than the above three exceptions will be caught in the part
    # ------------------------------------------------------------------
    print(f"Unexpected Error: {e}")

# ------------------------------------------------------------------
# TODO:
# Summary: This program truly depicts best programming conventions.
# 1) Every Opened file must be closed automatically
# 2) Every Error should be known specifically that helps us in faster debugging and saves our time
# ------------------------------------------------------------------
print("\nProgram finished.")