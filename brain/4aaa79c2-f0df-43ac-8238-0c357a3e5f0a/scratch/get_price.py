import urllib.request
import re

req = urllib.request.Request(
    'https://web.joongna.com/product/227771904', 
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
)
html = urllib.request.urlopen(req).read().decode('utf-8')

# Search for productPrice or price
match = re.search(r'"productPrice":(\d+)', html)
if not match:
    match = re.search(r'"price":(\d+)', html)
    
if match:
    print('Price:', match.group(1))
else:
    print('Price not found in HTML')
