
# Kata Set-2

import time
import requests
def slow(task_id):
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
    print(f"Task {task_id}: {response.status_code}")
    
start = time.perf_counter()
for i in range(5):
    slow(i)
    
end = time.perf_counter()
print(f"\nSequential Time: {end - start:.2f} seconds")

from concurrent.futures import ThreadPoolExecutor


start = time.perf_counter()

with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(slow, range(5))
    
end = time.perf_counter()

print(f"\nThreaded Time: {end - start:.2f} seconds")