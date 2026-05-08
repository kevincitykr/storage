import json
import os
import requests

api_key = "w3ErEbSuoqNd9DtiifDzszosg6Rxp7My"
url = "http://127.0.0.1:8384/rest/config"
headers = {"X-API-Key": api_key}

response = requests.get(url, headers=headers)
config = response.json()

found = False
for folder in config['folders']:
    if folder['id'] == "os-files-etc":
        folder['path'] = "D:\\Etc\\운영체제"
        found = True

if found:
    put_response = requests.put(url, headers=headers, json=config)
    print(f"Update response: {put_response.status_code}")
else:
    print("Folder not found.")
