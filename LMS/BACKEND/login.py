
from app import app 
from flask import Flask,request,jsonify
import os
from models import User,Role,RolesUsers,db

from tokengen import *
import hashlib
from flask import render_template

@app.route('/drop_table')
def drop():
    db.drop_all()
    db.create_all()
    if(db.session.query(Role).count()==0):
        app.security.datastore.create_role(name="librarian")
        app.security.datastore.create_role(name="user")
        username="lib"
        password="lib"
        fname="LIBRAIAN"
        lname="LIBRARIAN"
        email = os.getenv('SENDER_ADDRESS')
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
    return "Table dropped"


@app.post('/')
def user_login():
    if request.method=="POST":
        data=request.json
        print(data)
        username=data['username'] 
        if not username:
            return jsonify({'message':' username not given'}),400
        password=data['password']
        encoded_password = password.encode('utf-8')
        hashed_password = hashlib.sha256(encoded_password).hexdigest()
        # m=Users.query.filter_by(username=username).first()
        m=db.session.query(User).filter(User.id==username).first()
        r=db.session.query(RolesUsers).filter(RolesUsers.user_id==username).first()
        print(m)
        if m :
            if m.password==hashed_password :
                    # role_users=RolesUsers.query.filter_by(user_id=username).first()
                    toke = m.get_auth_token()
                    roles=db.session.query(Role).filter(Role.id==r.role_id).first()
            else:
                    return jsonify({'message':'Invalid password'}),400
        else:
             return jsonify({'message':'Invalid user'}),404
        return jsonify({'token':toke,'role':roles.name,'username':r.user_id,'mobile':m.mobile_no,'fname':m.fname,'lname':m.lname,'email':m.email}),200
    else:
        return KeyError

@app.get('/')
def index():
    return "heyyy run frontend idiot"

@app.post('/signup')
def signup():
    data = request.json
    username = data['username']
    password = data['password']
    fname = data['fname']
    lname = data['lname']
    email = data['email']
    mobile = data['mobile']
    role = data["roles"]
    is_auth = True
    active = True
    encoded_password = password.encode('utf-8')
    hashed_password = hashlib.sha256(encoded_password).hexdigest()

    # Check if the username already exists
    if User.query.filter_by(id=username).first():
        return jsonify({'message': 'Username already exists'}), 400

    # Check if the email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    # Create the user
    app.security.datastore.create_user(
        id=username,
        fname=fname,
        lname=lname,
        roles=role,
        mobile_no=mobile,
        email=email,
        password=hashed_password,
        authenticated=is_auth
    )
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 200
