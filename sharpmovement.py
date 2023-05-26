import requests
import datetime as dt
import pandas as pd
import os
import pandas_market_calendars as mcal
from dotenv import load_dotenv
from pathlib import Path
from send_sms import sendSms

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
ALPHA_API_KEY = os.getenv('ALPHA_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
DATE_OF_YESTERDAY = dt.date.today() - dt.timedelta(days=1)
DATE_OF_BEFORE_YESTERDAY = DATE_OF_YESTERDAY - dt.timedelta(days=1)


class SharpMovement:
    send_sms = sendSms()

    def __init__(self, stock, company_name):
        self.company_name = company_name
        self.stock = stock
        self.alpha_url_api = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&outputsize=full&symbol={stock}&apikey={ALPHA_API_KEY}'
        self.news_url_api = f'https://newsapi.org/v2/everything?q={company_name}&searchIn=title&language=en&sortBy=popularity&apiKey={NEWS_API_KEY}'

    def sharp_movement(self):
        datesIwant = {
            "yesterdayString": DATE_OF_YESTERDAY.strftime('%Y-%m-%d'),
            "beforeyesterdayString": DATE_OF_BEFORE_YESTERDAY.strftime('%Y-%m-%d')
        }

        nyse = mcal.get_calendar('NASDAQ')
        trading_dates = nyse.schedule(
            start_date=datesIwant['beforeyesterdayString'], end_date=datesIwant['yesterdayString'])
        actual_dates = {}
        count = 1
        for index, row in trading_dates.iterrows():
            if (count == 1):
                actual_dates.update(
                    {'yesterdayString': index.strftime('%Y-%m-%d')})
            if (count == 2):
                actual_dates.update(
                    {'beforeyesterdayString': index.strftime('%Y-%m-%d')})
            count += 1
        if (len(actual_dates) == 1):  # can't calculate if day before wasn't trading
            print("Could not find sharp movement, a day without trading")
            exit()
        alpha_request = requests.get(self.alpha_url_api)
        alpha_request.raise_for_status()
        alpha_data = alpha_request.json()
        yesterdayData = alpha_data['Time Series (Daily)'][actual_dates['yesterdayString']]
        beforeyesterdayData = alpha_data['Time Series (Daily)'][actual_dates['beforeyesterdayString']]
        num = float(
            yesterdayData['1. open']) / float(beforeyesterdayData['4. close'])

        try:
            news_request = requests.get(self.news_url_api)
            news_request.raise_for_status()
            news_data = news_request.json()
            newest_articles = {}
        except:
            print(
                f"Could not get data for the specific url: {self.news_url_api}\n")
            news_request.raise_for_status()
        # check if before two days and yesterday has a difference of 3% and more of the stock value
        if ((abs(num - 1)) >= 0.03):
            iter = 1

            for index in news_data['articles']:  # iter means only 1 articles
                if (iter == 2):
                    break
                newest_articles.update({index['title']: {
                    'Description': index['description'].split("\n")[1].lower()}})
                iter += 1
            if ((num - 1) > 0):
                present = f"⬆{round(abs(num-1),3)}%"
            else:
                present = f"⬇{round(abs(num-1),3)}%"
            send_sms = sendSms()
            send_sms = sendSms.send_sms(present, newest_articles)
