import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve API URLs and keys from environment variables
url = os.getenv("AI_TEXT_TO_IMAGE_API_URL")
rapidapi_key = os.getenv("X-RAPIDAPI_KEY")
rapidapi_host = os.getenv("X-RAPIDAPI_HOST_AI-t2I")
meshy_api_key = os.getenv("MESHY_API_KEY")

# Define input payload for the initial request
payload = {"inputs": "A fire dragon, standing in lava, surrounded by volcanoes"}
headers = {"x-rapidapi-key": rapidapi_key,
           "x-rapidapi-host": rapidapi_host,
           "Content-Type": "application/json"
           }

# Make the initial request to get the image URL
response = requests.post(url, json=payload, headers=headers)
response.raise_for_status()

print(response.json())
image_url = response.json()["url"]
print("image url : ", image_url)

# Prepare payload and headers for Meshy API request
payload = {
    "image_url": image_url,
    "enable_pbr": True,
}
headers = {
    "Authorization": f"Bearer {meshy_api_key}"
}

meshy_api_url = os.getenv("MESHY_API_URL")

# Make a request to convert image to 3D model
response = requests.post(meshy_api_url, headers=headers, json=payload)
response.raise_for_status()

print(response.json())
task_id = response.json()["result"]
print("task id : ", task_id)

# Wait for some time before checking the status of the task
time.sleep(180)

# Check the status of the 3D model generation task
response = requests.get(f"{meshy_api_url}/{task_id}", headers=headers)
response.raise_for_status()

print(response.json())
