import json
import time
import uuid
from datetime import datetime


def create_thread_data(user_text, title=None):
    """
    Create a thread data structure similar to the output.jsonl format.

    Args:
        user_text (str): The user message content
        title (str, optional): The thread title. If None, will be generated from user_text

    Returns:
        dict: Complete thread data structure
    """
    # Generate thread ID with T prefix
    thread_id = f"T-{str(uuid.uuid4())}"

    # Current timestamp in milliseconds
    current_time_ms = int(time.time() * 1000)

    # Generate title if not provided
    if title is None:
        # Simple title generation - capitalize first letter and limit length
        title = user_text[:50] + "..." if len(user_text) > 50 else user_text
        title = title[0].upper() + title[1:] if title else "New thread"

    # Create the complete thread data structure
    thread_data = {
        "v": 3,
        "id": thread_id,
        "created": current_time_ms,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": user_text}],
                "meta": {"sentAt": current_time_ms},
            },
            {
                "role": "assistant",
                "state": {"type": "complete", "stopReason": "end_turn"},
                "content": [{"text": "Ok! Let me do that for you.", "type": "text"}],
            },
        ],
        "title": title,
    }

    return thread_data


def create_api_request_data(thread_data, bearer_token):
    """
    Create the complete API request structure for ampcode.com

    Args:
        thread_data (dict): Thread data from create_thread_data()
        bearer_token (str): Bearer token for Authorization header

    Returns:
        dict: Complete API request data structure
    """
    thread_id = thread_data["id"]
    timestamp = datetime.now().isoformat()
    body_json = json.dumps(thread_data)

    api_request = {
        "timestamp": timestamp,
        "method": "POST",
        "url": f"https://ampcode.com/api/threads/{thread_id}",
        "host": "ampcode.com",
        "port": 443,
        "path": f"/api/threads/{thread_id}",
        "query": None,
        "headers": {
            "host": "ampcode.com",
            "connection": "keep-alive",
            "X-Amp-Client-Application": "CLI",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bearer_token}",
            "accept": "*/*",
            "accept-language": "*",
            "sec-fetch-mode": "cors",
            "user-agent": "node",
            "accept-encoding": "gzip, deflate",
            "content-length": str(len(body_json)),
        },
        "body": body_json,
        "scheme": "https",
    }

    return api_request


# Example usage
if __name__ == "__main__":
    # Create thread data
    thread = create_thread_data(
        user_text="Thinking of a number between 1 and 100",
        title="Thinking of a number",
    )

    # Create API request data
    api_data = create_api_request_data(
        thread,
        "sgamp_user_01JQVWY2JWZ3RWGHVCRV1XK1HJ_c91b998631fcf3f948bec1e8c28ed225c8f7f762121b63879302a65c4cd22aa5",
    )

    # Make API call using the populated data
    import requests

    response = requests.post(
        api_data["url"], headers=api_data["headers"], data=api_data["body"]
    )
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
