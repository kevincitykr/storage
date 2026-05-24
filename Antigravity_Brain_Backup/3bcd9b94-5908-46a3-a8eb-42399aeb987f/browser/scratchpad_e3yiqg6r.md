# Syncthing Troubleshooting Checklist

- [x] Navigate to http://localhost:8384
- [x] Open 'Actions' (작업) -> 'Logs' (로그)
- [x] Check logs for errors ('upload2601', 'error', 'failed', 'connection reset', 'timed out')
    - Result: 'Upload_2601' (IP 192.168.0.36) is connecting successfully.
    - Log entry: "Established secure connection (device=KCACWLR ... remote.name=Upload_2601)"
    - No 'error', 'failed', 'connection reset', or 'timed out' messages found in the logs.
- [x] Expand 'Kevincity Share' folder
- [x] Check for 'Failed Items' (실패한 항목)
    - Result: 'Failed Items' link is NOT present.
    - 'Out of Sync Items' (동기화 미완료 항목) exists for 'upload2601' (5,747 items, ~110 GiB), but this is normal work-in-progress, not a failure.
- [x] Report findings
