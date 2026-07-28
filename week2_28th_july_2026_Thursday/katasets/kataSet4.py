
# Sequential Version

import asyncio
import time

async def slow_task(task_id):
    print(f"Task {task_id} started")
    await asyncio.sleep(1)
    print(f"Task {task_id} finished")


async def sequential():
    start = time.perf_counter()

    for i in range(5):
        await slow_task(i)

    end = time.perf_counter()

    print(f"\nSequential Time: {end-start:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(sequential())
    
    
# Concurrent Version
import asyncio
import time


async def slow_task(task_id):
    print(f"Task {task_id} started")

    await asyncio.sleep(1)

    print(f"Task {task_id} finished")


async def main():

    start = time.perf_counter()

    tasks = [
        slow_task(i)
        for i in range(5)
    ]

    await asyncio.gather(*tasks)

    end = time.perf_counter()

    print(f"\nAsync Time: {end-start:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())