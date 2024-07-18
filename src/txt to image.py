import os
import time
import requests
from dotenv import load_dotenv
import pollinations.ai as ai
import firebase_admin
from firebase_admin import credentials, storage

# Load environment variables from a .env file
load_dotenv()

meshy_api_key = os.getenv("MESHY_API_KEY")
meshy_api_url = os.getenv("MESHY_API_URL")
firebase_storage_bucket = os.getenv("FIREBASE_STORAGE_BUCKET")

# Initialize Firebase Admin SDK
cred = credentials.Certificate("C:/Users/Administrator/Documents/DOCUMENTS/holomat-ai-firebase-adminsdk-tjlnn-198fa2071b.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': firebase_storage_bucket
})

# Initialize Pollinations AI and generate an image
model = ai.Image()
image = model.generate(
    prompt="a ninja, no background, only character, with katana, black clothes, anime style, full body",
    width=768,
    height=1280,
)

# Save the generated image
image_path = "ninjaGo.png"
image.save(image_path)

# Upload the image to Firebase Storage
bucket = storage.bucket()
blob = bucket.blob(image_path)
blob.upload_from_filename(image_path)

# Get the image URL
image_url = blob.public_url
print(f"Image URL: {image_url}")

# # Prepare payload and headers for Meshy API request
# payload = {
#     "image_url": image_url,
#     "enable_pbr": True,
# }
# headers = {
#     "Authorization": f"Bearer {meshy_api_key}",
#     "Content-Type": "application/json"
# }
#
# # Debugging information
# print(f"Payload: {payload}")
# print(f"Headers: {headers}")
#
# # Make a request to convert the image to a 3D model
# try:
#     response = requests.post(meshy_api_url, headers=headers, json=payload)
#     response.raise_for_status()
# except requests.exceptions.HTTPError as err:
#     print(f"HTTP error occurred: {err}")
#     print(f"Response content: {response.content}")
#
# # If the request is successful, process the response
# if response.status_code == 200:
#     print(response.json())
#     task_id = response.json()["result"]
#     print(f"Task ID: {task_id}")
#
#     # Wait for some time before checking the status of the task
#     time.sleep(180)
#
#     # Check the status of the 3D model generation task
#     response = requests.get(f"{meshy_api_url}/{task_id}", headers=headers)
#     response.raise_for_status()
#
#     print(response.json())
# else:
#     print(f"Failed to initiate the task. Status code: {response.status_code}")
#     print(f"Response content: {response.content}")
