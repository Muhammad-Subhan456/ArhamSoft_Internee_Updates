# Kata-1 - Cache Bug

# Personal Information

def personalInformation(name, age, store = None):
    if store is None:
        store = {}
    store[name] = age
    return store

ali = personalInformation("Ali",23)
usman = personalInformation("Usman", 27)

print(ali)
print(usman)

# Kata-2 : Bare Except
import json

try:
    with open("config.json") as f:
        Config = json.load(f)
except FileNotFoundError:
    print("Config File Not Found")
except json.JSONDecodeError:
    print("Config file is corrupted")
finally:
    print(Config)
    print("File Closed")
