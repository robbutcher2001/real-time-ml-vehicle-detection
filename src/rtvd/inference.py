from ultralytics import YOLO
from .rtsp_stream import get_frame

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

    model = YOLO(MODEL)
    results = model(get_frame(), device="mps", verbose=False)

    for result in results:
        boxes = result.boxes
        xywh = boxes.xywh
        for detection in xywh:
            x = int(detection[0].tolist()) #TODO: check tolist()
            y = int(detection[1].tolist())
            if isIntersectingKitchen(x, y):
                kitchen_occupied = True
            if isIntersectingFrontdoor(x, y):
                frontdoor_occupied = True
    
    print("Kitchen space is occupied" if kitchen_occupied else "Kitchen space is free")
    print("Frontdoor space is occupied" if frontdoor_occupied else "Frontdoor space is free")
    # Upload to cloud storage here
