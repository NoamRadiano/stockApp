import requests
import datetime as dt
import numpy as np
import pandas as pd
import random
import time
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathlib import Path
from colorama import Fore, Back, Style
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
URL_TO_SCRAPE = os.getenv('URL_TO_SCRAPE')


class YahooScraping:

    # Constructor
    def __init__(self, url):
        self.user_agent_list = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
            'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
            'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',]
        self.url = url
        try:
            user_agent = random.choice(self.user_agent_list)
            headers = {'User-Agent': user_agent}
            response = requests.get(url, headers=headers)
            data_scrape = response.text
            self.soup = BeautifulSoup(data_scrape, 'html.parser')
        except:
            print(f"Could not scrape the specific url: {url}\n")

    # Returning dictionaries of each market
    def get_market_summary(self):
        try:
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
        except:
            print(f'Could not load data for yahoo')
            return

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
