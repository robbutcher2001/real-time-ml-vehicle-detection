# real-time-ml-vehicle-detection

Using real-time RTSP stream and machine learning (specifically computer vision) to analyse parked vehicles.

## dev

- `poetry install`
- `poetry run python -m rtvd.server`

## prod

Build and run in detached mode with: `docker compose up --build -d`.
