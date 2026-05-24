import requests
import re
import sys

def check_related_video(video_id):
    url = f"https://www.youtube.com/shorts/{video_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Error: Status code {response.status_code}")
            return False
            
        html = response.text
        
        # Look for the related video ID or link in the HTML
        # Usually it's in ytInitialData or similar JSON embedded in the page.
        # Let's search for the pattern of a video ID in the context of a related video.
        # We can look for "shortFormVideoRenderer" which often contains related video info.
        
        # Let's print if we find "shortFormVideoRenderer"
        if "shortFormVideoRenderer" in html:
            print("Found shortFormVideoRenderer in HTML")
        else:
            print("Did NOT find shortFormVideoRenderer in HTML")
            
        # Let's check for any "/watch?v=" links
        watch_links = re.findall(r'/watch\?v=([a-zA-Z0-9_-]{11})', html)
        print(f"Found {len(watch_links)} watch links.")
        if watch_links:
            print(f"Unique watch links: {set(watch_links)}")
            return True
            
        return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

if __name__ == "__main__":
    # Test with one of the IDs from the daemon
    test_id = "4kcUdz571eE"
    if len(sys.argv) > 1:
        test_id = sys.argv[1]
    print(f"Testing Video ID: {test_id}")
    result = check_related_video(test_id)
    print(f"Has Related Video: {result}")
