def append_to(element, to = None):
    if to is None:
        to = []
    to.append(element)
    return to

first = append_to(42)
second = append_to(62)

print(first)
print(second)