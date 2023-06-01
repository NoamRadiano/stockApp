import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import customtkinter as ctk
import tkinter as tk
import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from pathlib import Path
from tkinter import messagebox
import math
import random
import smtplib
import yahooFinance
import datetime as dt
import twelve_data
import yfinance as yf
import seaborn as sns

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
PASS1 = os.getenv('PASS1')
PASS2 = os.getenv('PASS2')
USER1 = os.getenv('USER1')
USER2 = os.getenv('USER2')
EMAIL1 = os.getenv('EMAIL1')
EMAIL2 = os.getenv('EMAIL2')
URL_TO_SCRAPE = os.getenv('URL_TO_SCRAPE')
OTP = ""
MY_OTP = ""
BLUE = "#1F6AA5"
STOCK_SYMBOL = ""


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        self.current_datetime = dt.datetime.now()
        self.data_market = []
        self.period_val_con = True
        self.inter_val_con = True
        super().__init__(*args, **kwargs)
        self.title("StockApp")
        self.geometry(
            f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        # ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.make_menubar()
        self.make_main_page()

    def make_login_page(self):
        self.login_height = self.winfo_screenheight() - 200
        self.login_width = self.winfo_screenwidth() - 200
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.login_frame = ctk.CTkFrame(
            self, corner_radius=0,  height=self.login_height, width=self.login_width, fg_color="transparent")
        self.login_frame.grid(row=0, column=0, sticky="sew")
        self.login_frame.grid_rowconfigure(
            0, weight=1)  # Make row 0 expandable
        self.login_frame.grid_columnconfigure(
            0, weight=1)  # Make column 0 expandable
        self.login_label = ctk.CTkLabel(self.login_frame, text="Login",
                                        font=ctk.CTkFont('Calibri', 46, 'bold'))
        self.login_label.grid(row=0, column=0, padx=30,
                              pady=(40, 17))
        self.login_label.grid_columnconfigure(0, weight=1)
        self.login_label.grid_rowconfigure(0, weight=1)
        self.username_entry = ctk.CTkEntry(
            self.login_frame, width=300, height=46, placeholder_text="Username", font=ctk.CTkFont('Calibri', 24, 'bold'))
        self.username_entry.grid(
            row=1, column=0, padx=30, pady=(15, 0))
        self.username_entry.grid_rowconfigure(1, weight=1)
        self.password_entry = ctk.CTkEntry(
            self.login_frame, width=300, height=46, show="*", placeholder_text="Password", font=ctk.CTkFont('Calibri', 24, 'bold'))
        self.password_entry.grid(
            row=2, column=0, padx=30, pady=(15, 15))
        self.password_entry.grid_rowconfigure(2, weight=1)
        self.login_button = ctk.CTkButton(
            self.login_frame, text="Submit", height=46, command=self.login_event, width=300, font=ctk.CTkFont('Calibri', 34, 'bold'), anchor='center')
        self.login_button.grid(row=3, column=0,
                               pady=(15, 15), padx=30)
        self.login_button.grid_rowconfigure(3, weight=1)
        self.bind('<Return>', lambda event: self.login_button.invoke())

    def make_menubar(self):
        self.menu_bar = tk.Menu(self, font=ctk.CTkFont(
            'Calibri', 22), )
        self.m1 = tk.Menu(self.menu_bar, tearoff=0, font=ctk.CTkFont(
            'Calibri', 22), )
        self.menu_bar.add_cascade(label="File", menu=self.m1)
        self.m1.add_command(label="Graphs", command=self.open_graph_label)
        self.m1.add_command(label="Statistics Graphs",
                            command=self.open_statistics_graphs_label)

        # self.m2 = tk.Menu(self.menu_bar, tearoff=0, font=ctk.CTkFont(
        #     'Calibri', 22), )
        # self.menu_bar.add_cascade(label="Setting", menu=self.m2)
        # self.m2.add_command(label="Light theme",)
        # self.m2.add_command(label="System theme",)

        # self.m3 = tk.Menu(self.menu_bar, tearoff=0, font=ctk.CTkFont(
        #     'Calibri', 22), )
        # self.menu_bar.add_cascade(label="Help", menu=self.m3)
        # self.m3.add_command(label="help!")
        self.config(menu=self.menu_bar)

    def make_second_main_frame(self):
        # create second main frame
        self.grid_columnconfigure((0, 1), weight=1)  # type: ignore
        self.grid_rowconfigure((0, 1), weight=1)  # type: ignore
        self.second_main_frame = ctk.CTkFrame(
            self, fg_color="#2E3033", bg_color="#2E3033")  # border_color="red", border_width=2
        # configure grid layout (2x2)
        self.second_main_frame.grid_columnconfigure((0, 1), weight=1)
        self.second_main_frame.grid_rowconfigure(
            (0, 1), weight=1)  # type: ignore
        self.second_main_frame.grid(row=0, column=0)
        ###
        # creating first frame
        self.first_frame_in_statistics_page = ctk.CTkFrame(
            self.second_main_frame,  width=450, height=self.winfo_screenheight(), bg_color="#2E3033", fg_color="#2E3033")  # border_color="pink", border_width=2
        self.first_frame_in_statistics_page.grid(
            row=0, column=0,  sticky="nsew")
        self.first_frame_in_statistics_page.grid_columnconfigure(0, weight=0)
        self.first_frame_in_statistics_page.grid_rowconfigure(0, weight=0)
        self.data_label_for_stock = ctk.CTkLabel(
            self.first_frame_in_statistics_page, text=f"{STOCK_SYMBOL} Data", font=ctk.CTkFont('Calibri', 40, 'bold'))

        self.data_label_for_stock.grid(row=0, column=0, padx=20, pady=(20, 10))

    def open_statistics_graphs_label(self):
        self.main_frame.grid_forget()
        self.make_second_main_frame()

    def open_graph_label(self):
        self.second_main_frame.grid_forget()
        self.main_frame.grid(row=0, column=0)

    def get_interval_value_event(self, interval_value: str):
        self.interval_value = interval_value.replace(" ", "")

    def get_period_value_event(self, period_value: str):
        self.period_value = period_value.replace(" ", "")

    def get_result_function_event(self, result_function: str):
        self.result_function = result_function

    def print_results_and_build_graph_and_ibframe(self, entry):
        self.results_textbox.configure(state="normal")
        global STOCK_SYMBOL
        self.function_data = ""
        self.results_textbox.delete('1.0', 'end')
        STOCK_SYMBOL = entry.get()
        STOCK_SYMBOL = STOCK_SYMBOL.upper()
        # entry.delete(0, 'end')
        if (len(self.period_value) > 3):
            if (self.period_value == "1day" or self.period_value == "5days" or self.period_value == "1year" or self.period_value == "2years" or self.period_value == "5years"):
                self.period_value = self.period_value[:1] + \
                    self.period_value[1:2]
            elif (self.period_value == "1month" or self.period_value == "3months" or self.period_value == "6months"):
                self.period_value = self.period_value[:1] + \
                    self.period_value[1:3]
            elif (self.period_value == "10years"):
                self.period_value = self.period_value[:2] + \
                    self.period_value[2:3]
            elif (self.period_value == "Yeartodate"):
                self.period_value = "ytd"
            elif (self.period_value == "max"):
                self.period_value = "max"
            else:
                pass
        if (len(self.interval_value) > 3):
            if (self.interval_value == "1min" or self.interval_value == "5min" or self.interval_value == "1hour" or self.interval_value == "1day" or self.interval_value == "5days"):
                self.interval_value = self.interval_value[:1] + \
                    self.interval_value[1:2]
            elif (self.interval_value == "1month" or self.interval_value == "3months"):
                self.interval_value = self.interval_value[:1] + \
                    self.interval_value[1:3]
            elif (self.interval_value == "15min" or self.interval_value == "30min"):
                self.interval_value = self.interval_value[:2] + \
                    self.interval_value[2:3]
            elif (self.interval_value == "1week"):
                self.interval_value = "1wk"
            else:
                pass

        self.stock = yf.Ticker(STOCK_SYMBOL)
        self.stock_history_data = self.stock.history(
            period=self.period_value, interval=self.interval_value)
        self.data_for_results_textbox = self.stock_history_data.drop(
            ['Dividends', 'Stock Splits'], axis=1)
        self.results_textbox.insert(
            "0.0", self.data_for_results_textbox.describe().round(2))
        self.results_textbox.configure(state="disabled")
        self.make_graphs(self.stock_history_data)
        self.build_ib_frame()

    def make_graphs(self, stock_data):
        self.candle_width = 0.9   # width of real body
        self.candle_shadow_width = 0.05  # width of shadow
        self.fig, self.axes = plt.subplots()
        self.fig.set_figheight(5)
        self.fig.set_figwidth(9)
        self.fig.set_alpha(1)
        self.fig.set_facecolor(color="#2E3033")
        self.axes.plot(stock_data.index, stock_data['Open'],
                       label=f"{STOCK_SYMBOL} Stock", alpha=1, lw=1, ls='-', marker='s', markersize=1, markeredgecolor="blue")
        self.axes.set_xlabel('Dates', fontdict={
            'size': 12, 'weight': 'bold', })
        self.axes.set_ylabel('Open Price', fontdict={
            'size': 12, 'weight': 'bold', })
        self.axes.set_title(f'{STOCK_SYMBOL} Graph', fontdict={
            'size': 14, 'weight': 'bold', })
        self.axes.legend()
        self.line = FigureCanvasTkAgg(self.fig, self.graph_frame)
        self.line.get_tk_widget().grid(row=0, column=0, sticky="nsew",)
        self.line.get_tk_widget().grid_columnconfigure(0, weight=1)
        self.line.get_tk_widget().grid_rowconfigure(0, weight=1)

        self.fig1, self.axes1 = plt.subplots()
        self.fig1.set_figheight(5)
        self.fig1.set_figwidth(9)
        self.fig1.set_alpha(1)
        self.fig1.set_facecolor(color="#2E3033")
        # find the rows that are bullish
        dfup = stock_data[stock_data['Close']
                          >= stock_data['Open']]
        # find the rows that are bearish
        dfdown = stock_data[stock_data['Close']
                            < stock_data['Open']]
        # plot the bullish candle stick
        self.axes1.bar(dfup.index, dfup['Close'] - dfup["Open"], self.candle_width,
                       bottom=dfup["Open"], edgecolor='g', color='green')
        self.axes1.bar(dfup.index, dfup['High'] - dfup['Close'], self.candle_shadow_width,
                       bottom=dfup['Close'], edgecolor='g', color='green')
        self.axes1.bar(dfup.index, dfup['Low'] - dfup["Open"], self.candle_shadow_width,
                       bottom=dfup["Open"], edgecolor='g', color='green')
        # plot the bearish candle stick
        self.axes1.bar(dfdown.index, dfdown['Close'] - dfdown["Open"], self.candle_width,
                       bottom=dfdown["Open"], edgecolor='r', color='red')
        self.axes1.bar(dfdown.index, dfdown['High'] - dfdown["Open"], self.candle_shadow_width,
                       bottom=dfdown["Open"], edgecolor='r', color='red')
        self.axes1.bar(dfdown.index, dfdown['Low'] - dfdown['Close'], self.candle_shadow_width,
                       bottom=dfdown['Close'], edgecolor='r', color='red')
        self.axes1.set_xlabel(
            'Dates', fontdict={'size': 12, 'weight': 'bold', })
        self.axes1.set_ylabel('Open Price', fontdict={
            'size': 12, 'weight': 'bold', })
        self.axes1.set_title(f'{STOCK_SYMBOL} Candles', fontdict={
            'size': 14, 'weight': 'bold', })
        # self.axes1.legend()
        self.chart = FigureCanvasTkAgg(self.fig1, self.graph_frame)
        self.chart.get_tk_widget().grid(row=1, column=0, sticky="nsew")
        self.chart.get_tk_widget().grid_columnconfigure(0, weight=1)
        self.chart.get_tk_widget().grid_rowconfigure(1, weight=1)

    def textbox_data(self):
        self.current_date = self.current_datetime.strftime("%d/%m/%Y")
        self.current_time = self.current_datetime.strftime("%H:%M:%S")
        self.stock_indexes_textbox.tag_config("tag_name", justify='center')
        self.stock_indexes_textbox.configure(state="normal")
        data = yahooFinance.YahooScraping(URL_TO_SCRAPE)
        marketsummery = data.get_market_summary()
        if (marketsummery):
            if not (self.data_market):
                self.data_market.clear()
            for market in marketsummery:
                self.data_market.append(
                    f'Data of {market["Data For"]}\nCurrent value is {market["Current value"]}\nPoints {market["Point"]} ({market["Percentage"]})\n\n')
        else:
            self.data_market.append("")
        self.stock_indexes_textbox.delete("1.0", "end")
        self.stock_indexes_textbox.insert(
            ctk.INSERT, text=f"{self.current_date}\n{self.current_time}\n\n")
        for data in self.data_market:
            self.stock_indexes_textbox.insert(ctk.INSERT, data)
        self.stock_indexes_textbox.tag_add("tag_name", "1.0", "end")
        self.stock_indexes_textbox.configure(state="disabled")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def error_message_for_details(self):
        messagebox.showwarning(
            "Invalid input", "Your password or username is incorrect.\nPlease try again.")

    def error_message_for_OTP(self, top1):
        messagebox.showwarning(
            "Invalid input", "Your OTP key is incorrect.\nPlease try again.", parent=top1)

    def error_message_for_email(self, top):
        messagebox.showwarning(
            "Invalid input", "Your email is not exist.\nPlease try again.", parent=top)

    def make_main_page(self):
        # create main frame
        self.grid_columnconfigure((0, 1, 2), weight=1)  # type: ignore
        self.grid_rowconfigure((0, 1, 2), weight=1)  # type: ignore
        self.main_frame = ctk.CTkFrame(
            self, fg_color="#2E3033", bg_color="#2E3033")  # border_color="red", border_width=2
        # configure grid layout (3x3)
        self.main_frame.grid_columnconfigure((0, 2), weight=0)  # type: ignore
        self.main_frame.grid_columnconfigure((1), weight=1)
        self.main_frame.grid_rowconfigure((0, 1, 2), weight=1)  # type: ignore
        self.main_frame.grid(row=0, column=0)
        ###
        # creating first frame
        self.first_frame = ctk.CTkFrame(
            self.main_frame,  width=140, height=self.winfo_screenheight(), bg_color="#2E3033", fg_color="#2E3033")  # border_color="pink", border_width=2
        self.first_frame.grid(row=0, column=0,  sticky="nsew")
        self.first_frame.grid_columnconfigure(0, weight=0)
        self.first_frame.grid_rowconfigure(4, weight=1)
        self.STOCK_SYMBOL = ctk.CTkLabel(
            self.first_frame, text="Stock Symbol", font=ctk.CTkFont('Calibri', 25, 'bold'))
        self.STOCK_SYMBOL.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.stockname_entry = ctk.CTkEntry(
            self.first_frame, width=170, height=35, placeholder_text="Stock Symbol", font=ctk.CTkFont('Calibri', 21, 'bold'))
        self.stockname_entry.grid(row=1, column=0, padx=20)
        self.search_for_stock_button = ctk.CTkButton(
            self.first_frame, text="Submit", height=37, width=170, font=ctk.CTkFont('Calibri', 25, 'bold'), command=lambda: self.print_results_and_build_graph_and_ibframe(entry=self.stockname_entry))
        self.search_for_stock_button.grid(row=2, column=0, padx=20, pady=10)
        self.bind(
            '<Return>', lambda event: self.search_for_stock_button.invoke())
        self.stock_indexes_textbox = ctk.CTkTextbox(
            self.first_frame, font=ctk.CTkFont('Calibri', 20, 'bold'), width=265, height=425, corner_radius=25, border_width=6,)
        self.stock_indexes_textbox.grid(row=3, column=0, padx=(
            15, 15), pady=(30, 0), sticky="nsew")
        self.textbox_data()
        ###
        self.appearance_mode_label = ctk.CTkLabel(
            self.first_frame, text="Appearance Mode", font=ctk.CTkFont('Calibri', 20, 'bold'), anchor="w")
        self.appearance_mode_label.grid(
            row=5, column=0, padx=(0, 0), pady=(10, 0))
        self.appearance_mode_optionmenu = ctk.CTkOptionMenu(self.first_frame, values=["Dark", "Light", "System"], font=ctk.CTkFont(
            'Calibri', 13, 'bold'), command=self.change_appearance_mode_event)
        self.appearance_mode_optionmenu.grid(
            row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = ctk.CTkLabel(
            self.first_frame, text="UI Scaling", anchor="w", font=ctk.CTkFont('Calibri', 20, 'bold'),)
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionmenu = ctk.CTkOptionMenu(self.first_frame, values=["90%", "100%", "110%", "120%"], font=ctk.CTkFont('Calibri', 13, 'bold'),
                                                    command=self.change_scaling_event)
        self.scaling_optionmenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        ###
        # creating second frame
        self.second_frame = ctk.CTkFrame(
            self.main_frame,  width=(self.winfo_screenwidth() // 5 * 2), height=self.winfo_screenheight(), bg_color="#2E3033", fg_color="#2E3033")  # border_color="blue", border_width=2
        self.second_frame.grid(row=0, column=1, sticky="nsew", padx=15)
        self.second_frame.grid_columnconfigure((0, 1), weight=1)
        self.second_frame.grid_rowconfigure(
            (0, 1, 2, 3, 4), weight=1)  # type: ignore

        self.variable_for_stock_frame = ctk.CTkFrame(
            self.second_frame,  width=(self.winfo_screenwidth() // 5 * 2), fg_color="transparent")  # border_color="orange", border_width=2
        self.variable_for_stock_frame.grid(row=0, column=0, sticky="nsew")
        self.variable_for_stock_frame.grid_columnconfigure(
            (0, 1, 2), weight=1)
        self.variable_for_stock_frame.grid_rowconfigure(2, weight=1)

        self.interval_label = ctk.CTkLabel(
            self.variable_for_stock_frame, text="Interval", font=ctk.CTkFont('Calibri', 25, 'bold'))
        self.interval_label.grid(
            row=0, column=0, padx=10, pady=(20, 10))
        self.interval_value = "1day"  # default value
        # "1 min", "5 min", "15 min", "30 min", "1 hour",
        self.interval_optionmenu = ctk.CTkOptionMenu(self.variable_for_stock_frame, values=["1 day", "5 days", "1 week", "1 month", "3 months"], font=ctk.CTkFont(
            'Calibri', 20, 'bold'), command=self.get_interval_value_event, anchor='center')
        self.interval_optionmenu.grid(
            row=1, column=0, padx=10, pady=(0, 25))
        self.output_size_label = ctk.CTkLabel(
            self.variable_for_stock_frame, text="Period", font=ctk.CTkFont('Calibri', 25, 'bold'))
        self.output_size_label.grid(
            row=0, column=1, padx=10, pady=(20, 10))
        self.period_value = "5days"  # default value
        # 1 day
        self.period_size_optionmenu = ctk.CTkOptionMenu(self.variable_for_stock_frame, values=["5 days", "1 month", "3 months", "6 months", "1 year", "2 years", "5 years", "10 years", "Year to date", "max"], font=ctk.CTkFont(
            'Calibri', 20, 'bold'), command=self.get_period_value_event, anchor='center')
        self.period_size_optionmenu.grid(
            row=1, column=1, padx=10, pady=(0, 25))

        self.result_function_label = ctk.CTkLabel(
            self.variable_for_stock_frame, text="Result Function", font=ctk.CTkFont('Calibri', 25, 'bold'))
        self.result_function_label.grid(
            row=0, column=2, padx=10, pady=(20, 10))
        self.result_function_optionmenu = ctk.CTkOptionMenu(self.variable_for_stock_frame, values=["function", "function", "function", "function", "function", "function", "function", "function"], font=ctk.CTkFont(
            'Calibri', 20, 'bold'), command=self.get_result_function_event, anchor='center')
        self.result_function_optionmenu.grid(
            row=1, column=2, padx=10, pady=(0, 25))

        self.results_textbox = ctk.CTkTextbox(
            self.variable_for_stock_frame, font=ctk.CTkFont('Calibri', 24, 'bold'), corner_radius=25, border_width=6, border_spacing=10, width=(self.winfo_screenwidth() // 5 * 2), height=440)
        self.results_textbox.grid(row=2, column=0, columnspan=3, sticky="nsew")
        self.results_textbox.grid_columnconfigure(
            0, weight=1)  # result of query
        self.results_textbox.grid_rowconfigure(0, weight=1)
        self.results_textbox.configure(state="disabled")
        ##
        ##
        ###
        # matplotlib frame (third frame)
        self.graph_frame = ctk.CTkFrame(
            self.main_frame,  width=int((self.winfo_screenwidth() // 5 * 2.5)), height=self.winfo_screenheight(), fg_color="#2E3033", bg_color="#2E3033")  # border_color="green", border_width=2
        self.graph_frame.grid(row=0, column=2, sticky="nsew")
        self.graph_frame.grid_rowconfigure((0, 1), weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)
        ##
        ##
        plt.style.use('dark_background')
        self.fig, self.axes = plt.subplots()
        self.fig.set_figheight(5)
        self.fig.set_figwidth(9)
        self.fig.set_alpha(1)
        self.fig.set_facecolor(color="#2E3033")
        self.line = FigureCanvasTkAgg(self.fig, self.graph_frame)
        self.line.get_tk_widget().grid(row=0, column=0, sticky="nsew",)
        self.line.get_tk_widget().grid_columnconfigure(0, weight=1)
        self.line.get_tk_widget().grid_rowconfigure(0, weight=1)
        ##
        ##
        self.fig1, self.axes1 = plt.subplots()
        self.fig1.set_figheight(5)
        self.fig1.set_figwidth(9)
        self.fig1.set_alpha(1)
        self.fig1.set_facecolor(color="#2E3033")
        self.chart = FigureCanvasTkAgg(self.fig1, self.graph_frame)
        self.chart.get_tk_widget().grid(row=1, column=0, sticky="nsew")
        self.chart.get_tk_widget().grid_columnconfigure(0, weight=1)
        self.chart.get_tk_widget().grid_rowconfigure(1, weight=1)

    def build_ib_frame(self):
        self.ib_label = ctk.CTkLabel(
            self.second_frame, text=f"{STOCK_SYMBOL} Stock", font=ctk.CTkFont('Calibri', 24, 'bold'), width=(self.winfo_screenwidth() // 5 * 2), fg_color="transparent")  # border_color="purple", border_width=2,
        self.ib_label.grid(row=1, column=0, sticky="nsew", pady=15)
        self.ib_label.grid_columnconfigure(
            0, weight=1)
        ##
        ##
        self.ask_price_button = ctk.CTkButton(
            self.second_frame, text=f"Ask Price: ", height=46, width=170, font=ctk.CTkFont('Calibri', 25, 'bold'))
        self.ask_price_button.grid(row=2, column=0)
        self.ask_price_button.grid_columnconfigure(
            0, weight=1)
        self.ask_price_button.configure(state="disabled")
        ##
        ##
        self.frame_for_buy_and_sell = ctk.CTkFrame(
            self.second_frame,  width=(self.winfo_screenwidth() // 5 * 2), fg_color="transparent")  # border_color="orange", border_width=2
        self.frame_for_buy_and_sell.grid(row=3, column=0, sticky="nsew")
        self.frame_for_buy_and_sell.grid_columnconfigure(
            (0, 1), weight=1)
        self.frame_for_buy_and_sell.grid_rowconfigure(0, weight=1)
        ##
        ##
        self.sell_stock_button = ctk.CTkButton(
            self.frame_for_buy_and_sell, text="Sell Stock", height=42, width=122, font=ctk.CTkFont('Calibri', 25, 'bold'))
        self.sell_stock_button.grid(
            row=0, column=0,)
        self.sell_stock_button.grid_columnconfigure(
            0, weight=1)
        ##
        ##
        self.buy_stock_button = ctk.CTkButton(
            self.frame_for_buy_and_sell, text="Buy Stock", height=42, width=122, font=ctk.CTkFont('Calibri', 25, 'bold'))
        self.buy_stock_button.grid(
            row=0, column=1)
        self.buy_stock_button.grid_columnconfigure(
            1, weight=1)

    def verify_OTP(self, top1, entry1):
        global OTP
        global MY_OTP
        MY_OTP = entry1.get()
        if (MY_OTP == OTP):
            self.login_frame.grid_forget()
            top1.destroy()  # remove OTP frame
            self.make_main_page()
        else:
            entry1.delete(0, 'end')
            MY_OTP = ""
            self.error_message_for_OTP(top1)

    def verify_window_for_OTP(self, entry, top, text, placeholder_text):
        global OTP
        global MY_OTP
        global EMAIL1
        global EMAIL2
        digits = "0123456789"
        email_var = entry.get()
        if ((email_var == EMAIL1) or (email_var == EMAIL2)):
            for i in range(6):
                OTP += digits[math.floor(random.random()*10)]
            otp = OTP + " is your OTP"
            message = otp
            try:
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login("pookloko57@gmail.com", "cqkeutyeuvrqbyyc")
                s.sendmail('&&&&&&', email_var, message)
            except:
                print("Could not send OTP email")
            top.destroy()  # remove EMAIL frame
            top1 = ctk.CTkToplevel(self, )
            top1.title("Verify")
            top1.grid_rowconfigure((0, 1, 2, 3), weight=1)  # type: ignore
            top1.grid_columnconfigure(0, weight=1)
            top1.geometry("350x300")
            top1.resizable(False, False)
            # place in center window
            self.eval(f'tk::PlaceWindow {str(top1)} center')
            otp_label = ctk.CTkLabel(top1, text=text,
                                     font=ctk.CTkFont('Calibri', 30, 'bold'), width=300, height=26)
            otp_label.grid(row=0, column=0, padx=20, pady=(7, 7))
            otp_label.grid_rowconfigure(0, weight=1)
            entry1 = ctk.CTkEntry(
                top1, placeholder_text=placeholder_text, width=300, height=46, font=ctk.CTkFont('Calibri', 24, 'bold'))
            entry1.grid(row=1, column=0, padx=20, pady=(7, 7))
            entry1.grid_rowconfigure(1, weight=1)
            send_otp_button = ctk.CTkButton(
                top1, text="Verify", height=46, command=lambda: self.verify_OTP(top1, entry1), width=300, font=ctk.CTkFont('Calibri', 25, 'bold'), anchor='center')
            top1.bind('<Return>', lambda event: send_otp_button.invoke())
            send_otp_button.grid(row=2, column=0, padx=20, pady=(7, 7))
            send_otp_button.grid_rowconfigure(2, weight=1)

        else:
            entry.delete(0, 'end')
            self.error_message_for_email(top)

    def verify_window_for_email(self, text, placeholder_text):
        top = ctk.CTkToplevel(self, )
        top.title("Verify")
        top.grid_rowconfigure((0, 1, 2, 3), weight=1)  # type: ignore
        top.grid_columnconfigure(0, weight=1)
        top.geometry("350x300")
        top.resizable(False, False)
        # place in center window
        self.eval(f'tk::PlaceWindow {str(top)} center')
        email_label = ctk.CTkLabel(top, text=text,
                                   font=ctk.CTkFont('Calibri', 30, 'bold'), width=300, height=26)
        email_label.grid(row=0, column=0, padx=20, pady=(7, 7))
        email_label.grid_rowconfigure(0, weight=1)
        entry = ctk.CTkEntry(
            top, placeholder_text=placeholder_text, width=300, height=46, font=ctk.CTkFont('Calibri', 24, 'bold'))
        entry.grid(row=1, column=0, padx=20, pady=(7, 7))
        entry.grid_rowconfigure(1, weight=1)
        send_mail_button = ctk.CTkButton(
            top, text="Send code", height=46, command=lambda: self.verify_window_for_OTP(entry, top, text="Enter your OTP code", placeholder_text="OTP code"), width=300, font=ctk.CTkFont('Calibri', 25, 'bold'), anchor='center')
        top.bind('<Return>', lambda event: send_mail_button.invoke())
        send_mail_button.grid(row=2, column=0, padx=20, pady=(7, 7))
        send_mail_button.grid_rowconfigure(2, weight=1)

    def login_event(self):
        user_entry = self.username_entry.get()
        pass_entry = self.password_entry.get()
        if ((user_entry == USER1 and pass_entry == PASS1) or (user_entry == USER2 and pass_entry == PASS2)):
            self.verify_window_for_email(text="Verify By Email",
                                         placeholder_text="Your Email")
        else:
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.error_message_for_details()


# if __name__ == "__main__":
#     app = App()
#     app.mainloop()
