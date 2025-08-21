from flask import Flask, jsonify
from inference import car_space_inference
import threading
import queue
import time
import uuid

INFERENCES_PER_TASK = 3
INFERENCE_INTERVAL = 60 * 2

app: Flask = Flask(__name__)
inference_queue: queue.Queue = queue.Queue()

def process_task(task):
    print(f"Inference {task['id']} started")
    for _ in range(INFERENCES_PER_TASK):
        car_space_inference()
        time.sleep(INFERENCE_INTERVAL)
    print(f"Inference {task['id']} completed")

def worker():
    print("Worker started, waiting for inference requests..")
    while True:
        try:
            process_task(inference_queue.get())
        finally:
            inference_queue.task_done()
            print(f"Queue size {inference_queue.qsize()}" if inference_queue.qsize() > 0 else "Queue is empty, waiting for inference requests..")

@app.post("/inference")
def inference():
    id = str(uuid.uuid4())
    inference_queue.put({ 'id': id })
    queue_size = inference_queue.qsize()
    print(f"Inference {id} queued, queue size: {queue_size}")
    return jsonify({"queued": id, "queue_position": queue_size})

if __name__ == "__main__":
    threading.Thread(target=worker, daemon=True).start()
    app.run(host="0.0.0.0", port=8000)

# need to run from terminal with: gunicorn -w 4 -b 0.0.0.0:8000 app:app