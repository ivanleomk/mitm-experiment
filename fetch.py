from datetime import datetime
import requests
import os
import json


def create_sync_request(bearer_token):
    """
    Create a sync request to ampcode.com API

    Args:
        bearer_token (str): Bearer token for Authorization header

    Returns:
        dict: API request data structure
    """
    timestamp = datetime.now().isoformat()

    api_request = {
        "timestamp": timestamp,
        "method": "POST",
        "url": "https://ampcode.com/api/threads/sync",
        "scheme": "https",
    }

    return api_request


# Create the request
api_key = os.getenv("AMP_API_KEY")
request_data = create_sync_request(api_key)

headers = {
    "host": "ampcode.com",
    "connection": "keep-alive",
    "X-Amp-Client-Application": "CLI",
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
    "accept": "*/*",
    "accept-language": "*",
    "sec-fetch-mode": "cors",
    "user-agent": "node",
    "accept-encoding": "gzip, deflate",
    "content-length": "85",
}

# Make the API call
response = requests.get(
    "https://ampcode.com/api/threads",
    headers={
        "Authorization": f"Bearer {api_key}",
        "host": "ampcode.com",
        "connection": "keep-alive",
        "X-Amp-Client-Application": "CLI",
        "Content-Type": "application/json",
    },
)

# Get JSON response and write to file
response_json = response.json()
with open("output.json", "w") as f:
    json.dump(response_json, f, indent=2)
