from flask import Flask, flash, redirect, render_template, request, send_file , app, url_for
from flask_sqlalchemy import SQLAlchemy
from base64 import b64decode, b64encode  # Import these from base64
from itsdangerous import Serializer
from werkzeug.utils import secure_filename
from io import BytesIO
from datetime import datetime, timedelta  # Import datetime module
from flask_mail import Mail, Message

# Configure Flask-Mail for sending email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'monishkumarpecai@gmail.com'  # Your Gmail email address
app.config['MAIL_PASSWORD'] = ''  # The App Password you generated
app.config['MAIL_DEFAULT_SENDER'] = 'monishkumarpecai@gmail.com' 
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_MAX_EMAILS'] = None  # Optional: Set the maximum number of emails to send
mail = Mail(app)

app = Flask(__name__)
app.secret_key = 'gpalogin' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/gpalogin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
usmail = "monish@gmail.com"

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

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["POST","GET"])
def index():
    return render_template("index.html")


@app.route("/help", methods=["POST","GET"])
def help():
    return render_template("help.html")


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
    return render_template("success.html")

@app.route("/resetsuccess", methods=["POST", "GET"])
def resetsuccess():
    return render_template("resetsuccess.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        dummy = request.form.get("ur_email")
        userImg = Image.query.filter_by(umail=dummy).first()

        if userImg:
            image_data_base64 = b64encode(userImg.data).decode('utf-8')
            return render_template("loginimag.html", imga=userImg, image_data_base64=image_data_base64)
        else:
            # Email not found in the database, display a flash message
            flash("Email not found. Please try again or sign up.")
            return render_template("login.html")

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
            tolerance = 150
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

        if matching_points_count >= 1:
            return render_template("home.html")
        else:
            return render_template("failure.html")


@app.route("/reset_password_form/<token>", methods=["GET", "POST"])
def reset_password_form(token):
    # Add your code for the password reset form here
    return render_template("reset_password_form.html", token=token)


def reset_password_form():
    # Add your code for the password reset form here
    return render_template("reset_password_form.html")

@app.route("/reset_password_request", methods=["POST", "GET"])
def reset_password_request():
    if request.method == 'POST':
        user_email = request.form.get("email")
        
        # Check if the user's email exists in the database
        user = Image.query.filter_by(umail=user_email).first()
        
        if user:
            # Generate a token for password reset
            serializer = Serializer(app.secret_key)  # Adjust the expiration time as needed
            token = serializer.dumps({"email": user_email})
            
            # Create a password reset link
            reset_link = url_for("reset_password_form", token=token, _external=True)
            
            # Send the password reset link to the user's email
            msg = Message("Password Reset Request", sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[user_email])
            msg.body = f"Click the following link to reset your password: {reset_link}"
            mail.send(msg)
            
            # Display a message to the user
            flash("Password reset link has been sent to your email. Please check your inbox.")
        
        else:
            # User email not found
            flash("Email not found. Please try again.")
    
    return render_template("reset_password_request.html")

from itsdangerous import URLSafeSerializer

# Initialize the URLSafeSerializer with a secret key
serializer = URLSafeSerializer(app.secret_key)

@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    
    if request.method == 'POST':
        umail = request.form.get("user_email")
        file = request.files['file']

        if file and allowed_file(file.filename):
            # Find the existing record by email
            userImg = Image.query.filter_by(umail=umail).first()

            if userImg:
                # Update the existing record
                userImg.name = secure_filename(file.filename)
                userImg.mime = file.mimetype
                userImg.data = file.read()
                db.session.commit()

                image_data_base64 = b64encode(userImg.data).decode('utf-8')
                return render_template("resetimg.html", imga=userImg, image_data_base64=image_data_base64)

    return render_template("reset_password_form.html")

def generate_token(email):
    expiration_time = datetime.utcnow() + timedelta(hours=1)
    payload = {
        "email": email,
        "exp": expiration_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    }
    return b64encode(str(payload).encode("utf-8"))

# Verify the token and check for expiration
def verify_token(token):
    try:
        payload = eval(b64decode(token))
        if "exp" in payload and datetime.utcnow() <= datetime.strptime(payload["exp"], "%Y-%m-%d %H:%M:%S.%f"):
            return True
    except:
        pass
    return False


if __name__ == "__main__":
    app.run(debug=True ,port=4444 )

