import requests

r = requests.get("https://io.adafruit.com/api/v2/frankieson/feeds/welcome-feed?x-aio-key=aio_ZAKd12H1ixw1CcKYOeLkHqaTNHwE")
t = r.json()
print(t['last_value'])