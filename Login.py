from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_bcrypt import Bcrypt
import re
from cryptography.fernet import Fernet
from SQL_Functions import *
from forms import *
from twilio.rest import Client
import random

app = Flask(__name__)
bcrypt = Bcrypt()

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'very secret'

# Enter database connection details
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_DB'] = 'sys_sec'

# Initialize MySQL
mysql = MySQL(app)


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
    password_ok = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)
    passClear = re.search(r"""^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]+$""", password) is not None
    print(passClear)
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


@app.route('/WebApp', methods=['GET', 'POST'])
def login():
    msg = ''
    login = LoginForm()
    if login.validate_on_submit():
        username = login.username.data
        password = login.password.data

        # Validate the password using password_check()
        password_validation = password_check(password)

        if SQL_Login(username, password) == 0 and password_validation['password_ok']:
            # Generate OTP and store it in the session
            otp = str(random.randint(100000, 999999))
            session['otp'] = otp

            # # Get user's phone number from the database
            # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            # user = cursor.fetchone()
            # phone_number = user['phone_no']
            #
            # # Send OTP via SMS
            # account_sid = 'ACa1c4471cfc07d62502d48bd509232754'
            # auth_token = 'f94c6e3669f4da38b2498f5294493925'
            # client = Client(account_sid, auth_token)
            #
            # message = client.messages.create(
            #     body=f"Your OTP is {otp}",
            #     from_='+15738594156',
            #     to=phone_number
            # )

            # return redirect(url_for('verify_otp'))
            return redirect(url_for('home'))
        else:
            if SQL_rate_limit(username) == 1:
                msg = 'Incorrect Username/Password'
                # Pass the password validation results to the template
                return render_template('index.html', msg=msg, form=login, password_validation=password_validation)
            elif SQL_rate_limit(username) == 2:
                msg = 'Account has been locked'
                return render_template('index.html', msg=msg, form=login, password_validation=password_validation)



    return render_template('index.html', msg='', form=login)

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


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    regform = RegisterForm()
    if regform.validate_on_submit():
        username = regform.username.data
        password = regform.password.data
        email = regform.email.data
        phone = regform.phone.data  # Get the phone data from the form

        # Validate the password using password_check()
        password_validation = password_check(password)
        print(password_validation)
        print(password)

        if password_validation['password_ok']:
            if SQL_Register(username, password, email, phone) == 0:  # Pass the phone data to the SQL_Register function
                msg = 'Successful registration'
            elif SQL_Register(username, password, email, phone) == 1:  # Pass the phone data to the SQL_Register function
                msg = 'Duplicate found'
        else:
            msg = 'Invalid password. Please make sure your password meets the requirements.'
    elif request.method == 'POST':
        msg = 'Please fill out the form'
        print(regform.errors)  # Print form errors

    return render_template('register.html', msg=msg, form=regform)



@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE id = %s", (session['id'],))
        account = cursor.fetchone()

        encrypted_email = account['email'].encode()

        file = open('symmetric_user.key', 'rb')
        key = file.read()
        file.close()
        f = Fernet(key)
        decrypted_email = f.decrypt(encrypted_email)

        return render_template('profile.html', account=account, decrypted_email=decrypted_email)
    return redirect(url_for('login'))


@app.route('/card', methods=['GET', 'POST'])
def card():
    msg = ''
    regcard = RegisterCard()
    nList = readCards()
    print(nList)
    if regcard.validate_on_submit():
        fname = regcard.fname.data
        lname = regcard.lname.data
        fullname = fname + ' ' + lname
        card_num = regcard.card_num.data
        exp_date = regcard.exp_date.data
        cvv = regcard.cvv.data
        if SQL_registerCard(card_num, fname, lname, exp_date, cvv) == 0:
            msg = 'Card added'
        elif SQL_registerCard(card_num, fname, lname, exp_date, cvv) == 1:
            msg = "Error in adding card"
    else:
        print(regcard.fname.data, regcard.lname.data, regcard.card_num.data, regcard.exp_date.data, regcard.cvv.data)
    return render_template('registercard.html', msg=msg, form=regcard, cards=nList)


if __name__ == '__main__':
    app.run()
