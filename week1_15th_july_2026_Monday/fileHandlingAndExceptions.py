# file never closes because error occured before closing the file
# Don use Open
#Problem: File remains open until pythons garbage collector eventually cleansup
# Keeping files open unnecessarily can waste system resources or prevent other programs from accessing the file.


f = open(r"D:\Subhan Folder\ArhamSoft_Internship\week1_15th_july_2026\data.txt", "r")

content = f.read()
try:
    x = 10 / 0      # Raises ZeroDivisionError
finally:
    print("File Not Closed")

f.close()       # Never executes

# Solution: Use Context Manager "with open(path) as f":
# Even if the error occurs the file still gets closed
with open(r"D:\Subhan Folder\ArhamSoft_Internship\week1_15th_july_2026\data.txt", "r") as f:
    content = f.read()
try:
    x = 10 / 0      # Exception
finally:
    print(content)
    print("File Closed")
    
    
with open("students.txt", "r") as file:
    for line in file:
        print(line.strip())