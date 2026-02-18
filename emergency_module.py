import geocoder
from twilio.rest import Client
import datetime
import os

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

TO_NUMBER = "+91 8861397007"
FROM_NUMBER = "+1 413 493 2574"

def get_location():
    g = geocoder.ip('me')
    if g.latlng:
        return g.latlng
    return (0, 0)

def send_sos():
    lat, lon = get_location()
    location_link = f"https://maps.google.com/?q={lat},{lon}"

    # Get current timestamp
    time_now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    body = f"""
🚨 EMERGENCY ALERT 🚨
AI distress detection triggered.

Time: {time_now}
Location:
{location_link}

Please respond immediately.
"""

    message = client.messages.create(
        body=body,
        from_=FROM_NUMBER,
        to=TO_NUMBER
    )

    print("SOS SMS sent with timestamp.")
