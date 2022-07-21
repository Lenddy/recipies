from flask import flash
from flask_app.config.connect_tosql import connectToMySQL
from flask_app import db
import re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
password_regex =re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')




class User:
    def __init__(self,data):
        self.id = data["id"]
        self.f_name = data["f_name"]
        self.l_name = data["l_name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def add_one(cls,data):
        query = "insert into users (f_name,l_name,email,password) values(%(f_ name)s,%(l_name)s,%(email)s,%(password)s);"
        result = connectToMySQL(db).query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query = "select * from users;"
        result = connectToMySQL(db).query_db(query)
        return cls(result[0])

    @classmethod
    def get_email(cls,data):
        query = "select* from users where email = %(email)s;"
        result = connectToMySQL(db).query_db(query,data)
        return cls(result[0])

    @staticmethod
    def validation(user):
        is_valid = True
        #for name
        if len(user['f_name']) == 0:
            flash("you must input a name","name")
            is_valid = False
        elif len(user['f_name']) < 2:
            flash("Your name must be at least 2 character long","name")
            is_valid = False
        #for last name
        if len(user['l_name']) == 0:
            flash("you must input a name","l_name")
            is_valid = False
        elif len(user['l_name']) < 2:
            flash("Your name must be at least 2 character long","l_name")
            is_valid = False
        #for email
        if len(user['email']) == 0 :
            flash('you must enter a email','email')
            is_valid = False
        elif not re.match(email_regex):
            flash("email does not follow the right format","email")
            is_valid = False
        elif User.get_email({"email":user['email']}):
            flash("email is already in use",'email')
            is_valid = False
        #for password
        if len(user['password']) == 0:
            flash("a password must be enter","password")
            is_valid = False
        elif not re.match(password_regex):
            flash("password must be minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character","password")
        if len(user["password"]) < 8:
            flash("your password must be at least 8 character long")
            is_valid = False
        if user["confirm_password"] != user["password"]:
            flash("password does not mach","confirm")