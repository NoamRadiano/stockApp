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
from ui import App
import time

myApp = App()
myApp.mainloop()
