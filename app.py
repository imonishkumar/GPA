from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from base64 import b64encode
from werkzeug.utils import secure_filename
from io import BytesIO

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

        if matching_points_count >= 3:
            return render_template("home.html")
        else:
            return render_template("failure.html")

if __name__ == "__main__":
    app.run(debug=True ,port=5555 )

