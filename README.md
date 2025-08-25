# real-time-ml-vehicle-detection

Using real-time RTSP stream and machine learning (specifically computer vision) to analyse parked vehicles.

## dev

- `poetry install`
- `poetry run python -m rtvd.server`

## prod

- `poetry config virtualenvs.create false && poetry install`
- `poetry run gunicorn --bind 0.0.0.0:8000 rtvd.server:app`
