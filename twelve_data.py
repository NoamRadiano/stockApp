import requests
import datetime as dt
import pandas as pd
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathlib import Path
from colorama import Fore, Back, Style

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
TWELVE_DATA_API = os.getenv('TWELVE_DATA_API')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
URL = "https://twelve-data1.p.rapidapi.com"
endpoint = "time_series"  # for stocks
headers = {
    "X-RapidAPI-Key": RAPID_API_KEY,
    "X-RapidAPI-Host": "twelve-data1.p.rapidapi.com"
}


class TwelveData:
    def __init__(self, symbol, endpoint="time_series", format="json", exchange="NASDAQ", interval="5min", outputsize="30", type="stock"):
        self.url = f"{URL}/{endpoint}"
        params = {}
        params.update({"interval": interval, "outputsize": outputsize, "symbol": symbol,
                      "type": type, "apikey": TWELVE_DATA_API, "exchange": exchange, "format": format, })
        try:
            response = requests.get(self.url, headers=headers, params=params)
            data = response.json()
            self.data = data
        except:
            print(f"Could not get data for the specific url: {self.url}\n")
            response.raise_for_status()

    def max_diffrence_in_interval(self):
        for data_for_min in self.data["values"]:
            max_difference = 0
            open_in_float = float(data_for_min["open"])
            close_in_float = float(data_for_min["close"])
            if (abs(open_in_float - close_in_float) > max_difference):
                max_difference = open_in_float - close_in_float
                at_time = data_for_min["datetime"].split(" ")[1]

        return {
            "interval": self.data["meta"]["interval"],
            "max_difference": round(max_difference, 2),
            "at_time": at_time,
        }
