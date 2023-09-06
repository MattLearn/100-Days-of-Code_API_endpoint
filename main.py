import requests
from datetime import datetime
import smtplib

MY_EMAIL = "email here"
MY_PASS = "pass here"
MY_LAT = 18.017874
MY_LNG = -76.809906
TIMENOW = str(datetime.now().hour)


def is_iss_above():
    iss_feed = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_feed.raise_for_status()
    # data = iss_feed.json()["iss_position"]
    iss_lng = iss_feed.json()["iss_position"]["longitude"]
    iss_lat = iss_feed.json()["iss_position"]["latitude"]
    if (MY_LAT-5) <= iss_lat <= (MY_LAT+5) and (MY_LNG - 5) <= iss_lng <= (MY_LNG + 5):
        # print("true")
        return True


def is_it_night():
    my_params = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }

    sunrise_feed = requests.get(url="https://api.sunrise-sunset.org/json", params=my_params)
    sunrise_feed.raise_for_status()
    sunrise_time = (sunrise_feed.json()["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_time = (sunrise_feed.json()["results"]["sunset"].split("T")[1].split(":")[0])
    # print(f"Sunrise:{sunrise_time}\nSunset:{sunset_time}")
    if TIMENOW >= sunset_time or TIMENOW <= sunrise_time:
        # print("it's night")
        return True


if is_it_night() and is_iss_above():
    connection = smtplib.SMTP("url here")
    connection.starttls()
    connection.login(MY_EMAIL, MY_PASS)
    connection.sendmail(
        from_addr=MY_EMAIL,
        to_addrs=MY_EMAIL,
        msg="Subject: The ISS is overhead!\n\nTry to find the ISS in the sky!"
    )
    connection.quit()

    # print("look at the sky")
