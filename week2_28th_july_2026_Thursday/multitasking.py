import multiprocessing

def worker(num):
    print(f"Worker: {num}")

if __name__ == "__main__":
    process = multiprocessing.Process(target=worker, args=(1,))
    process.start()
    process.join()
    
