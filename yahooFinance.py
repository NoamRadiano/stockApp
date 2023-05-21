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
URL_TO_SCRAPE = os.getenv('URL_TO_SCRAPE')


class YahooScraping:

    # Constructor
    def __init__(self, url):
        self.url = url
        try:
            response = requests.get(url)
            data_scrape = response.text
            self.soup = BeautifulSoup(data_scrape, 'html.parser')
        except:
            print(f"Could not scrape the specific url: {url}\n")
            response.raise_for_status()

    # Returning dictionaries of each market
    def get_market_summary(self):
        get_summary = self.soup.find(
            "div", {"class": "market-summary"}).find("ul")
        listing_for_current_value = list(
            get_summary.find_all("li", recursive=False))
        points_data = [round(float(listing_for_current_value[li].find_all(
            "fin-streamer")[1]["value"]), 2) for li in range(0, 4)]
        percentage_data = [round(float(listing_for_current_value[li].find_all(
            "fin-streamer")[2]["value"]), 2) for li in range(0, 4)]
        current_value_data = [round(float(listing_for_current_value[li].find(
            "fin-streamer")["value"]), 2) for li in range(0, 4)]
        title_data = [listing_for_current_value[li].find(
            "a")["title"] for li in range(0, 4)]
        symbol = []
        for index in range(0, 4):
            if (points_data[index] < 0):
                symbol.append("⬇")
            else:
                symbol.append("⬆")
        return ({"Data For": title_data[i], "Current value": current_value_data[i], "Point": points_data[i], "Percentage": f'{percentage_data[i]}%{symbol[i]}'} for i in range(0, 4))

    # Printing the data of market summary
    def market_summary_print(self, market_summary):
        current_datetime = dt.datetime.now()
        current_date = current_datetime.strftime("%d/%m/%Y")
        current_time = current_datetime.strftime("%H:%M:%S")
        print(f'Current date: {current_date}\nCurrent time: {current_time}\n')
        for market in market_summary:
            if (market['Point'] < 0):
                arrow_color = Back.RED
            else:
                arrow_color = Back.GREEN

            print(
                f'Data for {Fore.BLUE + market["Data For"] + Style.RESET_ALL}\nCurrent value is {Fore.YELLOW}{market["Current value"]}{Style.RESET_ALL}\nPoints are {market["Point"]} {Fore.WHITE + arrow_color}({market["Percentage"]}){Style.RESET_ALL}\n')


def bringMeDataOfIndexes():
    data = YahooScraping(URL_TO_SCRAPE)
    marketsummery = data.get_market_summary()
    data.market_summary_print(marketsummery)  # printing summary
