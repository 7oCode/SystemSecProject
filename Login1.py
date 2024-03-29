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

from twilio.rest import Client
from datetime import timedelta
import smtplib
import pyotp
import qrcode
from io import BytesIO
import base64


from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import PyPDF2

from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm, RecaptchaField

from google_auth_oauthlib.flow import Flow, InstalledAppFlow
import google.auth.transport.requests
import tkinter as tk
from tkinter import ttk
import os
import pathlib
from pathlib import Path
import requests
import time
from flask_session import Session

app = Flask(__name__)
bcrypt = Bcrypt()

app.config['RECAPTCHA_PUBLIC_KEY'] = '6Ld_BVEnAAAAAJWCzb859ZSVXSMN7vxwVOgNkDEk'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6Ld_BVEnAAAAAEqVkudxjudXLE0WfM0QfBrlX_1V'

s = URLSafeTimedSerializer('Thisisasecret!')

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'very secret'

# Enter database connection details
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_DB'] = 'sys_sec'

app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'mohd.irfan.khan.9383@gmail.com'
app.config['MAIL_PASSWORD'] = 'afxjkjngfitkekzs'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True



# Set the session timeout to 10 minutes
app.config['SESSION_PERMANENT'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=0.5)

# Configure the session to use Flask-Session extension
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Initialize MySQL
mysql = MySQL(app)
mail = Mail(app)

# Start of google oauth

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "20330302842-28sotd6auelvra12rqi94ah5rb456n23.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email",
            "openid"],
    redirect_uri="https://127.0.0.1:5000/callback"
)


# create audit log function
def add_audit_log(log_message, log_type):
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO audit_logs VALUES (NULL, %s, %s)', (log_message, log_type,))
    mysql.connection.commit()
    cursor.close()


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


# End


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
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\]^`{|}~" + r'"]', password) is None

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


LOCKOUT_DURATION = 30  # Lockout duration in seconds

cnum = 0


@app.route('/fail', methods=['GET', 'POST'])
def failpage():
    remaining_time = 0
    if session.get('locked_out'):
        lockout_time = session['locked_out']
        current_time = time.time()
        if current_time - lockout_time <= LOCKOUT_DURATION:
            remaining_time = int(LOCKOUT_DURATION - (current_time - lockout_time))
            return render_template('wait.html', remaining_time=remaining_time)
        else:
            session.pop('locked_out', None)
        return redirect(url_for('login'))

    return render_template('wait.html', remaining_time=remaining_time)


@app.route('/WebApp', methods=['GET', 'POST'])
def login():
    msg = ''
    login = LoginForm()
    try:
        if session['locked_out'] is True:
            return redirect(url_for('failpage'))
    except:
        print("All good")

    if login.validate_on_submit():
        username = login.username.data
        password = login.password.data

        # Validate the password using password_check()
        # password_validation = password_check(password)
        #  and password_validation['password_ok']
        #         print(SQL_Login(username,password))
        if SQL_Login(username, password) == 0:
            if check_ratelimit(username) == 3:
                return redirect(url_for('forceuser'))

            # super important don't remove
            # Generate OTP and store it in the session
            otp = str(randint(100000, 999999))
            session['otp'] = otp

            # Get user's phone number from the database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            phone_number = user['phone_no']

            # Send OTP via SMS
            account_sid = 'ACa1c4471cfc07d62502d48bd509232754'
            auth_token = '5a0fd865769b3025f40aaa31d6d35f26'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=f"Your OTP is {otp}",
                from_='+15738594156',
                to=phone_number
            )

            return redirect(url_for('verify_otp'))
            print(f"{username}, {password}")

            # Add a log entry for successful login
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"Successful Login for user '{username}' via username/password at time: {date_time_str}"
            # log_message = f"Successful registration for user {username} at time: {date_time_str}"
            add_audit_log(log_message, 'login')

            return redirect(url_for('home'))
        elif SQL_Login(username, password) == 1:
            a = SQL_rate_limit_def()
            if a == 1:
                msg = 'Incorrect Username/Password(d)'
                print(f"{username}, {password}")
            elif a == 2:
                session['locked_out'] = time.time()
                return redirect(url_for('failpage'))

            # Add a log entry for unsuccessful login
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"Unsuccessful Login for user '{username}' via username/password at time: {date_time_str}"
            # log_message = f"Successful registration for user {username} at time: {date_time_str}"
            add_audit_log(log_message, 'login')

        elif SQL_Login(username, password) == 2:
            u = SQL_rate_limit_user(username)
            if u == 1:
                msg = 'Incorrect Username/Password(u)'
                print(f"{username}, {password}")
            elif u == 2:
                return redirect(url_for('forceuser'))

            # Add a log entry for unsuccessful login
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"Unsuccessful Login for user '{username}' via username/password at time: {date_time_str}"
            # log_message = f"Successful registration for user {username} at time: {date_time_str}"
            add_audit_log(log_message, 'login')

        # authorization_url, state = flow.authorization_url()
        # session["state"] = state
        # return redirect(authorization_url)

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


chUser = ''


@app.route('/forget_password', methods=['GET', 'POST'])
def forget():
    msg = ''
    forgetForm = forgetPassword()
    if forgetForm.validate_on_submit():
        global chUser
        email = forgetForm.email.data
        user = forgetForm.username.data
        chUser = user
        # print(SQL_Check_Email(email, user))
        if SQL_Check_Email(email, user) == 0:
            msg = 'Email sent to user'
            # # Email exists in the database
            # # Generate a time-limited token for email verification
            # token = s.dumps(email, salt='email-confirm')
            #
            # # Create a message with the verification link and send it via email
            # v_msg = Message('Confirm Email', sender='mohd.irfan.khan.9383@gmail.com',
            #                 recipients=[email])  # Replace with your Gmail email
            # link = url_for('confirm_email1', token=token, _external=True)
            # v_msg.body = f'To reset your password, click the link: {link}. The link will expire in 3 minutes. Thank You!'
            # mail.send(v_msg)
            #
            # # Store the email in the session for further processing
            # session['email'] = email
            # chUser = user
            print(question(chUser))
            return redirect(url_for('changepassword'))

        elif SQL_Check_Email(email, user) == 1:
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


@app.route('/forcechange', methods=['GET', 'POST'])
def forceuser():
    msg = ''
    forgetForm = forgetPassword()
    if forgetForm.validate_on_submit():
        global chUser
        email = forgetForm.email.data
        user = forgetForm.username.data
        # print(SQL_Check_Email(email, user))
        if SQL_Check_Email(email, user) == 0:
            msg = 'Email sent to user'
            # Email exists in the database
            # Generate a time-limited token for email verification
            # token = s.dumps(email, salt='email-confirm')
            #
            # # Create a message with the verification link and send it via email
            # v_msg = Message('Confirm Email', sender='mohd.irfan.khan.9383@gmail.com',
            #                 recipients=[email])  # Replace with your Gmail email
            # link = url_for('confirm_email1', token=token, _external=True)
            # v_msg.body = f'To reset your password, click the link: {link}. The link will expire in 3 minutes. Thank You!'
            # mail.send(v_msg)
            #
            # # Store the email in the session for further processing
            # session['email'] = email
            chUser = user
            print(question(chUser))
            return redirect(url_for('changepassword'))

        elif SQL_Check_Email(email, user) == 1:
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

    return render_template('forcepass.html', msg=msg, form=forgetForm)


@app.route('/forcechange', methods=['GET', 'POST'])
def forcepassword():
    msg = ''
    changepwd = changePassword()
    changepwd.securityquestion.data = question(chUser)

    if changepwd.validate_on_submit():
        npwd = changepwd.npassword.data
        # opwd = changepwd.opassword.data
        # squest = changepwd.securityquestions.data
        sans = changepwd.s_ans.data
        if SQL_Update_Password(chUser,npwd,sans) == 0:
            return redirect(url_for("login"))
        elif SQL_Update_Password(chUser, npwd, sans) == 1:
            msg = "Error"
    print(changepwd.validate_on_submit())

    return render_template('forcechange.html', form=changepwd, msg=msg)


@app.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
    msg = ''

    changepwd = changePassword()
    changepwd.securityquestion.data = question(chUser)

    if changepwd.validate_on_submit():
        npwd = changepwd.npassword.data
        # opwd = changepwd.opassword.data
        # squest = changepwd.securityquestions.data
        sans = changepwd.s_ans.data
        print('we in')
        if SQL_Update_Password(chUser, npwd,sans) == 0:
            return redirect(url_for("login"))
        elif SQL_Update_Password(chUser, npwd, sans) == 1:
            msg = "Error"
    print(changepwd.validate_on_submit())

    return render_template('changepassword.html', form=changepwd, msg=msg)


@app.route('/confirm_email1/<token>')
def confirm_email1(token):
    try:
        # Validate the token and extract the email
        email = s.loads(token, salt='email-confirm', max_age=180)

        # Check if the email exists in the SQL database
        if SQL_Check_Email(email,authUser):
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
            return render_template('reset_password.html',
                                   error='Invalid password. Please meet the password requirements.')
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

    # Clear session data, this will log the user out
    session.clear()
    print(session.clear())

    # Redirect to login page
    return redirect(url_for('login'))

# updated logout function to ensure
authUser = None
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    regform = RegisterForm()
    if regform.validate_on_submit():
        global authUser
        username = regform.username.data
        password = regform.password.data
        email = request.form['email']
        authUser = username
        phone = regform.phone.data
        squest = regform.securityquestions.data
        s_ans = regform.s_ans.data

        if SQL_Register(username, password, email, phone, squest, s_ans) == 0:
            msg = 'Succcess'

            token = s.dumps(email, salt='email-confirm')

            v_msg = Message('Confirm Email', sender='mohd.irfan.khan.9383@gmail.com', recipients=[email])

            link = url_for('confirm_email', token=token, _external=True)

            v_msg.body = 'To confirm your email, click the link {} . The link will expire in 3 minutes! Thank You'.format(
                link)

            mail.send(v_msg)

            session['username'] = username
            session['password'] = password
            session['email'] = email
            session['squest'] = squest
            session['s_ans'] = s_ans

            # phone = regform.phone.data  # Get the phone data from the form
            session['phone'] = phone

            # Validate the password using password_check()
            password_validation = password_check(password)
            print(password_validation)
            print(password)
            token = s.dumps(email, salt='email-confirm')
            link = url_for('confirm_email', token=token, _external=True)

            return render_template('thanks.html', username=username, password=password, email=email, link=link)

            # Add a log entry for successful registration
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"Successful registration for user '{username}' via username/password at time: {date_time_str}"
            # log_message = f"Successful registration for user {username} at time: {date_time_str}"
            add_audit_log(log_message, 'registration')
            # return redirect(url_for('email_verification'))


        elif SQL_Register(username, password, email, phone, squest, s_ans) == 1:
            msg = 'Error'

            # Add a log entry for unsuccessful registration
            now = datetime.now()
            date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"Unsuccessful registration for user '{username}' via username/password at time: {date_time_str}"
            # log_message = f"Unsuccessful registration for user {username} at time: {date_time_str}"
            add_audit_log(log_message, 'registration')

    return render_template('register.html', msg=msg, form=regform)


@app.route('/email_verification')
def email_verification():
    if ('username' in session) and ('password' in session) and ('email' in session):
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
        squest = session['squest']
        s_ans = session['s_ans']
        SQL_Register(username, password, email, phone, squest, s_ans)  # Register the account in the database
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

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    pass


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE user_ID = %s", (session['id'],))
        account = cursor.fetchone()
        dlist = []
        j = 0
        print(account)
        for filename in os.listdir():
            if filename.endswith('.key') and filename.__contains__(account['username']):
                dlist.append(filename)

        dlist.sort()
        # decrypted_email = None
        try:
            for a in dlist:
                en_mail = account['email'].encode()
                file = open(a, 'rb')
                key = file.read()
                file.close()
                f = Fernet(key)
                decrypted_email = f.decrypt(en_mail)
                account['email'] = decrypted_email.decode()
        except Exception as e:
            print(f"Error {e}")
        else:
            decrypted_email = account['email']

            # if 'google_id' in account:
            #     # User registered with Google account
            #     if request.method == 'POST':
            #         password = request.form.get('password')
            #         phone = request.form.get('phone')
            #
            #         # Validate the password using password_check()
            #         password_validation = password_check(password)
            #
            #         if password_validation['password_ok']:
            #             # Update the user's password and phone number in the database
            #             SQL_UpdatePasswordAndPhone(session['id'], password, phone)
            #             return redirect(url_for('home'))
            #         else:
            #             msg = 'Invalid password. Please make sure your password meets the requirements.'
            #
            #     return render_template('set_password_phone.html')

            return render_template('profile.html', account=account, decrypted_email=decrypted_email)
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
        return render_template('registercard.html', msg=msg, form=regcard, cards=[])

    try:
        ohist = transactions(str(session['id']))
    except Exception as e:
        print(f'Error: {e}')
        return render_template('registercard.html', msg=msg, form=regcard, cards=nList, hist=[])

    # print(nList)
    if regcard.validate_on_submit():
        fname = regcard.fname.data
        lname = regcard.lname.data
        userID = str(session['id'])
        fullname = fname + ' ' + lname
        card_num = regcard.card_num.data
        exp_date = regcard.exp_date.data
        cvv = regcard.cvv.data
        if SQL_registerCard(card_num, fname, lname, exp_date, cvv, userID) == 0:
            msg = 'Card added'
        elif SQL_registerCard(card_num, fname, lname, exp_date, cvv, userID) == 1:
            msg = "Error in adding card"

    print(regcard.fname.data, regcard.lname.data, regcard.card_num.data, regcard.exp_date.data, regcard.cvv.data)
    return render_template('registercard.html', msg=msg, form=regcard, cards=nList, hist=ohist)


@app.route('/updateCard', methods=['GET', 'POST'])
def update_card():
    msg = ''
    updateForm = UpdateCard()
    if updateForm.validate_on_submit():
        card_num = updateForm.card_num.data
        card_val = updateForm.card_val.data
        try:
            uID = str(session['id'])
        except KeyError:
            uID = str(session['id'])
        if SQL_update_card(card_num, card_val, uID) == 0:
            msg = 'Successful update!'
        elif SQL_update_card(card_num, card_val, uID) == 1:
            msg = 'Error in updating'
    return render_template('update.html', msg=msg, form=updateForm)


@app.route('/newTransaction', methods=['GET', 'POST'])
def newtransaction():
    msg = ''
    newT = newTransaction()

    if newT.validate_on_submit():
        cnum = newT.card_num.data
        trans = newT.transaction.data
        cost = newT.cost.data
        uID = str(session['id'])
        if SQL_New_Transaction(cnum, trans, cost, uID) == 0:
            msg = "Transaction Added"
        elif SQL_New_Transaction(cnum, trans, cost, uID) == 1:
            msg = "Error in adding transaction"

    return render_template('transaction.html', msg=msg, form=newT)


@app.route('/uploadFile', methods=['GET', 'POST'])
def uploadfile():
    msg = ''
    form = UploadForm()
    fpath = r"C:\Users\Student\Downloads\\"
    if form.validate_on_submit():
        pdf_file = form.pdf_file.data
        fname = fpath + pdf_file
        with open(fname, 'rb') as source_file:
            with open('Upload.docx', 'wb') as destination_file:
                destination_file.write(source_file.read())

        # Perform further processing or save to database

        msg = 'File uploaded successfully'

    return render_template('uploadfile.html', form=form, msg=msg)

@app.route('/forcereset', methods=['GET', 'POST'])
def forcereset():
    msg = ''
    pwreset = ForceReset()

    if pwreset.validate_on_submit():
        username = pwreset.userreset.data
        if SQL_Check_User(username) == 0:
            msg = "User will reset on next login"
        elif SQL_Check_User(username) == 1:
            msg = "User does not exist"

    return render_template('forcereset.html', msg=msg, form=pwreset)


# Start of Google Oauth
@app.route("/google_login")
def google_login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


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
        session["id"] = user["user_ID"]
        session["username"] = user["username"]
        return redirect(url_for("home"))

        # Add a log entry for successful Google Oauth Login
        now = datetime.now()
        date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"Successful login for user '{username}' via via Google OAuth at time: {date_time_str}"
        # log_message = f"Successful registration for user {username} at time: {date_time_str}"
        add_audit_log(log_message, 'login')
    else:
        # User is not registered, add the user to the database
        phone = ""  # You may handle the phone number if needed
        SQL_RegisterGoogleUser(google_id, name, email, phone)

        # Set session for the new user and redirect to the profile page
        cursor.execute("SELECT * FROM users WHERE google_id = %s", (google_id,))
        new_user = cursor.fetchone()
        session["loggedin"] = True
        session["id"] = new_user["user_ID"]
        session["username"] = new_user["username"]
        return redirect(url_for("profile"))

        # Add a log entry for successful Google Oauth Login
        now = datetime.now()
        date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"Successful registration for user '{username}' via via Google OAuth at time: {date_time_str}"
        # log_message = f"Successful registration for user {username} at time: {date_time_str}"
        add_audit_log(log_message, 'registration')


def SQL_RegisterGoogleUser(google_id, name, email, phone):
    cursor = mysql.connection.cursor()
    pw = '$2b$12$2KBJ6o8rUJgHBKjA3ldqy.uKnhSay0GMTSv8uC8EkQScdtg9CU.JG'
    """pw - Jeff@1234
    email - Jeff@gmail.com"""
    jeff = 'gAAAAABk2NL8ZhwyQuPZUo6a6rvNfejC9c51J51GiTAm6xVizxOWxliQofE11vCNVEn52P2DtAGRpm7EiaGgHdo5M2QTOcUMiw=='
    hp='+6583098239'
    cursor.execute("INSERT INTO users VALUES (NULL, %s, %s, %s, %s, 0, 0, %s, 'Q2: What is 2+2?','4')",
                   (name,pw, jeff, hp, google_id))
    mysql.connection.commit()
    cursor.close()


def SQL_UpdatePasswordAndPhone(user_id, password, phone):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE users SET password = %s, phone_no = %s WHERE id = %s", (password, phone, user_id))
    mysql.connection.commit()
    cursor.close()


@app.route("/protected_area")
@login_is_required
def protected_area():
    return render_template('protected_area.html')


@app.route('/MyWebApp/admin_login_page', methods=['GET', 'POST'])
def admin_login_page():
    return render_template('admin_login_page.html')


@app.route('/check_for_admin_login/', methods=['GET', 'POST'])
def check_admin_login():
    # print(request.method)
    if request.method == 'POST':
        correct_username = 'admin'
        correct_password = 'admin'
        entered_username = request.form['admin_username']
        entered_password = request.form['admin_password']
        entered_email = request.form['admin_email']
        # print(correct_username, correct_password, entered_username, entered_password)
        if entered_username == correct_username and entered_password == correct_password:
            # print(correct_username, correct_password, entered_username, entered_password)

            # app.config["MAIL_SERVER"] = 'smtp.gmail.com'
            # app.config["MAIL_PORT"] = 465
            # app.config["MAIL_USERNAME"] = 'mohd.irfan.khan.9383@gmail.com'
            # app.config['MAIL_PASSWORD'] = 'afxjkjngfitkekzs'
            # app.config['MAIL_USE_TLS'] = False
            # app.config['MAIL_USE_SSL'] = True
            print('subyes')
            # Generate OTP and send it to the user's email
            otp = str(randint(100000, 999999))
            TO = entered_email  # user's email
            FROM = 'mohd.irfan.khan.9383@gmail.com'  # coder's Gmail email
            SUBJECT = "Verification"
            TEXT = str("Your OTP is: " + otp)
            MESSAGE = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(FROM, 'afxjkjngfitkekzs')  # coder's email password
            server.sendmail(FROM, TO, MESSAGE)

            # Store OTP and username in the session
            session['otp'] = otp
            session['username'] = entered_username

            # Redirect to OTP verification page
            return redirect(url_for('otp_verification'))

            # # Redirect to login_2fa_form verification page
            # return redirect(url_for('login_2fa'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('admin_login_page.html')

# email otp part
@app.route('/otp_verification', methods=['GET', 'POST'])
def otp_verification():
    if 'otp' in session and 'username' in session:
        if request.method == 'POST':
            entered_otp = request.form.get('otp')
            stored_otp = session['otp']
            print(entered_otp, stored_otp)
            if entered_otp == stored_otp:
                # OTP verification successful
                # Perform the login action
                return redirect(url_for('login_2fa'))
            else:
                error_msg = "Invalid OTP. Please try again."
                return render_template('otp_verification.html', error=error_msg)

        # Handle the case when the request method is 'GET'
        return render_template('otp_verification.html')

    # Handle the case when 'otp' or 'username' is not in the session
    return redirect(url_for('admin_login_page'))


@app.route('/MyWebApp/admin_home_page', methods=['GET', 'POST'])
def admin_home_page():
    return render_template('admin_home_page.html')


def display_logs():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM audit_logs")
    logs = cursor.fetchall()
    logs = list(logs)
    # print(logs)

    return logs


@app.route('/MyWebApp/admin_view_logs', methods=['GET', 'POST'])
def admin_view_logs():
    logs = display_logs()
    # print(logs)
    return render_template('admin_view_logs.html', logs=logs)


# ----------- Google Authentication 2FA ---------------

# generating random PyOTP in hex format
print(pyotp.random_hex()) # returns a 32-character hex-encoded secret

@app.route("/login/2fa/")
def login_2fa():
    # Generating random secret key for authentication
    secret = pyotp.random_base32()

    # Generating TOTP instance for the QR code
    totp = pyotp.TOTP(secret)
    otp_url = totp.provisioning_uri("MyWebApp:admin", issuer_name="MyWebApp Admin")

    # Generate a QR code image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(otp_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_io = BytesIO()
    img.save(img_io)
    img_data = img_io.getvalue()

    # Encode the image data as base64
    img_base64 = base64.b64encode(img_data).decode("utf-8")

    return render_template("login_2fa.html", secret=secret, qr_code=img_base64)




# 2FA form route
@app.route("/login/2fa/", methods=["POST"])
def login_2fa_form():
    # getting secret key used by user
    secret = request.form.get("secret")
    # getting OTP provided by user
    otp = int(request.form.get("otp"))

    # verifying submitted OTP with PyOTP
    if pyotp.TOTP(secret).verify(otp):
        # inform users if OTP is valid
        flash("The TOTP 2FA token is valid", "success")
        return redirect(url_for("admin_home_page"))
    else:
        # inform users if OTP is invalid
        flash("You have supplied an invalid 2FA token!", "danger")
        return redirect(url_for("login_2fa"))

# END


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=5000, ssl_context=(Path('./ssl.crt'), Path('./ssl.key')))
