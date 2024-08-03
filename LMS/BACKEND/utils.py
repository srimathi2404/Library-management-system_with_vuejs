import requests
import json

def send_message(webhook_url, message):
    headers = {
        'Content-Type': 'application/json; charset=UTF-8'
    }

    payload = {
        'text': message
    }

    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            print("Message sent successfully")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error sending message : {str(e)}")


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()
def send_notification(message):
    from_address = os.getenv('SENDER_ADDRESS')
    to_address = os.getenv('SENDER_ADDRESS')
    password = os.getenv('SENDER_PASSWORD')
    
    if not from_address or not to_address or not password:
        raise ValueError("Email address or password not set in environment variables")
    
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "E-Book Access Export Completed"
    
    msg.attach(MIMEText(message, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_address, password)
    text = msg.as_string()
    server.sendmail(from_address, to_address, text)
    server.quit()
