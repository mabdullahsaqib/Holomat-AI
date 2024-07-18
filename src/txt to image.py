import os
import time
import requests
from dotenv import load_dotenv
import pollinations.ai as ai

# Load environment variables from a .env file
load_dotenv()

meshy_api_key = os.getenv("MESHY_API_KEY")
meshy_api_url = os.getenv("MESHY_API_URL")

# Initialize Pollinations AI and generate an image
model = ai.Image()
image = model.generate(
    prompt="a ninja, no background, only character, with katana, black clothes, anime style, full body",
    width=768,
    height=1280,
)

image.save("ninja.png")

# Upload the image and get the temporary URL
image_url = image.url
print(f"Image URL: {image_url}")

# Prepare payload and headers for Meshy API request
payload = {
    "image_url": image_url,
    "enable_pbr": True,
}
headers = {
    "Authorization": f"Bearer {meshy_api_key}",
    "Content-Type": "application/json"
}

# Debugging information
print(f"Payload: {payload}")
print(f"Headers: {headers}")

# Make a request to convert the image to a 3D model
try:
    response = requests.post(meshy_api_url, headers=headers, json=payload)
    response.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
    print(f"Response content: {response.content}")

# If the request is successful, process the response
if response.status_code == 200:
    print(response.json())
    task_id = response.json()["result"]
    print(f"Task ID: {task_id}")

    # Wait for some time before checking the status of the task
    time.sleep(180)

    # Check the status of the 3D model generation task
    response = requests.get(f"{meshy_api_url}/{task_id}", headers=headers)
    response.raise_for_status()

    print(response.json())
else:
    print(f"Failed to initiate the task. Status code: {response.status_code}")
    print(f"Response content: {response.content}")
