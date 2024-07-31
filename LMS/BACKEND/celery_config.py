from dotenv import load_dotenv
load_dotenv()
import os

broker_url = os.getenv('CELERY_BROKER_URL')
result_backend = os.getenv('CELERY_RESULT_BACKEND')
timezone = "Asia/kolkata"
broker_connection_retry_on_startup=True
print('celery_success 1')
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')