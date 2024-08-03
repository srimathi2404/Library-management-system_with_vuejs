from celery import Celery
from celery.schedules import crontab
import celery_config
import os
from model_func import exportdetails, get_returned_books_today,get_other_books,get_monthly_report_data,remove_expired_book_access
from app import app
from monthly_report import generate_monthly_report, send_email
import requests
with app.app_context():
    reminders = get_returned_books_today()
    print(reminders)
    reminders1=get_other_books()
    print(reminders1)
    monthy=get_monthly_report_data()
    print(monthy)
    exp_dict=remove_expired_book_access()
    print(exp_dict)

# Initialize Celery
app = Celery('backjobs')
app.conf.update(
    broker_url=celery_config.CELERY_BROKER_URL,
    result_backend=celery_config.CELERY_RESULT_BACKEND
)

# Serialize the dictionary to a JSON string for the periodic task
import json
reminders_json = json.dumps(reminders)
reminder1_json=json.dumps(reminders1)
monthy_json=json.dumps(monthy)
exp_json=json.dumps(exp_dict)
app.conf.beat_schedule = {
    'send-monthly-report': {
        'task': 'backjobs.monthly_report_task',
        'schedule': crontab(hour=19, minute=24, day_of_month=3),
        'args': (monthy_json,)
    },
    'send-daily-reminder': {
        'task': 'backjobs.engagment1',
        'schedule': crontab(hour=18, minute=3),
        'args': (reminders_json,)
    },
    'send-daily1-reminder': {
        'task': 'backjobs.engagment2',
        'schedule': crontab(hour=18, minute=3),
        'args': (reminder1_json,)
    },

    'remove-expired-book-access': {
            'task': 'backjobs.remove_expired_book_access_task',
            'schedule': crontab(hour=20, minute=26), 
             'args':(exp_json,) # Run daily at midnight
        },

    'trigger-export': {
            'task': 'backjobs.trigger_export_task',
            'schedule': crontab(hour=23, minute=31),  # Run daily at midnight
        },
    # 'send-every-60-seconds': {
    #     'task': 'backjobs.engagment1',
    #     'schedule': 60.0,
    #     'args': (reminders_json,)
    # }
}

app.conf.timezone = "Asia/Kolkata"
app.conf.broker_connection_retry_on_startup = True

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(30.0, test.s('world'), expires=10)
#     sender.add_periodic_task(
#         crontab(hour=17, minute=30, day_of_week=0),
#         test.s('Happy Mondays!'),
#     )

@app.task
def test(arg):
    print(arg)

@app.task
def add(x, y):
    z = x + y
    print(z)
@app.task
def monthly_report_task(month_json):
    report_data = json.loads(month_json)
    
    report_directory = os.path.join("C:\\Users\\18049\\Desktop", 'reports')
    if not os.path.exists(report_directory):
        os.makedirs(report_directory)

    for user_id, user_data in report_data.items():
        pdf_path = os.path.join(report_directory, f"monthly_report_{user_id}.pdf")
        generate_monthly_report(user_data, pdf_path)
        
        subject = "Your Monthly Report"
        body = f"Dear {user_data['username']},\n\nPlease find attached your monthly report."
        send_email(user_data['email'], subject, body, pdf_path)
        
        # Ensure the file is closed before attempting to delete it
        try:
            os.remove(pdf_path)
        except PermissionError:
            # If the file is still in use, wait a moment and try again
            import time
            time.sleep(1)
            os.remove(pdf_path)
@app.task
def engagment1(data):
    print(data)
    from utils import send_message
    import json
    webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAABN4yDm8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=bdFYUNx6xyL2btWwQDrHKIflDVhQBJ66rSs-vcREwjA'
    
    # Deserialize the JSON string back to a dictionary
    data_dict = json.loads(data)

    # Format the dictionary into a multiline string
    reminder_lines = ["BOOKS NEED TO BE RETURNED TODAY"]
    for user_id, book_ids in data_dict.items():
        book_ids_str = ", ".join(str(book_id) for book_id in book_ids)
        reminder_lines.append(f"User {user_id}: Books {book_ids_str}")
    reminder_message = "\n".join(reminder_lines)
    
    send_message(webhook_url, reminder_message)


@app.task
def engagment2(data):
    print(data)
    from utils import send_message
    import json

    webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAABN4yDm8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=bdFYUNx6xyL2btWwQDrHKIflDVhQBJ66rSs-vcREwjA'
    
    # Deserialize the JSON string back to a dictionary
    data_dict = json.loads(data)

    # Format the dictionary into a multiline string
    reminder_lines = ["OTHER BOOKS WHICH NEED TO RETURNED IN THE UPCOMING DAYS"]
    for user_id, books in data_dict.items():
        book_entries = []
        for book_name, return_date in books:
            book_entries.append(f'"{book_name}" needed to be returned on "{return_date}"')
        books_str = "; ".join(book_entries)
        reminder_lines.append(f'USERNAME "{user_id}": {books_str}')
    reminder_message = "\n".join(reminder_lines)
    
    send_message(webhook_url, reminder_message)

@app.task
def remove_expired_book_access_task(expired_json):
    expired_book_accesses = json.loads(expired_json)
    
    # Assuming your API endpoint is hosted locally on port 5000
    api_url = "http://127.0.0.1:5000/api/bookaccess"
    
    for access in expired_book_accesses:
        response = requests.delete(api_url, json={'user_id': access['user_id'], 'book_id': access['book_id']})
        if response.status_code == 200:
            print(f"Deleted book access for user {access['user_id']} and book {access['book_id']}")
        else:
            print(f"Failed to delete book access for user {access['user_id']} and book {access['book_id']}")


@app.task
def trigger_export_task():
    # Assuming your API endpoint is hosted locally on port 5000
    api_url = "http://127.0.0.1:5000/api/trigger_export"
    
    response = requests.post(api_url)
    if response.status_code == 200:
        print("Export task completed successfully.")
    else:
        print("Failed to complete the export task.")