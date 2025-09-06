import queue
import time
import threading
from .logging_config import get_logger

ITERATIONS_PER_TASK = 3
ITERATION_INTERVAL = 60 * 2

task_queue: queue.Queue = queue.Queue()
logger = get_logger(__name__)

def process_task(task):
    logger.info(f"Task {task['id']} started")
    for _ in range(ITERATIONS_PER_TASK):
        task['action']()
        time.sleep(ITERATION_INTERVAL)
    logger.info(f"Task {task['id']} completed")

def worker():
    logger.info("Worker started, waiting for tasks..")
    while True:
        try:
            process_task(task_queue.get())
        finally:
            task_queue.task_done()
            if task_queue.qsize() > 0:
                logger.info(f"Queue size {task_queue.qsize()}")
            else:
                logger.info("Queue is empty, waiting for tasks..")

threading.Thread(target=worker, daemon=True).start()
