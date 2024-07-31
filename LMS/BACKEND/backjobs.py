from celery import Celery
from celery.schedules import crontab
import celery_config

from model_func import exportdetails
from app import app
from monthly_report import generate_monthly_report

with app.app_context():
    print(exportdetails())

app = Celery('backjobs')
app.conf.update(
    broker_url=celery_config.CELERY_BROKER_URL,
    result_backend=celery_config.CELERY_RESULT_BACKEND
)

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'backjobs.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
    'send-monthly-report': {
        'task': 'backjobs.monthly_report',
        'schedule': crontab(hour=23, minute=51, day_of_month=19)
    },
    'send-daily-reminder': {
        'task': 'backjobs.engagment1',
        'schedule': crontab(hour=18, minute=14),
        'args': ("This is a daily reminder message", "sad")
    },
    'send-every-60-seconds': {
        'task': 'backjobs.engagment1',
        'schedule': 60.0,
        'args': ("This is a 60 second reminder message", "das")
    }
}

app.conf.timezone = "Asia/Kolkata"
app.conf.broker_connection_retry_on_startup = True

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30.0, test.s('world'), expires=10)
    sender.add_periodic_task(
        crontab(hour=17, minute=30, day_of_week=0),
        test.s('Happy Mondays!'),
    )

@app.task
def test(arg):
    print(arg)

@app.task
def add(x, y):
    z = x + y
    print(z)

@app.task
def monthly_report():
    from models import User, Role
    from weasyprint import HTML
    from mail_service import send_email
    subject = 'Monthly report'
    users = User.query.filter(User.roles.any(Role.name == 'user')).all()
    for user in users:
        report_file = generate_monthly_report(user.id)
        print(f"Report generated: {report_file}")
        temp_html = f'report.html'
        pdf_file = 'report.pdf'
        HTML(temp_html).write_pdf(pdf_file)
        send_email(user.email, subject, message="Monthly report", attachment_file='report.pdf', content="pdf")
    print(users)
    return "OK"

@app.task
def engagment1(message, data):
    from utils import send_message
    webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAABN4yDm8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=bdFYUNx6xyL2btWwQDrHKIflDVhQBJ66rSs-vcREwjA'
    send_message(webhook_url, message)




