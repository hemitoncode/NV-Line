import psycopg2
import smtplib
from os import getenv 
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ...globalStates import categories

load_dotenv()

gmail_email = getenv("GMAIL_SECRET")
gmail_app_password = getenv("GMAIL_APP_PASSWORD")
postgres_connection_string = getenv("POSTGRES_CONNECTION_STRING")

def buildEmailHtml(preferred_categories):
    html = """
    <html>
    <body>
        <h1>NYC Legislative Update</h1>
    """

    for category, bills in categories.items():
        if category not in preferred_categories:
            continue

        html += f"<h2>{category}</h2>"
        if not bills:
            html += "<p>No new updates.</p>"
            continue

        for bill in bills:
            sponsors = ", ".join(bill.get("sponsors", []) or [])
            html += f"""
            <div>
                <h3>{bill.get("name", "Unknown")} ({bill.get("fileNumber", "N/A")})</h3>
                <p><b>Summary:</b> {bill.get("summarized", "No summary provided.")}</p>
                <p><b>Sponsors:</b> {sponsors}</p>
            </div>
            <hr>
            """

    html += "</body></html>"
    return html

def fetchEmailSubscribers(): 
    with psycopg2.connect(postgres_connection_string) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    contact,
                    ARRAY(SELECT jsonb_array_elements_text(topics)) AS topics
                FROM subscriptions
                WHERE type_contact = 'email';
            """)
            subscribers = cursor.fetchall()
    
    return subscribers

def sendEmails():
    
    subscribers = fetchEmailSubscribers()

    # Open SMTP connection ONCE through with syntax
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_email, gmail_app_password)

        for email, preferred_categories in subscribers:
            html_body = buildEmailHtml(preferred_categories)

            msg = MIMEMultipart("alternative")
            msg["Subject"] = "NYC Legislation Update - Civic Line"
            msg["From"] = gmail_email
            msg["To"] = email
            msg.attach(MIMEText(html_body, "html"))

            server.sendmail(gmail_email, email, msg.as_string())
            print(f"Sent to {email}")
