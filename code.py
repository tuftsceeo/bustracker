"""
This example queries the Open Weather Maps site API to find out the current
weather for your location... and display it on a screen!
if you can find something that spits out JSON data, we can display it
"""
import sys
import time
import supervisor
import board
from adafruit_pyportal import PyPortal
cwd = ("/"+__file__).rsplit('/', 1)[0] # the current working directory (where this file is)
sys.path.append(cwd)
import openweather_graphics  # pylint: disable=wrong-import-position


# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

DATA_SOURCE = "https://api-v3.mbta.com/predictions?page%5Blimit%5D=2&sort=arrival_time&filter%5Bdirection_id%5D=1&filter%5Bstop%5D=2373"
DATA_LOCATION = []


# Initialize the pyportal object and let us know what data to fetch and where
# to display it
pyportal = PyPortal(url=DATA_SOURCE,
                    json_path=DATA_LOCATION,
                    status_neopixel=board.NEOPIXEL,
                    default_bg=0x000000)


gfx = openweather_graphics.OpenWeather_Graphics(pyportal.splash)


localtile_refresh = None
weather_refresh = None
while True:
    # only query the online time once per hour (and on first run)
    if (not localtile_refresh) or (time.monotonic() - localtile_refresh) > 3600:
        try:
            print("Getting time from internet!")
            pyportal.get_local_time()
            localtile_refresh = time.monotonic()
        except RuntimeError as e:
            print("Some error occured, retrying! -", e)
            continue
    try:
        value = pyportal.fetch()

        gfx.display_time(value)
        weather_refresh = time.monotonic()

        gfx.update_time()
        time.sleep(20)
         # wait 20 seconds before updating anything again
    except RuntimeError as e:

        print("main loop error occured, retrying! -", e)
        
        continue

   