import concurrent.futures
import queue
import random
import threading
import time

def producer(queue, event):
    while not event.is_set():
        message = random.randint(1, 101)
        print("Producer got message: ", message)
        queue.put(message)

    print("Producer received event. Exiting")

def consumer(queue, event):
    while not event.is_set() or not queue.empty():
        message = queue.get()
        print("Consumer storing message: ", message)
        print("Current workload in the queue: ", queue.qsize())

    print("Consumer received event. Exiting")

if __name__ == "__main__":
    producers_count = int(input('Input producer count: '))
    consumer_count = int(input('Input consumer count: '))

    pipeline = queue.Queue(maxsize=10)
    event = threading.Event()
    producer_executor = concurrent.futures.ThreadPoolExecutor(max_workers=producers_count)
    consumer_executor = concurrent.futures.ThreadPoolExecutor(max_workers=consumer_count)

    producer_executor.submit(producer, pipeline, event)
    consumer_executor.submit(consumer, pipeline, event)
    time.sleep(0.1) # work time
    print("STOP: SET EVENT")
    event.set()