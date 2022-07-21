from flask import redirect, render_template, request
from flask_app import app
from flask_bcrypt import Bcrypt

from flask_app.models.user_model import User
bcrypt = Bcrypt(app)


#always use the decorator
#registration page
@app.route("/")
def registration_form():
    return render_template("index.html")

@app.route("/registration", methods = ["post"])
def registration():
    if not User.validation(request.form):
        return redirect("/")
    data ={
        **request.form,
        "password": bcrypt.generate_password_hash("password")
    }
    User.add_one(data)
    return redirect("/")
