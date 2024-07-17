import time
import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("OMNIINFER_API_URL")
rapidapi_key = os.getenv("X-RAPIDAPI_KEY")
rapidapi_host = os.getenv("X-RAPIDAPI_HOST_OMNIINFER")
meshy_api_key = os.getenv("MESHY_API_KEY")


url_txt2img = url + "/txt2img"


payload = {
	"negative_prompt": "nsfw, watermark, facial distortion, lip deformity, redundant background, extra fingers, Abnormal eyesight, ((multiple faces)), ((Tongue protruding)), ((extra arm)), extra hands, extra fingers, deformity, missing legs, missing toes, missin hand, missin fingers, (painting by bad-artist-anime:0.9), (painting by bad-artist:0.9), watermark, text, error, blurry, jpeg artifacts, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, artist name, (worst quality, low quality:1.4), bad anatomy",
	"sampler_name": "Euler a",
	"batch_size": 1,
	"n_iter": 1,
	"steps": 20,
	"cfg_scale": 7,
	"seed": -1,
	"height": 1024,
	"width": 768,
	"model_name": "meinamix_meinaV9.safetensors",
	"prompt": "dragon, volcano, fire , lava "
}
headers = {
	"x-rapidapi-key": rapidapi_key,
	"x-rapidapi-host": rapidapi_host,
	"Content-Type": "application/json"
}

response = requests.post(url_txt2img, json=payload, headers=headers)

print(response.json())

task_id = response.json()["data"]["task_id"]

print(task_id)

time.sleep(60)

url_progress = url + "/progress"

querystring = {"task_id": task_id}

headers = {
	"x-rapidapi-key": rapidapi_key,
	"x-rapidapi-host": rapidapi_host,
}

response = requests.get(url_progress, headers=headers, params=querystring)

# get img url from response -> data -> img
image_url = response.json()["data"]

print(image_url)

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



