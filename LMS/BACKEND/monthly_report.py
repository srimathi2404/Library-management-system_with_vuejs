from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfgen import canvas
import os
import time

def generate_monthly_report(user_data, file_path):
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    elements = []

    # Draw a fancy quote at the top
    quote = "“A room without books is like a body without a soul.” – Cicero"
    styles = getSampleStyleSheet()
    quote_paragraph = Paragraph(quote, styles["Normal"])
    elements.append(quote_paragraph)
    elements.append(Spacer(1, 12))

    # Draw a heading
    heading = "MONTHLY REPORT FROM BOOK HIVE"
    heading_paragraph = Paragraph(heading, styles["Title"])
    elements.append(heading_paragraph)
    elements.append(Spacer(1, 24))

    # Draw the user information box
    user_info = f"Monthly Report for {user_data['username']}<br/>Email: {user_data['email']}"
    user_info_paragraph = Paragraph(user_info, styles["Normal"])
    elements.append(user_info_paragraph)
    elements.append(Spacer(1, 24))

    # Draw the book information in a table
    data = [['Book', 'Author', 'Issue Date', 'Return Date']]
    for book in user_data['books']:
        data.append([book['book_name'], book['author'], book['issue_date'], book['return_date']])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    doc.build(elements)






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

