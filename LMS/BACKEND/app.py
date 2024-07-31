
from celery.result import AsyncResult
import os
import hashlib
import random
from flask import Flask, render_template,request, make_response, jsonify, send_file
from flask_security import SQLAlchemySessionUserDatastore, Security, login_user, logout_user
from flask_security import current_user, auth_required, login_required, roles_required, roles_accepted,hash_password,verify_password
from flask_cors import CORS
from pyshortcuts import make_shortcut
from models import *
from api import *
from config import Config
import time
from Cache import cache
from flask import send_file
# from flask_mail import Mail
from worker import celery_init_app
from tasks import  engagment
from mail_service import send_email as smail
from tasks import create_resource_csv, monthly_report
app = Flask(__name__,static_folder='../FRONTEND/static',
    template_folder='../FRONTEND/templates'
)
api.init_app(app)
app.config.from_object(Config)
CORS(app)
app.config['CACHE_TYPE'] = 'simple'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./dev.db"

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", 
                                          "hbivnfdisbvljobfgjoihfhrugubdfsbery89w34yt5898he")
app.config["SECURITY_PASSWORD_SALT"] = os.environ.get("SECURITY_PASSWORD_SALT",
                                                       "hbivnfdisbvljobfgjoihfhrugubdfsbery89w34yt5898he")

# authenticatin paramter for url
app.config["`SECURITY_TOKEN_AUTHENTICATION_KEY`"] = "auth_key" # Default: auth_token
# in postman add the key as auth_key and value as the token , this should be in the url
app.config["SECURITY_TOKEN_AUTHENTICATION_HEADER"] = "Authentication-Token" # Default: Authentication-Token"
# in postman add the key as Authentication-Token and value as the token
# app.config[]

db.init_app(app)

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role) # Not SQLAlchemyUserDatastore
app.security = Security(app, user_datastore)
def celery_func():
    # cache.init_app(app)
    from workers import ContextTask, celery
    celery1 = celery
    celery1.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"]
    )
    celery1.Task = ContextTask
    # Setting Flask Security Setup
    cache.init_app(app)
    app.app_context().push()

    return celery1


celery = celery_func()
celery_app = celery_init_app(app)

with app.app_context():

    db.create_all()

    if(db.session.query(Role).count()==0):
        app.security.datastore.create_role(name="librarian")
        app.security.datastore.create_role(name="user")
        username="lib"
        password="lib"
        fname="LIBRAIAN"
        lname="LIBRARIAN"
        email="lib@gmail.com"
        mobile=1234567890
        role=["librarian"]
        is_auth=True
        active=True
        encoded_password = password.encode('utf-8')
        hashed_password = hashlib.sha256(encoded_password).hexdigest()
        app.security.datastore.create_user(id=username,fname=fname, lname=lname,roles=role, mobile_no=mobile, email=email,password=hashed_password, authenticated=is_auth)

        db.session.commit()
        username="sri"
        password="sri"
        fname="sri"
        lname="sri"
        email="sri@gmail.com"
        mobile=1234567899
        role=["user"]
        is_auth=True
        active=True
        encoded_password = password.encode('utf-8')
        hashed_password = hashlib.sha256(encoded_password).hexdigest()
        app.security.datastore.create_user(id=username,fname=fname, lname=lname,roles=role, mobile_no=mobile, email=email,password=hashed_password, authenticated=is_auth)

        db.session.commit()
     
        # celery_app = celery_init_app(app)


@app.route('/download_csv')
def download_csv():
    return send_file(f'./instance/name.csv', as_attachment=True)


@app.get("/cached-data")
@cache.cached(timeout=50)
def cached_data():
    time.sleep(10)
    print("printing cached data")
    return {"cached_data": "sds"}

@app.route('/gen_csv')
def gen_csv():
    from tasks import bla
    task=bla.delay()
    return jsonify({"task-id": task.id})

@app.route('/task')
def taskgy():

    task=monthly_report.delay()
    return jsonify({"task-id": task.id})

@app.get('/get_csv/<task_id>')
def get_csv(task_id):
    res = AsyncResult(task_id)
    print(res)
    if res.ready():
        filename = res.result
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({"message": "Task Pending"}), 404
 

from celery.schedules import crontab
@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=19, minute=55, day_of_month=20),
        engagment.s(),
    )

@app.post('/add-to-desktop')
def add_to_desktop():
    data=request.get_json()
    app_name = data['name']
    icon_path = data['icon']
    app_route = data['url']

    shortcut_path= f'/Users/shriprasad/Desktop/{app_name}'
    # Creating the desktop shortcut
    make_shortcut(app_name,shortcut_path,icon=icon_path, terminal=False)

    return {"Message":"Shortcut Created Successfully!"}

from login import *

if __name__ == "__main__":
    app.run(debug=True)