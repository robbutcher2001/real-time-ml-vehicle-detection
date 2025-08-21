from contextlib import asynccontextmanager
from fastapi import FastAPI
from inference import car_space_inference
import asyncio
import uvicorn
import uuid

TWO_MINUTES = 60 * 2

inference_queue: asyncio.Queue = asyncio.Queue()
worker: asyncio.Task | None = None
shutdown_event = asyncio.Event()

async def process_task(task):
    for _ in range(3):
        print('Inferring car space..')
        await car_space_inference()
        print('Inference complete, sleeping for ', TWO_MINUTES, ' seconds')
        await asyncio.sleep(10)
    print(f"Task {task['id']} completed")

async def worker():
    while not shutdown_event.is_set():
        try:
            task = await asyncio.wait_for(inference_queue.get(), timeout=1.0)
        except asyncio.TimeoutError:
            continue
        try:
            await process_task(task)
        finally:
            inference_queue.task_done()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global worker
    worker = asyncio.create_task(worker())
    yield
    shutdown_event.set()
    if worker:
        worker.cancel()
        try:
            await worker
        except asyncio.CancelledError:
            pass
    if inference_queue.qsize() > 0: print('Unprocessed tasks:', inference_queue.qsize())

app = FastAPI(lifespan=lifespan)

@app.post("/inference")
async def inference():
    id = str(uuid.uuid4())
    task = {
        'id': id
    }
    print(f"Received task: {task}")
    await inference_queue.put(task)
    return {"queued": id, "queue_position": inference_queue.qsize()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)