import requests

url = "https://ai-text-to-image-generator-api.p.rapidapi.com/realistic"

payload = { "inputs": "A teddy bear in the storm." }
headers = {
	"x-rapidapi-key": "",
	"x-rapidapi-host": "",
	"Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())