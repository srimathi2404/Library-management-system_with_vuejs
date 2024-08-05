
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
        email="bookhive14@gmail.com"
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
        email="srima.r2004@gmail.com"
        mobile=1234567899
        role=["user"]
        is_auth=True
        active=True
        encoded_password = password.encode('utf-8')
        hashed_password = hashlib.sha256(encoded_password).hexdigest()
        app.security.datastore.create_user(id=username,fname=fname, lname=lname,roles=role, mobile_no=mobile, email=email,password=hashed_password, authenticated=is_auth)

        db.session.commit()
     
        # celery_app = celery_init_app(app)




@app.route('/add-to-desktop', methods=['POST'])
def add_to_desktop():
    try:
        data = request.get_json()
        app_name = data['name']
        icon_path = data['icon']
        app_route = data['url']  # This should be the URL of your web application
        
        # Ensure the icon path is absolute
        if not os.path.isabs(icon_path):
            icon_path = os.path.abspath(icon_path)
        
        shortcut_path = f'C:\\Users\\18049\\Desktop\\{app_name}.lnk'
        
        # Log details
        print(f"Creating shortcut with the following details:")
        print(f"App Name: {app_name}")
        print(f"Icon Path: {icon_path}")
        print(f"App Route: {app_route}")
        print(f"Shortcut Path: {shortcut_path}")
        
        # Check if the icon path exists
        if not os.path.exists(icon_path):
            return jsonify({"Error": f"Icon path does not exist: {icon_path}"}), 400
        
        # Create the shortcut for the URL
        make_shortcut(app_route, name=app_name, icon=icon_path, terminal=False, folder='C:\\Users\\18049\\Desktop\\')

        return jsonify({"Message": "Shortcut Created Successfully!"})
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
from login import *



if __name__ == "__main__":
    app.run(debug=True)