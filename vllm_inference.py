import requests
import json

# Define the API endpoint
api_url = "http://127.0.0.1:8000/v1/chat/completions"

# Define the request payload
payload = {
    "model": "HarleyCooper/GRPOtuned",
    "messages": [
        {
            "role": "user",
            "content": "What is the capital of France?"
        }
    ]
}

# Convert the payload to JSON format
json_payload = json.dumps(payload)

# Set the headers
headers = {
    "Content-Type": "application/json"
}

# Send the POST request
try:
    response = requests.post(api_url, headers=headers, data=json_payload)

    # Check the response status code
    if response.status_code == 200:
        # Parse the JSON response
        response_json = response.json()
        print("vLLM Response:", response_json)
    else:
        print(f"Error: {response.status_code} - {response.text}")

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
