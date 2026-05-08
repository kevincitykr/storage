import requests
import json

# Syncthing API 설정
API_KEY = "w3ErEbSuoqNd9DtiifDzszosg6Rxp7My"
BASE_URL = "http://127.0.0.1:8384"
HEADERS = {"X-API-Key": API_KEY}

# 추가할 기기 정보
NEW_DEVICE_ID = "ZIJNJ42-TTXMLYV-OYNMTNB-UPVE2IK-CB75DG4-LWGWABI-MXYHSGN-TF7IGAV"
NEW_DEVICE_NAME = "New_Member_Sync"  # 기본 이름
FOLDER_ID = "rlpuk-xkiiv"  # Kevincity Share

def add_new_member():
    print(f"[*] Fetching current config from {BASE_URL}...")
    response = requests.get(f"{BASE_URL}/rest/system/config", headers=HEADERS)
    if response.status_code != 200:
        print(f"[!] Error: Failed to fetch config (Status: {response.status_code})")
        return

    config = response.json()

    # 1. 기기 리스트에 추가 (이미 있으면 스킵)
    device_exists = any(d['deviceID'] == NEW_DEVICE_ID for d in config['devices'])
    if not device_exists:
        new_device = {
            "deviceID": NEW_DEVICE_ID,
            "name": NEW_DEVICE_NAME,
            "addresses": ["dynamic"],
            "compression": "metadata",
            "certName": "",
            "introducer": False,
            "skipIntroductionRemovals": False,
            "introducedBy": "",
            "paused": False,
            "allowedNetworks": [],
            "autoAcceptFolders": False,
            "maxSendKbps": 0,
            "maxRecvKbps": 0,
            "ignoredFolders": [],
            "maxRequestKiB": 0,
            "untrusted": False,
            "remoteGUIPort": 0,
            "numConnections": 0
        }
        config['devices'].append(new_device)
        print(f"[+] Device {NEW_DEVICE_ID} added to global device list.")
    else:
        print(f"[-] Device {NEW_DEVICE_ID} already exists in global list.")

    # 2. 특정 폴더 공유 설정에 기기 추가
    folder_found = False
    for folder in config['folders']:
        if folder['id'] == FOLDER_ID:
            folder_found = True
            if not any(d['deviceID'] == NEW_DEVICE_ID for d in folder['devices']):
                folder['devices'].append({"deviceID": NEW_DEVICE_ID, "introducedBy": "", "encryptionPassword": ""})
                print(f"[+] Device {NEW_DEVICE_ID} added to folder '{folder['label']}'.")
            else:
                print(f"[-] Device {NEW_DEVICE_ID} already shared with folder '{folder['label']}'.")
            break
    
    if not folder_found:
        print(f"[!] Warning: Folder ID '{FOLDER_ID}' not found in config.")

    # 3. 변경된 설정 반영
    print("[*] Posting updated config...")
    put_response = requests.put(f"{BASE_URL}/rest/system/config", headers=HEADERS, json=config)
    
    if put_response.status_code in [200, 204]:
        print("[✔] Successfully updated Syncthing configuration!")
        # 4. 재시작 없이 반영되지만, 안정성을 위해 restart (옵션)
        # requests.post(f"{BASE_URL}/rest/system/restart", headers=HEADERS)
    else:
        print(f"[!] Error: Failed to update config (Status: {put_response.status_code})")
        print(put_response.text)

if __name__ == "__main__":
    add_new_member()
