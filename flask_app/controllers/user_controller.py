from flask import render_template, request
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


#always use the decorator
#registration page
@app.route("/")
def registration_form():
    return render_template("index.html")

@app.route("/registration")
def registration():
    data ={
        **request.form,
        "password": bcrypt.generate_password_hash("password")
    }