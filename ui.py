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
import twelve_data

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
        self.current_date = self.current_datetime.strftime("%d/%m/%Y")
        self.current_time = self.current_datetime.strftime("%H:%M:%S")
        self.start_time = time.time()
        self.data_market = []
        super().__init__(*args, **kwargs)
        self.title("StockApp")
        self.geometry(
            f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        ###
        #
        # # create login frame
        login_height = self.winfo_screenheight() - 200
        login_width = self.winfo_screenwidth() - 200
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.login_frame = ctk.CTkFrame(
            self, corner_radius=0,  height=login_height, width=login_width, fg_color="transparent")
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

    def get_interval_value_event(self, interval_value: str):
        self.interval_value = interval_value.replace(" ", "")

    def get_output_size_value_event(self, output_size_value: str):
        self.output_size_value = output_size_value

    def get_result_function_event(self, result_function: str):
        self.result_function = result_function

    def print_in_results_textbox(self, entry):
        self.results_textbox.configure(state="normal")
        global STOCK_SYMBOL
        self.function_data = ""
        self.results_textbox.delete('1.0', 'end')
        STOCK_SYMBOL = entry.get()
        STOCK_SYMBOL = STOCK_SYMBOL.upper()
        entry.delete(0, 'end')
        self.twelve_data = twelve_data.TwelveData(
            STOCK_SYMBOL, interval=self.interval_value, outputsize=self.output_size_value)
        if (self.result_function == "max diffrence"):
            self.function_data = self.twelve_data.max_diffrence_in_interval()
        interval_string = self.function_data["interval"][:1] + \
            " " + self.function_data["interval"][1:]
        self.results_textbox.insert(
            '1.0', f'Stock symbol is: {STOCK_SYMBOL}\n')
        self.results_textbox.insert(
            '1.0', f'Interval time: {interval_string}\n')
        self.results_textbox.insert(
            '1.0', f'Max diffrence is: {self.function_data["max_difference"]}\n')
        self.results_textbox.insert(
            '1.0', f'Occurred on time: {self.function_data["at_time"]}\n')
        self.results_textbox.configure(state="disabled")

    def textbox_data(self):
        self.stock_indexes_textbox.tag_config("tag_name", justify='center')
        self.stock_indexes_textbox.configure(state="normal")
        data = yahooFinance.YahooScraping(URL_TO_SCRAPE)
        marketsummery = data.get_market_summary()
        if (marketsummery):
            if not (self.data_market):
                self.data_market.clear()
            for market in marketsummery:
                self.data_market.append(
                    f'Data for {market["Data For"]}\nCurrent value is {market["Current value"]}\nPoints are {market["Point"]}({market["Percentage"]})\n\n')
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

    def mainPage(self):
        ###
        # create main frame
        self.grid_columnconfigure((0, 1, 2), weight=1)  # type: ignore
        self.grid_rowconfigure((0, 1, 2), weight=1)  # type: ignore
        self.main_frame = ctk.CTkFrame(
            self,)  # border_color="red", border_width=2
        # configure grid layout (3x3)
        self.main_frame.grid_columnconfigure((0, 2), weight=0)  # type: ignore
        self.main_frame.grid_columnconfigure((1), weight=1)
        self.main_frame.grid_rowconfigure((0, 1, 2), weight=1)  # type: ignore
        self.main_frame.grid(row=0, column=0)
        ###
        # creating first frame
        self.first_frame = ctk.CTkFrame(
            self.main_frame,  width=140, height=self.winfo_screenheight(),)  # border_color="pink", border_width=2
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
            self.first_frame, text="Submit", height=37, width=170, font=ctk.CTkFont('Calibri', 25, 'bold'), command=lambda: self.print_in_results_textbox(entry=self.stockname_entry))
        self.search_for_stock_button.grid(row=2, column=0, padx=20, pady=10)
        self.bind(
            '<Return>', lambda event: self.search_for_stock_button.invoke())
        self.stock_indexes_textbox = ctk.CTkTextbox(
            self.first_frame, font=ctk.CTkFont('Calibri', 20, 'bold'), width=260, height=425, fg_color="transparent")
        self.stock_indexes_textbox.grid(row=3, column=0, padx=(
            15, 15), pady=(30, 0), sticky="nsew")
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
            self.main_frame,  width=(self.winfo_screenwidth() // 5 * 2), height=self.winfo_screenheight(),)  # border_color="blue", border_width=2
        self.second_frame.grid(row=0, column=1, sticky="nsew")
        self.second_frame.grid_columnconfigure(0, weight=1)
        self.second_frame.grid_rowconfigure((0, 1), weight=1)  # type: ignore
        ###
        self.variable_for_stock_frame = ctk.CTkFrame(
            self.second_frame,  width=(self.winfo_screenwidth() // 5 * 2), fg_color="transparent")  # border_color="orange", border_width=2
        self.variable_for_stock_frame.grid(row=0, column=0, sticky="nsew")
        self.variable_for_stock_frame.grid_columnconfigure(
            (0, 1, 2), weight=1)
        self.variable_for_stock_frame.grid_rowconfigure(2, weight=1)
        ###
        self.interval_label = ctk.CTkLabel(
            self.variable_for_stock_frame, text="Interval", font=ctk.CTkFont('Calibri', 25, 'bold'))
        self.interval_label.grid(
            row=0, column=0, padx=10, pady=(20, 10))
        self.interval_value = "5min"
        self.interval_optionmenu = ctk.CTkOptionMenu(self.variable_for_stock_frame, values=["1 min", "5 min", "15 min", "30 min", "45 min ", "1 hour", "2 hours", "4 hours", "1 day", "1 week", "1 month"], font=ctk.CTkFont(
            'Calibri', 20, 'bold'), command=self.get_interval_value_event, anchor='center')
        self.interval_optionmenu.grid(
            row=1, column=0, padx=10, pady=(0, 25))
        ###
        self.output_size_label = ctk.CTkLabel(
            self.variable_for_stock_frame, text="Output Size", font=ctk.CTkFont('Calibri', 25, 'bold'))
        self.output_size_label.grid(
            row=0, column=1, padx=10, pady=(20, 10))
        self.output_size_value = 100
        self.output_size_optionmenu = ctk.CTkOptionMenu(self.variable_for_stock_frame, values=["20", "50", "100", "200", "300", "500", "1000", "2000", "3000", "4000", "5000"], font=ctk.CTkFont(
            'Calibri', 20, 'bold'), command=self.get_output_size_value_event, anchor='center')
        self.output_size_optionmenu.grid(
            row=1, column=1, padx=10, pady=(0, 25))
        ###
        self.result_function_label = ctk.CTkLabel(
            self.variable_for_stock_frame, text="Result Function", font=ctk.CTkFont('Calibri', 25, 'bold'))
        self.result_function_label.grid(
            row=0, column=2, padx=10, pady=(20, 10))
        self.result_function = "max diffrence"
        self.result_function_optionmenu = ctk.CTkOptionMenu(self.variable_for_stock_frame, values=["max diffrence", "min diffrence", "function", "function", "function", "function", "function", "function"], font=ctk.CTkFont(
            'Calibri', 20, 'bold'), command=self.get_result_function_event, anchor='center')
        self.result_function_optionmenu.grid(
            row=1, column=2, padx=10, pady=(0, 25))
        ####
        self.results_textbox = ctk.CTkTextbox(
            self.variable_for_stock_frame, font=ctk.CTkFont('Calibri', 24, 'bold'), corner_radius=20, width=(self.winfo_screenwidth() // 5 * 2), height=440, border_color='#303A48', border_width=20, fg_color="transparent", border_spacing=10)
        self.results_textbox.grid(row=2, column=0, columnspan=3, sticky="nsew")
        self.results_textbox.grid_columnconfigure(
            0, weight=1)  # result of query
        self.results_textbox.grid_rowconfigure(0, weight=1)
        ###
        self.ib_textbox = ctk.CTkTextbox(
            self.second_frame, font=ctk.CTkFont('Calibri', 24, 'bold'), width=(self.winfo_screenwidth() // 5 * 2), fg_color="transparent")  # border_color="purple", border_width=2,
        self.ib_textbox.grid(row=1, column=0, sticky="nsew")
        self.ib_textbox.grid_columnconfigure(
            0, weight=1)  # result of query
        ###
        self.graph_frame = ctk.CTkFrame(
            self.main_frame,  width=int((self.winfo_screenwidth() // 5 * 2.5)), height=self.winfo_screenheight(), )  # border_color="green", border_width=2
        self.graph_frame.grid(row=0, column=2, sticky="nsew")
        self.textbox_data()

    def verify_OTP(self, top1, entry1):
        global OTP
        global MY_OTP
        MY_OTP = entry1.get()
        if (MY_OTP == OTP):
            self.login_frame.grid_forget()
            top1.destroy()  # remove OTP frame
            self.mainPage()
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
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("pookloko57@gmail.com", "cqkeutyeuvrqbyyc")
            s.sendmail('&&&&&&', email_var, message)
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


if __name__ == "__main__":
    app = App()
    app.mainloop()
