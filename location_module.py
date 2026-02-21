import geocoder
import time

def get_location():
    g = geocoder.ip('me')
    if g.latlng:
        return g.latlng[0], g.latlng[1]
    return None, None
