from collections import UserDict
import os
from django import apps
from flask import Flask, render_template, request, send_file, redirect, url_for
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from io import BytesIO
from base64 import b64encode
import bcrypt
import string


app = Flask(__name__)
app.secret_key = 'sssssrfgvv'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/prototype'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
usmail = "monish@gmail.com"

UPLOAD_FOLDER = os.path.join(app.static_folder, 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class Image(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    mime = db.Column(db.String, nullable=False)
    uname = db.Column(db.String, nullable=False)
    umail = db.Column(db.String, nullable=False)


class UserInfo(db.Model):
    __tablename__ = 'usinfo'
    id = db.Column(db.Integer, primary_key=True)
    umail = db.Column(db.String, nullable=False)
    uspass = db.Column(db.String, nullable=False)

# Define your User model here (replace with actual model definition)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked = db.Column(db.Boolean, default=False)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["POST","GET"])
def index():
    return render_template("index.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == 'POST':
        uname = request.form.get("user_name")
        umail = request.form.get("user_email")
        file = request.files['file']

        if file and allowed_file(file.filename):
            img = Image(
                name=secure_filename(file.filename),
                mime=file.mimetype,
                data=file.read(),
                uname=uname,
                umail=umail
            )
            db.session.add(img)
            db.session.commit()

            userImg = Image.query.filter_by(umail=umail).first()
            image_data_base64 = b64encode(userImg.data).decode('utf-8')
            return render_template("signupimg.html", uname=uname, imga=userImg, image_data_base64=image_data_base64)

    return render_template("signup.html")


@app.route('/download/<int:image_id>')
def download(image_id):
    img = Image.query.get_or_404(image_id)
    return send_file(
        BytesIO(img.data),
        mimetype=img.mime,
        attachment_filename=img.name
    )


@app.route("/success", methods=["POST", "GET"])
def success():
    passinp = request.form.get("xy")
    tolerance = request.form.get("tol")
    user = UserInfo(
        umail=usmail,
        uspass=passinp
    )
    db.session.add(user)
    db.session.commit()
    
    # Pass the success message to the template
    success_message = "Account created successfully"
    
    return render_template("success.html", success_message=success_message)



@app.route("/login", methods=["POST", "GET"])
def login():

    if request.method == 'POST':
        dummy = request.form.get("ur_email")
        usmail = dummy
        userImg = Image.query.filter_by(umail=dummy).first()

        if userImg:
            image_data_base64 = b64encode(userImg.data).decode('utf-8')
            return render_template("loginimag.html", imga=userImg, image_data_base64=image_data_base64)

    return render_template("login.html")


@app.route("/home", methods=["POST", "GET"])
def authenticate():
    if request.method == 'POST':
        tolerance = request.form.get("tolerance")
        reqUser = UserInfo.query.filter_by(umail=usmail).first()

        passdata = reqUser.uspass
        stored_coordinates = [int(coord) for coord in passdata.split()]
        print("Stored coordinates:", stored_coordinates)

        loginuser = request.form.get("passxy")
        clicked_coordinates = [int(coord) for coord in loginuser.split()]
        print("Clicked coordinates:", clicked_coordinates)

        if tolerance is None:
            tolerance = 30
        print("Tolerance:", tolerance)

        matching_points_count = 0

        for i in range(0, len(stored_coordinates), 2):
            stored_x  = int(stored_coordinates[i])
            stored_y  = int(stored_coordinates[i + 1])

            clicked_x = int(clicked_coordinates[i])
            clicked_y = int(clicked_coordinates[i + 1])

            x_diff = abs(stored_x - clicked_x)
            y_diff = abs(stored_y - clicked_y)

            if x_diff <= tolerance and y_diff <= tolerance:
                matching_points_count += 1

        print("Matching points count:", matching_points_count)

        if matching_points_count >= 2:
            return render_template("home.html")
        else:
            return render_template("failure.html")


# Extend string.punctuation with a space
string.punctuation = string.punctuation + " "

MAX_FAILED_LOGIN_ATTEMPTS = 5

def validate_password(password):
    length_requirement = 8
    complexity_requirement = 3

    if len(password) < length_requirement:
        return False

    if not any(c.islower() for c in password):
        return False

    if not any(c.isupper() for c in password):
        return False

    if not any(c.isdigit() for c in password):
        return False

    if not any(c in string.punctuation for c in password):
        return False

    return True

def lockout_account(user_id):
    user = User.query.get(user_id)
    if user:
        user.failed_login_attempts += 1
        # Assuming you have a method like update_timestamps for user updates
        user.update_timestamps()
        db.session.commit()

        if user.failed_login_attempts >= MAX_FAILED_LOGIN_ATTEMPTS:
            user.locked = True
            # Assuming you have a method like update_timestamps for user updates
            user.update_timestamps()
            db.session.commit()




if __name__ == "__main__":
    app.run(debug=True)
