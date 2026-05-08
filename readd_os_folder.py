import json
import requests

api_key = "w3ErEbSuoqNd9DtiifDzszosg6Rxp7My"
url = "http://127.0.0.1:8384/rest/config"
headers = {"X-API-Key": api_key}

response = requests.get(url, headers=headers)
config = response.json()

# Define the new folder with English path
new_folder = {
    "id": "os-setup",
    "label": "OS_Setup",
    "path": "D:\\Etc\\OS_Setup",
    "type": "sendreceive",
    "rescanIntervalS": 3600,
    "fsWatcherEnabled": True,
    "fsWatcherDelayS": 10,
    "fsWatcherTimeoutS": 0,
    "ignorePerms": False,
    "autoNormalize": True,
    "filesystemType": "basic",
    "devices": [
        {"deviceId": "AEPVQL6-RJJPJRK-4YYKAWZ-L3WXNAS-B2BNGGQ-BI65YSG-XIGDKAZ-ARD5MA6"}, # New_AI_Factory_PC
        {"deviceId": "TUDFJIN-RRC7UEN-OTOSXHQ-2R7Z5L7-5UQHV2L-BVC7VRR-DWJN7HZ-MXKFLQZ"}, # kevin_kingdom
        {"deviceId": "UW5V5CO-T4XDF3O-Y522MUS-FR46E2D-GRFH5KT-FIYWM5S-NWDBKOQ-3A7ZYAL"}  # kevincityHQ (self)
    ]
}

# Clean up any existing versions of this folder
config['folders'] = [f for f in config['folders'] if f['id'] not in ["os-setup", "os-files-etc"]]
config['folders'].append(new_folder)

put_response = requests.put(url, headers=headers, json=config)
print(f"Update response: {put_response.status_code}")
