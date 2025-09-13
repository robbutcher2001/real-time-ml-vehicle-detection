import os
import requests
import urllib3
from .logging_config import get_logger
from typing import Literal

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

NOTIFICATION_HOOK_URL = os.environ.get('NOTIFICATION_HOOK_URL')
NOTIFICATION_OCCUPIED_HOOK_ID = os.environ.get('NOTIFICATION_OCCUPIED_HOOK_ID')
NOTIFICATION_VACANT_HOOK_ID = os.environ.get('NOTIFICATION_VACANT_HOOK_ID')

with open("/run/secrets/edge_config_id", "r") as f:
    EDGE_CONFIG_ID = f.read().replace("\n", "")

with open("/run/secrets/edge_access_token", "r") as f:
    EDGE_ACCESS_TOKEN = f.read().replace("\n", "")

with open("/run/secrets/notification_hook_key", "r") as f:
    NOTIFICATION_HOOK_KEY = f.read().replace("\n", "")

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

def send_notification(status: Literal["full", "empty_space"]):
    endpoint_id = NOTIFICATION_OCCUPIED_HOOK_ID if status == 'full' else NOTIFICATION_VACANT_HOOK_ID
    url = f'{NOTIFICATION_HOOK_URL}/proxy/protect/integration/v1/alarm-manager/webhook/{endpoint_id}'
    headers = {
        'X-API-KEY': NOTIFICATION_HOOK_KEY
    }
    response = requests.post(url, headers=headers, verify=False)

    if (response.status_code == 204):
        logger.info("Notification sent")
    else:
        logger.error("Error sending notification")

def set_status(kitchen_status: bool, frontdoor_status: bool):
    global kitchen_occupied
    global frontdoor_occupied

    if (kitchen_status != kitchen_occupied or frontdoor_status != frontdoor_occupied):
        logger.info("Car space change detected, updating edge config..")
        update_storage(kitchen_status, frontdoor_status)
    
        if (kitchen_status == True and frontdoor_status == True):
            logger.info("Both spaces are occupied, sending notification..")
            send_notification('full')
        
        if (kitchen_status == False or frontdoor_status == False):
            logger.info("Visitor space is free, sending notification..")
            send_notification('empty_space')

    kitchen_occupied = kitchen_status
    frontdoor_occupied = frontdoor_status
