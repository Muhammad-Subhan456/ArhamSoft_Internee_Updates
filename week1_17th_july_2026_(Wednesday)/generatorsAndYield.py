def csv_reader(file_name):
    for row in open(file_name, "r"):
        yield row

csv_gen = csv_reader("techcrunch.csv")
row_count = 0

for row in csv_gen:
    row_count += 1

print(f"Row count is {row_count}")

    # Advance Generators
# Using .send()

# def greet():
#     name = yield
#     print(f"Hello {name}!")

# g = greet()

# next(g)            # Start the generator
# g.send("Subhan")

# Using .throw()
def worker():
    try:
        while True:
            yield "Working"
    except:
        print("Error handled inside generator")
        
g = worker()

print(next(g))
# g.throw(ValueError)

# Creating data pipelines:
file_name = "techcrunch.csv"
lines = (line for line in open(file_name))
list_line = (s.rstrip().split(",") for s in lines)
cols = next(list_line)
company_dicts = (dict(zip(cols, data)) for data in list_line)
funding = (
    int(company_dict["raisedAmt"])
    for company_dict in company_dicts
    if company_dict["round"] == "a"
)
total_series_a = sum(funding)
print(f"Total series A fundraising: ${total_series_a}")

