import requests

postcode = "UB56LH" 

url = f"https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/{postcode}"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)


if response.status_code == 200:
    
    data = response.json()["restaurants"][:10]
else:
    print(response.status_code)

print(data)