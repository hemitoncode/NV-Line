from twilio.rest import Client 
from dotenv import load_dotenv
from os import getenv 

load_dotenv()

account_sid = getenv("TWILIO_ACCOUNT_SID")
auth_token = getenv("TWILIO_AUTH_TOKEN")

client = Client(account_sid, auth_token)