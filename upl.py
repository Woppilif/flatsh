import requests

with open('tess', 'rb') as f:
    r = requests.post('http://127.0.0.1:8000/file/', files={'file': f})
    print(r.status_code)