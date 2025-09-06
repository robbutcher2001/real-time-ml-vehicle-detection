import requests
from .logging_config import get_logger

with open("/run/secrets/edge_config_id", "r") as f:
    EDGE_CONFIG_ID = f.read().replace("\n", "")

with open("/run/secrets/edge_access_token", "r") as f:
    EDGE_ACCESS_TOKEN = f.read().replace("\n", "")

kitchen_occupied: bool = None
frontdoor_occupied: bool = None
logger = get_logger(__name__)

def update_storage(current_kitchen_status: bool, current_frontdoor_status: bool):
    url = f'https://api.vercel.com/v1/edge-config/{EDGE_CONFIG_ID}/items'
    headers = {
        'Authorization': f'Bearer {EDGE_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        "items": [
            {
                "operation": "update",
                "key": "rtvd",
                "value": {
                    "spaces": {
                        "kitchen_occupied": current_kitchen_status,
                        "frontdoor_occupied": current_frontdoor_status
                    }
                }
            }
        ]
    }
    response = requests.patch(url, json=data, headers=headers)

    if (response.status_code == 200):
        logger.info("Edge config updated")
    else:
        logger.error("Error updating edge config")

def set_status(kitchen_status: bool, frontdoor_status: bool):
    global kitchen_occupied
    global frontdoor_occupied

    if (kitchen_status != kitchen_occupied or frontdoor_status != frontdoor_occupied):
        logger.info("Car space change detected, updating edge config..")
        update_storage(kitchen_status, frontdoor_status)

    kitchen_occupied = kitchen_status
    frontdoor_occupied = frontdoor_status
