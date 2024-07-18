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
firebase_cred_path = os.getenv("FIREBASE_CRED_PATH")

# Initialize Firebase Admin SDK
cred = credentials.Certificate(firebase_cred_path)
firebase_admin.initialize_app(cred, {
    'storageBucket': firebase_storage_bucket
})

# Initialize Pollinations AI and generate an image
model = ai.Image()
image = model.generate(
    prompt="a dragon, 3D, white background, only single character model, anime style, full body",
    width=768,
    height=1280,
)


print("Initial image url : ", image.url)

# Save the generated image
image_path = "dragon.png"
image.save(image_path)

# Upload the image to Firebase Storage
bucket = storage.bucket()
blob = bucket.blob(image_path)
blob.upload_from_filename(image_path)
blob.make_public()

# Get the image URL
image_url = blob.public_url
print(f"Image URL: {image_url}")

# # Prepare payload and headers for Meshy API request
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
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
    print(f"Response content: {response.content}")
else:
    response_data = response.json()
    print(response_data)

    if 'result' in response_data:
        task_id = response_data['result']
        print(f"Task ID: {task_id}")

        # Wait for some time before checking the status of the task
        time.sleep(180)

        # Check the status of the 3D model generation task
        try:
            status_response = requests.get(f"{meshy_api_url}/{task_id}", headers=headers)
            status_response.raise_for_status()
            status_data = status_response.json()
            print(status_data)
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred when checking status: {err}")
            print(f"Response content: {status_response.content}")
    else:
        print("Failed to retrieve task ID from the response")
        print(f"Response content: {response_data}")