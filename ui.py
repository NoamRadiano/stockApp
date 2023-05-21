import customtkinter as ctk
import os
from dotenv import load_dotenv
from pathlib import Path
from tkinter import messagebox
import math
import random
import smtplib

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
PASS1 = os.getenv('PASS1')
PASS2 = os.getenv('PASS2')
USER1 = os.getenv('USER1')
USER2 = os.getenv('USER2')
EMAIL1 = os.getenv('EMAIL1')
EMAIL2 = os.getenv('EMAIL2')
OTP = ""
MY_OTP = ""


class App(ctk.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(fg_color="#4E4E4E")
        self.title("StockApp")
        self.geometry(
            f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")

        # create login frame
        login_height = self.winfo_screenheight() - 200
        login_width = self.winfo_screenwidth() - 200
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.login_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent", height=login_height, width=login_width)
        self.login_frame.grid(row=0, column=0, sticky="sew")
        self.login_frame.grid_rowconfigure(
            0, weight=1)  # Make row 0 expandable
        self.login_frame.grid_columnconfigure(
            0, weight=1)  # Make column 0 expandable
        self.login_label = ctk.CTkLabel(self.login_frame, text="Login",
                                        font=('Calibri', 46, 'bold'))
        self.login_label.grid(row=0, column=0, padx=30,
                              pady=(40, 17))
        self.login_label.grid_columnconfigure(0, weight=1)
        self.login_label.grid_rowconfigure(0, weight=1)
        self.username_entry = ctk.CTkEntry(
            self.login_frame, width=300, height=46, placeholder_text="Username", font=('Calibri', 24, 'bold'))
        self.username_entry.grid(
            row=1, column=0, padx=30, pady=(15, 0))
        self.username_entry.grid_rowconfigure(1, weight=1)
        self.password_entry = ctk.CTkEntry(
            self.login_frame, width=300, height=46, show="*", placeholder_text="Password", font=('Calibri', 24, 'bold'))
        self.password_entry.grid(
            row=2, column=0, padx=30, pady=(15, 15))
        self.password_entry.grid_rowconfigure(2, weight=1)
        self.login_button = ctk.CTkButton(
            self.login_frame, text="Submit", height=46, command=self.login_event, width=300, font=('Calibri', 34, 'bold'), anchor='center')
        self.login_button.grid(row=3, column=0,
                               pady=(15, 15), padx=30)
        self.login_button.grid_rowconfigure(3, weight=1)
        # create main frame
        self.main_frame = ctk.CTkFrame(
            self, corner_radius=0, width=1300, height=800)
        # configure grid layout (3x3)
        self.main_label = ctk.CTkLabel(self.main_frame, text="Main Page",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.main_label.grid(row=0, column=0, padx=30, pady=(30, 15))
        self.main_label.grid_columnconfigure((1, 2), weight=1)
        self.main_label.grid_rowconfigure((1, 2), weight=1)

    def error_message_for_details(self):
        messagebox.showwarning(
            "Invalid input", "Your password or username is incorrect.\nPlease try again.")

    def error_message_for_OTP(self, top1):
        messagebox.showwarning(
            "Invalid input", "Your OTP key is incorrect.\nPlease try again.", parent=top1)

    def error_message_for_email(self, top):
        messagebox.showwarning(
            "Invalid input", "Your email is not exist.\nPlease try again.", parent=top)

    def verify_OTP(self, top1, entry1):
        global OTP
        global MY_OTP
        MY_OTP = entry1.get()
        if (MY_OTP == OTP):
            self.login_frame.grid_forget()
            top1.destroy()  # remove OTP frame
            self.main_frame.grid(row=2, column=2, sticky="nsew",
                                 padx=100)  # show main frame
            self.grid_columnconfigure((1, 2), weight=1)
            self.grid_rowconfigure((0, 1, 2), weight=1)
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
            top1 = ctk.CTkToplevel(self, fg_color="#4E4E4E")
            top1.title("Verify")
            top1.grid_rowconfigure((0, 1, 2, 3), weight=1)
            top1.grid_columnconfigure(0, weight=1)
            top1.geometry("350x300")
            top1.resizable(False, False)
            # place in center window
            self.eval(f'tk::PlaceWindow {str(top1)} center')
            otp_label = ctk.CTkLabel(top1, text=text,
                                     font=('Calibri', 30, 'bold'), width=300, height=26)
            otp_label.grid(row=0, column=0, padx=20, pady=(7, 7))
            otp_label.grid_rowconfigure(0, weight=1)
            entry1 = ctk.CTkEntry(
                top1, placeholder_text=placeholder_text, width=300, height=46, font=('Calibri', 24, 'bold'))
            entry1.grid(row=1, column=0, padx=20, pady=(7, 7))
            entry1.grid_rowconfigure(1, weight=1)
            send_otp_button = ctk.CTkButton(
                top1, text="Verify", height=46, command=lambda: self.verify_OTP(top1, entry1), width=300, font=('Calibri', 25, 'bold'), anchor='center')
            send_otp_button.grid(row=2, column=0, padx=20, pady=(7, 7))
            send_otp_button.grid_rowconfigure(2, weight=1)

        else:
            entry.delete(0, 'end')
            self.error_message_for_email(top)

    def verify_window_for_email(self, text, placeholder_text):
        top = ctk.CTkToplevel(self, fg_color="#4E4E4E")
        top.title("Verify")
        top.grid_rowconfigure((0, 1, 2, 3), weight=1)
        top.grid_columnconfigure(0, weight=1)
        top.geometry("350x300")
        top.resizable(False, False)
        # place in center window
        self.eval(f'tk::PlaceWindow {str(top)} center')
        email_label = ctk.CTkLabel(top, text=text,
                                   font=('Calibri', 30, 'bold'), width=300, height=26)
        email_label.grid(row=0, column=0, padx=20, pady=(7, 7))
        email_label.grid_rowconfigure(0, weight=1)
        entry = ctk.CTkEntry(
            top, placeholder_text=placeholder_text, width=300, height=46, font=('Calibri', 24, 'bold'))
        entry.grid(row=1, column=0, padx=20, pady=(7, 7))
        entry.grid_rowconfigure(1, weight=1)
        send_mail_button = ctk.CTkButton(
            top, text="Send code", height=46, command=lambda: self.verify_window_for_OTP(entry, top, text="Enter your OTP code", placeholder_text="OTP code"), width=300, font=('Calibri', 25, 'bold'), anchor='center')
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
