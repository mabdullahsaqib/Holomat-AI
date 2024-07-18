import pollinations.ai as ai
import os
import time
import requests
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

meshy_api_key = os.getenv("MESHY_API_KEY")

# Version 1
model: ai.Image = ai.Image()
image: ai.ImageObject = model.generate(
      prompt="a ninja, no background, only character, with  katana, black clothes, anime style",
      # negative...width...height...height...seed...model...nologo
      width=1024,
      height=1024,
)

print(image.url)

# Prepare payload and headers for Meshy API request
payload = {
    "image_url": image.url,
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



