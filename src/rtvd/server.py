from flask import Flask, jsonify
from .task_queue import task_queue
from .inference import car_space_inference
import uuid

app: Flask = Flask(__name__)

@app.post("/inference")
def inference():
    id = str(uuid.uuid4())
    task_queue.put({ 'id': id, 'action': car_space_inference })
    queue_size = task_queue.qsize()
    print(f"Inference {id} queued, queue size: {queue_size}")
    return jsonify({"queued": id, "queue_position": queue_size})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
