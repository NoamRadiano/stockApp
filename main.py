import requests
import customtkinter as ctk
import datetime as dt
import pandas as pd
import os
import tkinter as tk
import pandas_market_calendars as mcal
from dotenv import load_dotenv
from pathlib import Path
from send_sms import sendSms
from sharpmovement import SharpMovement
import yahooFinance
import twelve_data
from ui import AppUI
import time
import asyncio

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
URL_TO_SCRAPE = os.getenv('URL_TO_SCRAPE')
stock_name = ""


def getStockName():
    global stock_name
    stock_name = name_entry.get()
    stock_name_var.set(1)


app = AppUI()
stock_name_var = tk.StringVar()
buttonForGettingYahooData = app.makeButton(
    text="Bring me data of the indexes", row=10, column=10)
buttonForGettingYahooData._command = yahooFinance.bringMeDataOfIndexes
name_label = ctk.CTkLabel(master=app, text="Name of stock: ",
                          font=('calibre', 18, 'bold'))
name_entry = ctk.CTkEntry(master=app,
                          font=('calibre', 18, 'normal'))
name_label.grid(row=0, column=0, padx=10)
name_entry.grid(row=0, column=1)
buttonForGettingStockData = ctk.CTkButton(
    master=app, command=getStockName, text="Give me data", font=('calibre', 18, 'normal'))
buttonForGettingStockData.grid(row=0, column=2, padx=10)

buttonForGettingStockData.wait_variable(stock_name_var)
objFor1 = twelve_data.TwelveData(symbol=stock_name, interval="1min")
min_1_data = objFor1.max_diffrence_in_interval()

print(min_1_data)
app.mainloop()
