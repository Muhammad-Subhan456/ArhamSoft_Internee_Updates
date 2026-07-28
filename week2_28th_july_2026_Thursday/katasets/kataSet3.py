import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def cpu_task(n):
    total = 0
    for i in range(n):
        total += i * i
    return total


N = 20_000_000


def sequential():
    for _ in range(4):
        cpu_task(N)


def thread_pool():
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(cpu_task, [N] * 4))


def process_pool():
    with ProcessPoolExecutor(max_workers=4) as executor:
        list(executor.map(cpu_task, [N] * 4))


if __name__ == "__main__":

    start = time.perf_counter()
    sequential()
    print(f"Sequential: {time.perf_counter()-start:.2f}s")

    start = time.perf_counter()
    thread_pool()
    print(f"ThreadPool: {time.perf_counter()-start:.2f}s")

    start = time.perf_counter()
    process_pool()
    print(f"ProcessPool: {time.perf_counter()-start:.2f}s")