import requests

def internet_connection():
    try:
        response = requests.get("https://google.com/callback", timeout=5)
        return True
    except requests.ConnectionError:
        return False
