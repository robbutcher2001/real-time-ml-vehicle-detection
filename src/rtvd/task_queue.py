import queue
import logging
import sys
import time
import threading

ITERATIONS_PER_TASK = 3
ITERATION_INTERVAL = 60 * 2

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
task_queue: queue.Queue = queue.Queue()
print(logger.handlers)

def process_task(task):
    logging.info(f"Task {task['id']} started")
    for _ in range(ITERATIONS_PER_TASK):
        task['action']()
        time.sleep(ITERATION_INTERVAL)
    logging.info(f"Task {task['id']} completed")

def worker():
    logging.info("Worker started, waiting for tasks..")
    while True:
        try:
            process_task(task_queue.get())
        finally:
            task_queue.task_done()
            logging.info(f"Queue size {task_queue.qsize()}" if task_queue.qsize() > 0 else "Queue is empty, waiting for tasks..")

threading.Thread(target=worker, daemon=True).start()
