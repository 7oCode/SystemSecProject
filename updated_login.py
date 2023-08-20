from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_bcrypt import Bcrypt
import re
from cryptography.fernet import Fernet
from SQL_Functions import *
from forms import *

from flask import *
from flask_mail import Mail, Message
from random import *
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests


from flask_wtf import FlaskForm, RecaptchaField

from twilio.rest import Client
from datetime import timedelta
import logging

from google_auth_oauthlib.flow import Flow, InstalledAppFlow
import google.auth.transport.requests

import os
import pathlib
import requests

app = Flask(__name__)
bcrypt = Bcrypt()

# Initialize the logging module
logging.basicConfig(filename='audit.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

app.config['RECAPTCHA_PUBLIC_KEY'] = '6Ld_BVEnAAAAAJWCzb859ZSVXSMN7vxwVOgNkDEk'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Ld_BVEnAAAAAEqVkudxjudXLE0WfM0QfBrlX_1V'

s = URLSafeTimedSerializer('Thisisasecret!')

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'very secret'

# Set session to expire after 0.5 minutes of inactivity
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=0.5)

# Enter database connection details
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_DB'] = 'sys_sec'

app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'mohd.irfan.khan.9383@gmail.com'
app.config['MAIL_PASSWORD'] = 'afxjkjngfitkekzs'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Initialize MySQL
mysql = MySQL(app)
mail = Mail(app)


#Start of google oauth

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "887500220265-7jfh5ag7k8n3mlv37a9j0j8io817rbqo.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper
#End


def password_check(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) >= 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\]^`{|}~"+r'"]', password) is None

    # overall result
    # MUST CONTAIN SPECIAL CHARACTER
    password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)
    passClear = re.search(r"""^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]+$""", password) is not None
    # return {
    #     'password_ok': password_ok,
    #     'length_error': length_error,
    #     'digit_error': digit_error,
    #     'uppercase_error': uppercase_error,
    #     'lowercase_error': lowercase_error,
    #     'symbol_error': symbol_error,
    # }
    return {
        'password_ok': passClear
    }


@app.route('/', methods=['GET', 'POST'])
def homepage():
    return redirect(url_for('login'))

@app.route('/fail', methods=['GET', 'POST'])
def failpage():
    return render_template('stop.html')


def log_audit_action(action, details):
    """Function to log audit actions to the audit.log file."""
    log_msg = f"Action: {action} - Details: {details}"
    logging.info(log_msg)


@app.route('/WebApp', methods=['GET', 'POST'])
def login():
    msg = ''
    login = LoginForm()
    if login.validate_on_submit():
        username = login.username.data
        password = login.password.data

        # Validate the password using password_check()
        password_validation = password_check(password)
#  and password_validation['password_ok']
        if SQL_Login(username, password) == 0:
            # Generate OTP and store it in the session
            # otp = str(randint(100000, 999999))
            # session['otp'] = otp
            #
            # # Get user's phone number from the database
            # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            # user = cursor.fetchone()
            # phone_number = user['phone_no']
            #
            # # Send OTP via SMS
            # account_sid = 'ACa1c4471cfc07d62502d48bd509232754'
            # auth_token = 'a49afdd6460799e837ab9a3c237b30bb'
            # client = Client(account_sid, auth_token)
            #
            # message = client.messages.create(
            #     body=f"Your OTP is {otp}",
            #     from_='+15738594156',
            #     to=phone_number
            # )
            #
            # return redirect(url_for('verify_otp'))

            # Audit logging for successful logins
            log_audit_action("Successful login", f"User: {username}")

            return redirect(url_for('home'))
        elif SQL_Login(username, password) == 1:
            a = SQL_rate_limit_def()
            if a == 1:
                msg = 'Incorrect Username/Password1'
                print(f"{username}, {password}")
            elif a == 2:
                return redirect(url_for('failpage'))
        elif SQL_Login(username, password) == 2:
            u = SQL_rate_limit_user(username)
            if u == 1:
                msg = 'Incorrect Username/Password(u)'
                print(f"{username}, {password}")
            elif u == 2:
                msg = 'Account has been locked'

    # elif request.method == 'POST':
    #     msg = 'Incorrect Username/Password2'
    #     print(f"{login.username.data} {login.password.data}")

    #         if SQL_rate_limit(username) == 1:
    #             msg = 'Incorrect Username/Password'
    #             # Pass the password validation results to the template
    #             return render_template('index.html', msg=msg, form=login, password_validation=password_validation)
    #         elif SQL_rate_limit(username) == 2:
    #             msg = 'Account has been locked'
    #             return render_template('index.html', msg=msg, form=login, password_validation=password_validation)
    # elif request.method == 'POST':
    #     msg = 'Typo'

    return render_template('index.html', msg=msg, form=login)


@app.route('/forget_password', methods=['GET', 'POST'])
def forget():
    msg = ''
    forgetForm = forgetPassword()
    if forgetForm.validate_on_submit():
        email = forgetForm.email.data
        if SQL_Check_Email(email) == 0:
            msg = 'Email sent to user'
            # link = url_for('confirm_email1', token=token, _external=True)

        elif SQL_Check_Email(email) == 1:
            msg = 'Error'
    # if request.method == 'POST':
    #     email = request.form['email']
    #
    #     # Check if the email exists in the SQL database
    #     if SQL_Check_Email(email):
    #         # Generate a time-limited token for email verification
    #         token = s.dumps(email, salt='email-confirm')
    #
    #         # Create a message with the verification link and send it via email
    #         v_msg = Message('Confirm Email', sender='mohd.irfan.khan.9383@gmail.com', recipients=[email])  # Replace with your Gmail email
    #         link = url_for('confirm_email1', token=token, _external=True)
    #         v_msg.body = f'To reset your password, click the link: {link}. The link will expire in 3 minutes. Thank You!'
    #         mail.send(v_msg)
    #
    #         # Store the email in the session for further processing
    #         session['email'] = email
    #
    #     else:
    #         # Show an error message if the email does not exist in the database
    #         error_msg = "Email does not exist in the database. Please enter a valid email address."
    #         return render_template('forgetpass.html', error=error_msg)

    return render_template('forgetpass.html', msg=msg, form=forgetForm)


@app.route('/changepassword')
def changepassword():
    return render_template('changepassword.html')

@app.route('/confirm_email1/<token>')
def confirm_email1(token):
    try:
        # Validate the token and extract the email
        email = s.loads(token, salt='email-confirm', max_age=180)

        # Check if the email exists in the SQL database
        if SQL_Check_Email(email):
            # Redirect the user to the password reset page with the email as a query parameter
            return redirect(url_for('reset_password', email=email))
        else:
            # Show an error message if the email does not exist in the database
            error_msg = "Email does not exist in the database. Please enter a valid email address."
            return render_template('forgetpass.html', error=error_msg)

    except SignatureExpired:
        # Handle expired tokens here, e.g., show an error message
        return render_template('token_expired.html')



@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']

        # Validate the password using password_check()
        password_validation = password_check(new_password)
        if password_validation['password_ok']:
            # Update the password in the database for the given email
            # (Implement SQL_Update_Password(email, new_password) function)

            # Clear the session data for the email after resetting the password
            session.pop('email', None)

            # Redirect the user to the login page after successful password resetou
            return redirect(url_for('login'))
        else:
            # Show an error message if the new password is not valid
            return render_template('reset_password.html', error='Invalid password. Please meet the password requirements.')
    else:
        # Show the password reset form
        return render_template('reset_password.html')




@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        user_otp = request.form.get('otp')
        if 'otp' in session and user_otp == session['otp']:
            session.pop('otp')
            return redirect(url_for('home'))
        else:
            return render_template('verify_otp.html', error='Invalid OTP')
    return render_template('verify_otp.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

#updated logout function to ensure

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    regform = RegisterForm()
    if regform.validate_on_submit():
        username = regform.username.data
        password = regform.password.data
        email = request.form['email']
        phone = regform.phone.data

        if SQL_Register(username,password,email, phone) == 0:
            msg='Succcess'
            # token = s.dumps(email, salt='email-confirm')
            #
            # v_msg = Message('Confirm Email', sender='mohd.irfan.khan.9383@gmail.com', recipients=[email])
            #
            # link = url_for('confirm_email', token=token, _external=True)
            #
            # v_msg.body = 'To confirm your email, click the link {} . The link will expire in 3 minutes! Thank You'.format(
            #     link)
            #
            # mail.send(v_msg)
            #
            # session['username'] = username
            # session['password'] = password
            # session['email'] = email
            #
            # # phone = regform.phone.data  # Get the phone data from the form
            # session['phone'] = phone
            #
            # # Validate the password using password_check()
            # password_validation = password_check(password)
            # print(password_validation)
            # print(password)
            # token = s.dumps(email, salt='email-confirm')
            # link = url_for('confirm_email', token=token, _external=True)
            #
            # # return render_template('thanks.html', username=username, password=password, email=email, link=link)

            # Audit logging for account registration
            log_audit_action("Account registration", f"User: {username}, Email: {email}")

            # return redirect(url_for('email_verification'))
        elif SQL_Register(username, password, email, phone) == 1:
            msg = 'Error'


    return render_template('register.html', msg=msg, form=regform)

@app.route('/email_verification')
def email_verification():
    if 'username' in session and 'password' in session and 'email' in session:
        username = session['username']
        password = session['password']
        email = session['email']

        token = s.dumps(email, salt='email-confirm')
        link = url_for('confirm_email', token=token, _external=True)

        return render_template('thanks.html', username=username, password=password, email=email, link=link)

    return redirect(url_for('register'))


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=180)
        username = session['username']
        password = session['password']
        phone = session['phone']
        SQL_Register(username, password, email, phone)  # Register the account in the database
        session.pop('username', None)
        session.pop('password', None)
        session.pop('email', None)
        session.pop('phone', None)
        return render_template('success.html')
    except SignatureExpired:
        return render_template('fail.html')


@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))


# @app.route('/profile')
# def profile():
#     if 'loggedin' in session:
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute("SELECT * FROM users WHERE id = %s", (session['id'],))
#         account = cursor.fetchone()
#
#         encrypted_email = account['email'].encode()
#
#         file = open('symmetric_user.key', 'rb')
#         key = file.read()
#         file.close()
#         f = Fernet(key)
#         decrypted_email = f.decrypt(encrypted_email)
#
#         return render_template('profile.html', account=account, decrypted_email=decrypted_email)
#     return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE user_ID = %s", (session['id'],))
        account = cursor.fetchone()

        encrypted_email = account['email'].encode()

        file = open('symmetric_user.key', 'rb')
        key = file.read()
        file.close()
        f = Fernet(key)
        decrypted_email = f.decrypt(encrypted_email)

        if 'google_id' in account:
            # User registered with Google account
            if request.method == 'POST':
                password = request.form.get('password')
                phone = request.form.get('phone')

                # Validate the password using password_check()
                password_validation = password_check(password)

                if password_validation['password_ok']:
                    # Update the user's password and phone number in the database
                    SQL_UpdatePasswordAndPhone(session['id'], password, phone)
                    return redirect(url_for('home'))
                else:
                    msg = 'Invalid password. Please make sure your password meets the requirements.'

            return render_template('set_password_phone.html')

        return render_template('profile.html', account=account,decrypted_email=decrypted_email)
        # return render_template('profile.html', account=account, decrypted_email=decrypted_email)

    return redirect(url_for('login'))

@app.route('/set_password_phone', methods=['GET', 'POST'])
def set_password_phone():
    if 'loggedin' in session:
        if 'google_id' in session:
            if request.method == 'POST':
                password = request.form.get('password')
                phone = request.form.get('phone')

                # Validate the password using password_check()
                password_validation = password_check(password)

                if password_validation['password_ok']:
                    # Update the user's password and phone number in the database
                    SQL_UpdatePasswordAndPhone(session['id'], password, phone)
                    return redirect(url_for('home'))
                else:
                    msg = 'Invalid password. Please make sure your password meets the requirements.'

            return render_template('set_password_phone.html')
    return redirect(url_for('login'))

@app.route('/card', methods=['GET', 'POST'])
def card():
    msg = ''
    regcard = RegisterCard()
    try:
        nList = readCards(str(session['id']))
    except:
        print(str(session[id]))


    # print(nList)
    if regcard.validate_on_submit():
        fname = regcard.fname.data
        lname = regcard.lname.data
        userID = str(session['id'])
        fullname = fname + ' ' + lname
        card_num = regcard.card_num.data
        exp_date = regcard.exp_date.data
        cvv = regcard.cvv.data
        if SQL_registerCard(card_num, fname, lname, exp_date, cvv,userID) == 0:
            msg = 'Card added'
            # Audit logging for adding a new card
            log_audit_action("Adding a new card", f"User: {session['username']}, Card Number: {card_num}")
        elif SQL_registerCard(card_num, fname, lname, exp_date, cvv,userID) == 1:
            msg = "Error in adding card"

    print(regcard.fname.data, regcard.lname.data, regcard.card_num.data, regcard.exp_date.data, regcard.cvv.data)
    return render_template('registercard.html', msg=msg, form=regcard, cards=nList)

@app.route('/updateCard', methods=['GET', 'POST'])
def update_card():
    msg=''
    updateForm = UpdateCard()
    if updateForm.validate_on_submit():
        card_num = updateForm.card_num.data
        card_val = updateForm.card_val.data
        uID = str(session['id'])
        if SQL_update_card(card_num,card_val,uID) == 0:
            msg = 'Successful update!'
            # Audit logging for updating card information
            log_audit_action("Updating card information", f"User: {session['username']}, Card Number: {card_num}")
        elif SQL_update_card(card_num,card_val,uID) == 1:
            msg = 'Error in updating'
    return render_template('update.html', msg=msg, form=updateForm)


#Start of Google Oauth
@app.route("/google_login")
def google_login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

# @app.route("/callback")
# def callback():
#     flow.fetch_token(authorization_response=request.url)
#
#     if not session["state"] == request.args["state"]:
#         abort(500)  # State does not match!
#
#     credentials = flow.credentials
#     request_session = requests.session()
#     cached_session = cachecontrol.CacheControl(request_session)
#     token_request = google.auth.transport.requests.Request(session=cached_session)
#
#     id_info = id_token.verify_oauth2_token(
#         id_token=credentials._id_token,
#         request=token_request,
#         audience=GOOGLE_CLIENT_ID
#     )
#
#     session["google_id"] = id_info.get("sub")
#     session["name"] = id_info.get("name")
#     return redirect("/protected_area")

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    google_id = id_info.get("sub")
    name = id_info.get("name")
    email = id_info.get("email")  # Get the email of the user

    # Check if the Google user is already registered in the database
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE google_id = %s", (google_id,))
    user = cursor.fetchone()

    if user:
        # User is already registered, set session and redirect
        session["loggedin"] = True
        session["id"] = user["id"]
        session["username"] = user["username"]
        return redirect(url_for("home"))
    else:
        # User is not registered, add the user to the database
        phone = ""  # You may handle the phone number if needed
        SQL_RegisterGoogleUser(google_id, name, email, phone)

        # Set session for the new user and redirect to the profile page
        cursor.execute("SELECT * FROM users WHERE google_id = %s", (google_id,))
        new_user = cursor.fetchone()
        session["loggedin"] = True
        session["id"] = new_user["id"]
        session["username"] = new_user["username"]

        # Audit logging for Google OAuth login
        log_audit_action("Google OAuth login", f"User: {name}, Email: {email}")

        return redirect(url_for("profile"))



@app.route("/protected_area")
@login_is_required
def protected_area():
    return render_template('home.html')
#END


if __name__ == '__main__':
    app.run(debug=True)
