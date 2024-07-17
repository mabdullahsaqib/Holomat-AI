import time
import requests

url = "https://omniinfer.p.rapidapi.com/v2/txt2img"

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
	"prompt": "ninja, dragon, 2d, flying monsters, animated, anime, sword"
}
headers = {
	"x-rapidapi-key": "",
	"x-rapidapi-host": "",
	"Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())

task_id = response.json()["data"]["task_id"]

print(task_id)

time.sleep(10)

url = "https://omniinfer.p.rapidapi.com/v2/progress"

querystring = {"task_id": task_id}

headers = {
	"x-rapidapi-key": "",
	"x-rapidapi-host": ""
}

response = requests.get(url, headers=headers, params=querystring)

# get img url from response -> data -> img
img_url = response.json()["data"]

print(img_url)



