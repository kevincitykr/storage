import json
import os

config_path = os.path.join(os.environ['TEMP'], 'syncthing_config.json')

with open(config_path, 'r', encoding='utf-8-sig') as f:
    config = json.load(f)

# Define the new folder
new_folder = {
    "id": "d-drive-full",
    "label": "D Drive (Full)",
    "path": "D:\\",
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
    ],
    "minDiskFree": {"value": 1, "unit": "%"},
    "versioning": {"type": "", "params": {}, "cleanupIntervalS": 3600, "fsPath": "", "fsType": "basic"},
    "copiers": 0,
    "pullerMaxPendingKiB": 0,
    "hashers": 0,
    "order": "random",
    "ignoreDelete": False,
    "scanProgressIntervalS": 0,
    "pullerPauseS": 0,
    "pullerDelayS": 1,
    "maxConflicts": 10,
    "disableSparseFiles": False,
    "paused": False,
    "markerName": ".stfolder",
    "copyOwnershipFromParent": False,
    "modTimeWindowS": 0,
    "maxConcurrentWrites": 16,
    "disableFsync": False,
    "blockPullOrder": "standard",
    "copyRangeMethod": "standard",
    "caseSensitiveFS": False,
    "junctionsAsDirs": False,
    "syncOwnership": False,
    "sendOwnership": False,
    "syncXattrs": False,
    "sendXattrs": False,
    "xattrFilter": {"maxSingleEntrySize": 1024, "maxTotalSize": 4096}
}

# Add to folders list if not already there
exists = any(f['id'] == new_folder['id'] for f in config['folders'])
if not exists:
    config['folders'].append(new_folder)
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4)
    print("Folder added to config.")
else:
    print("Folder already exists in config.")
