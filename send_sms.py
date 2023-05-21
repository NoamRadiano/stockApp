import os
from twilio.rest import Client
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
STOCK = "TSLA"


class sendSms:

    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, present, newest_articles={}):
        if (newest_articles):
            for key, value in newest_articles.items():
                message = self.client.messages \
                    .create(
                        body=f'{STOCK}: {present}\nTitle: {key}\nDescription: {value["Description"]}',
                        from_=TWILIO_NUMBER,
                        to='+972505754164'
                    )
