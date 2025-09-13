from ultralytics import YOLO
from .rtsp_stream import get_frame
from .status_store import set_status
from .logging_config import get_logger

logger = get_logger(__name__)

MODEL = 'models/yolo11x.pt'

def isIntersectingKitchen(x, y):
    x1 = 1550 #top-left
    y1 = 650 #top-left
    x2 = 2100 #bottom-right
    y2 = 1200 #bottom-right
    xBound = x > x1 and x < x2
    yBound = y > y1 and y < y2

    return True if xBound and yBound else False

def isIntersectingFrontdoor(x, y):
    x1 = 850 #top-left
    y1 = 450 #top-left
    x2 = 1400 #bottom-right
    y2 = 1000 #bottom-right 
    xBound = x > x1 and x < x2
    yBound = y > y1 and y < y2

    return True if xBound and yBound else False

def car_space_inference():
    kitchen_occupied = False
    frontdoor_occupied = False

    try:
        frame = get_frame()
        if frame is None:
            logger.warning("Could not get frame from RTSP stream, skipping inference")
            return
        
        model = YOLO(MODEL)
        results = model(frame, device="mps", verbose=False)

        for result in results:
            boxes = result.boxes
            xywh = boxes.xywh
            for detection in xywh:
                x = int(detection[0].item())
                y = int(detection[1].item())
                if isIntersectingKitchen(x, y):
                    kitchen_occupied = True
                if isIntersectingFrontdoor(x, y):
                    frontdoor_occupied = True
        
        set_status(kitchen_occupied, frontdoor_occupied)
    except Exception as e:
        logger.error(f"Error in car_space_inference: {e}")
