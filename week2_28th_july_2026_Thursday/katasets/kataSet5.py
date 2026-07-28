import requests
url = "https://jsonplaceholder.typicode.com/posts/1"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    print(f"Status Code: {response.status_code}")
    print(f"Title: {data['title']}")

except requests.exceptions.RequestException as e:
    print("Request failed:", e)