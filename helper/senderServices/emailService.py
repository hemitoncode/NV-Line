import psycopg2
import smtplib
from os import getenv 
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ...globalStates import categories_link

load_dotenv()

gmail_email = getenv("GMAIL_SECRET")
gmail_app_password = getenv("GMAIL_APP_PASSWORD")
postgres_connection_string = getenv("POSTGRES_CONNECTION_STRING")

def buildEmailHtml(links_text):
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <title>Weekly Digest</title>
      </head>
      <body style="margin:0; padding:0; background-color:#ffffff; font-family: Arial, sans-serif; color:#111111;">
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td align="center">
              <table width="600" cellpadding="0" cellspacing="0" style="border:1px solid #e5e5e5;">
                
                <!-- Header -->
                <tr>
                  <td style="background-color:#c1121f; color:#ffffff; padding:20px; text-align:center;">
                    <h1 style="margin:0; font-size:24px;">Weekly Digest</h1>
                  </td>
                </tr>

                <!-- Body -->
                <tr>
                  <td style="padding:24px;">
                    <p style="margin-top:0;">Hey!</p>

                    <p>This is your weekly digest:</p>

                    <p style="line-height:1.6;">
                      {links_text}
                    </p>

                    <p style="margin-bottom:0;">
                      Stay informed.
                    </p>
                  </td>
                </tr>

                <!-- Footer -->
                <tr>
                  <td style="background-color:#f8f8f8; padding:12px; text-align:center; font-size:12px; color:#666;">
                    You’re receiving this because you signed up.
                  </td>
                </tr>

              </table>
            </td>
          </tr>
        </table>
      </body>
    </html>
    """
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

        for email, preferred_topics in subscribers:
            links = []
            for topic in preferred_topics: 
                links.append(categories_link[topic])
                
            links_text = "<br>".join(links)

            html_body = buildEmailHtml(links_text)
        

            msg = MIMEMultipart("alternative")
            msg["Subject"] = "NYC Legislation Update - Civic Line"
            msg["From"] = gmail_email
            msg["To"] = email
            msg.attach(MIMEText(html_body, "html"))

            server.sendmail(gmail_email, email, msg.as_string())
            print(f"Sent to {email}")
