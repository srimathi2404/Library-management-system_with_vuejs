from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
def generate_monthly_report(user_data, file_path):
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    
    c.drawString(100, height - 40, f"Monthly Report for {user_data['username']}")
    c.drawString(100, height - 60, f"Email: {user_data['email']}")
    
    y = height - 100
    for book in user_data['books']:
        c.drawString(100, y, f"Book: {book['book_name']} by {book['author']}")
        c.drawString(100, y - 20, f"Issue Date: {book['issue_date']}")
        c.drawString(100, y - 40, f"Return Date: {book['return_date']}")
        y -= 60
        if y < 40:
            c.showPage()
            y = height - 40

    c.save()

def send_email(to_address, subject, body, attachment_path):
    from_address = os.getenv('SENDER_ADDRESS')
    password = os.getenv('SENDER_PASSWORD')
    
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach the PDF
    attachment = open(attachment_path, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {attachment_path}")
    msg.attach(part)
    
    # Send the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_address, password)
    text = msg.as_string()
    server.sendmail(from_address, to_address, text)
    server.quit()

