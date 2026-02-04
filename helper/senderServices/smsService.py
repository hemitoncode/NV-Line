from twilio.rest import Client 
from dotenv import load_dotenv
from os import getenv 
from ...globalStates import categories, categories_link
import psycopg2

load_dotenv()

account_sid = getenv("TWILIO_ACCOUNT_SID")
auth_token = getenv("TWILIO_AUTH_TOKEN")
postgres_connection_string = getenv("POSTGRES_CONNECTION_STRING")

client = Client(account_sid, auth_token)

def buildSmsMsg(preferred_categories):
    messages = []

    for category, bills in categories.items():
        if category not in preferred_categories:
            continue

        for bill in bills:
            name = bill.get("name", "Unknown")
            file_num = bill.get("fileNumber", "N/A")
            sponsors_list = bill.get("sponsors", []) or []
            sponsors = ", ".join(sponsors_list) if sponsors_list else "N/A"
            summary = bill.get("summarized", "No summary provided.")

            parts = []
            parts.append(category)

            parts += [
                f"{name} ({file_num})",
                f"Summary: {summary}",
                f"Sponsors: {sponsors}",
            ]

            messages.append("\n".join(parts).strip())

    return messages

def fetchSmsSubscribers(): 
    with psycopg2.connect(postgres_connection_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    contact,
                    ARRAY(SELECT jsonb_array_elements_text(topics)) AS topics
                FROM subscriptions
                WHERE type_contact = 'sms';
            """)
            subscribers = cursor.fetchall()
    return subscribers

def sendSms():
    subscribers = fetchSmsSubscribers()

    for number, preferred_topics in subscribers:
        link = []
        for topic in preferred_topics: 
            link = categories_link[topic]
        
        client.