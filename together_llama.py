import requests
import config

TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
TOGETHER_API_KEY = config.TOGETHER_API_KEY

def query_llama(messages):
    """
    Sends a chat completion request to the Together AI API.

    Args:
        messages (list): A list of message dictionaries with 'role' and 'content'.

    Returns:
        str: The assistant's reply.
    """
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "messages": messages,
        "max_tokens": 150,
        "temperature": 0.7,
    }

    try:
        response = requests.post(TOGETHER_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        # this is the assistant's reply from the response
        assistant_message = result['choices'][0]['message']['content'].strip()
        return assistant_message
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response: {response.text}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None
