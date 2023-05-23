import customtkinter as ctk
import os
import time
from dotenv import load_dotenv
from pathlib import Path
from tkinter import messagebox
import math
import random
from PIL import Image
import smtplib
import yahooFinance
from colorama import Fore, Back, Style
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt


class DataGraph():
    def __init__(self):
        self.house_prices = np.random.normal(200000, 25000, 5000)
        plt.hist(self.house_prices, 50)
        plt.show()


hi = DataGraph()
