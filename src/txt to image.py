import requests
from dotenv import load_dotenv
import os

load_dotenv()

limewireapi_key = os.getenv("LIMEWIRE_API_KEY")

url = "https://api.limewire.com/api/image/generation"

payload = {
  "prompt": "a ninja, black clothes, holding a katana, anime style",
  "aspect_ratio": "1:1"
}

headers = {
  "Content-Type": "application/json",
  "X-Api-Version": "v1",
  "Accept": "application/json",
  "Authorization": f"Bearer {limewireapi_key}"
}

response = requests.post(url, json=payload, headers=headers)

data = response.json()
print(data)
# image_url = response.json()["data"]["asset_url"]
# print(image_url)