import time
from datetime import timedelta
import csv, os
from model_func import exportdetails
from utils import send_message
from celery.schedules import crontab
from celery import shared_task
from models import User, Role
import flask_excel as excel
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from mail_service import send_email
from monthly_report import generate_monthly_report

webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAABN4yDm8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=bdFYUNx6xyL2btWwQDrHKIflDVhQBJ66rSs-vcREwjA'

@shared_task()
def send_welcome_msg(data):
    print(time.time())
    time.sleep(10)
    print(time.time())
    return "Test"

@shared_task(ignore_result=False)
def generate_csv():
    # Simulate some delay
    time.sleep(10)
    
    # Remove existing CSV files in the instance directory
    for file in os.listdir('./instance'):
        if file.endswith(".csv"):
            os.remove(f'./instance/{file}')
    
    # Generate the new CSV file
    with open('./instance/name.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Book Name", "Total Access Count"])
        result = exportdetails()
        
        for row in result:
            book_name, total_access_count = row
            print(f"Book Name: {book_name}, Total Access Count: {total_access_count}")
            writer.writerow([book_name, total_access_count])
    
    # Message content to send
    message = 'CSV sent after generating. Click here to download: http://127.0.0.1:5000/download_csv'
    send_message(webhook_url, message)
    
    return "./instance/name.csv"

@shared_task()
def engagment():
    webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAABN4yDm8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=bdFYUNx6xyL2btWwQDrHKIflDVhQBJ66rSs-vcREwjA'

    message="This is a daily reminder message"
    send_message(webhook_url, message)

@shared_task
def bla():
    return generate_csv()

@shared_task(ignore_result=False)
def create_resource_csv():
    print("inside")
    from app import db  # Check if the import location is correct
    
    stud_res = User.query.all()
    data = [(i.email, i.fname) for i in stud_res]
    print(data)
    csv_output = excel.make_response_from_array(data, "csv", file_name="test.csv")
    print(csv_output)
    print("our")
    return csv_output

def generate_pdf(html_content, pdf_file):
    c = canvas.Canvas(pdf_file, pagesize=letter)
    text = c.beginText(40, 800)
    text.setFont("Helvetica", 12)
    
    for line in html_content.splitlines():
        text.textLine(line)

    c.drawText(text)
    c.save()

@shared_task(ignore_result=True)
def monthly_report():
    subject = 'Monthly report'
    users = User.query.filter(User.roles.any(Role.name == 'user')).all()
    for user in users:
        report_file = generate_monthly_report(user.id)
        print(f"Report generated: {report_file}")
        temp_html = 'report.html'
        pdf_file = 'report.pdf'
        if os.path.exists(pdf_file):
            os.remove(pdf_file)

        with open(temp_html, 'r') as f:
            html_content = f.read()

        generate_pdf(html_content, pdf_file)
        send_email(user.email, subject, message="Monthly report", attachement_file=pdf_file, content="pdf")
    print(users)
    return "OK"
