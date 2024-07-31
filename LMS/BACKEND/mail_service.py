
from email import encoders
from email.mime.base import MIMEBase
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv
load_dotenv()
import os
sender=os.getenv("SENDER_ADDRESS")
sender_password=os.getenv("SENDER_PASSWORD")


def send_email(to_address, subject, message,content='text',attachement_file=None):

    SMPTP_SERVER_HOST = 'smtp.gmail.com'
    SMPTP_SERVER_PORT = 587
    #recepient=sender
    SENDER_ADDRESS = sender
    SENDER_PASSWORD = sender_password
    print("calling send email")
    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To']=to_address
    msg['Subject'] = subject
    
    if content == 'html':
        msg.attach(MIMEText(message,'html'))
        
    else:
        msg.attach(MIMEText(message,'plain'))
        print("inside else")
    
    if attachement_file:
        with open(attachement_file,'rb') as attachment:
            part = MIMEBase('application','octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition', f'attachment; filename={attachement_file}',
        )
        msg.attach(part)
    try:
        print("inside try")
        s = smtplib.SMTP(host=SMPTP_SERVER_HOST,port=SMPTP_SERVER_PORT)
        s.starttls()
        s.login(SENDER_ADDRESS,SENDER_PASSWORD)
        s.send_message(msg)
        s.quit()
        print("isntide mail sent")
        return True
    except Exception as e:
        print("inside except")
        print(e)
        return False
    
