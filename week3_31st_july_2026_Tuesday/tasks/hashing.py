from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# Registration
user_password = "secret123"
stored_hash = pwd_context.hash(user_password)

print("Stored Hash:")
print(stored_hash)

# Login Attempt
login_password = input("Enter password: ")

if pwd_context.verify(login_password, stored_hash):
    print("Login Successful!")
else:
    print("Invalid Password!")