import queue
import time
import threading

ITERATIONS_PER_TASK = 3
ITERATION_INTERVAL = 60 * 2

task_queue: queue.Queue = queue.Queue()

def process_task(task):
    print(f"Task {task['id']} started")
    for _ in range(ITERATIONS_PER_TASK):
        task['action']()
        time.sleep(ITERATION_INTERVAL)
    print(f"Task {task['id']} completed")

def worker():
    print("Worker started, waiting for tasks.. bahhhhhh")
    while True:
        try:
            process_task(task_queue.get())
        finally:
            task_queue.task_done()
            print(f"Queue size {task_queue.qsize()}" if task_queue.qsize() > 0 else "Queue is empty, waiting for tasks..")

threading.Thread(target=worker, daemon=True).start()
