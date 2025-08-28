import requests

with open("/run/secrets/edge_config_id", "r") as f:
    EDGE_CONFIG_ID = f.read()

with open("/run/secrets/edge_access_token", "r") as f:
    EDGE_ACCESS_TOKEN = f.read()

kitchen_occupied: bool = None
frontdoor_occupied: bool = None

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
        print("Edge config updated")
    else:
        print("Error updating edge config")

def set_status(kitchen_status: bool, frontdoor_status: bool):
    global kitchen_occupied
    global frontdoor_occupied

    if (kitchen_status != kitchen_occupied or frontdoor_status != frontdoor_occupied):
        print("Car space change detected, updating edge config..")
        update_storage(kitchen_status, frontdoor_status)

    kitchen_occupied = kitchen_status
    frontdoor_occupied = frontdoor_status
