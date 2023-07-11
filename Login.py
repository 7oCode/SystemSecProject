from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_bcrypt import Bcrypt
import re
import cryptography
from cryptography.fernet import Fernet
from SQL_Functions import *
from forms import *
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


# http://localhost:5000/P_SQL/ - this will be the login page, we need to use both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def homepage():
    return redirect(url_for('login'))


# c = Counter()

#limiting done
@app.route('/WebApp', methods=['GET', 'POST'])
def login():
    # Output message is something is wrong
    msg = ''
    # if c.i == 3:
    #     return render_template('stop.html')

    # Check if username and password requests exists (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Variables for easy access
        username = request.form['username']
        password = request.form['password']

        if SQL_Login(username, password) == 0:
            return redirect(url_for('home'))
        elif SQL_Login(username, password) == 1:
            msg = 'Incorrect username/password'
            # print(c.i)
            # c.i +=1
            return render_template('index.html', msg=msg)

    # else:
    #     #Account doesn't exist or username/password incorrect
    #     msg = 'Incorrect username/password'

    # Login form with message (if any)
    return render_template('index.html', msg='')


# http://localhost:5000/P_SQL/logout - the logout page
@app.route('/logout')
def logout():
    # Remove session data, the user will be logged out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    # Redirect to login page
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    regform = RegisterForm()

    if regform.validate_on_submit():
        username = regform.username.data
        password = regform.password.data
        email = regform.email.data
        if SQL_Register(username, password, email) == 0:
            msg = 'Successful registration'
        elif SQL_Register(username, password, email) == 1:
            msg = 'Duplicate found'
    elif request.method == 'POST':
        # Form is empty (no POST Data)
        msg = 'Please fill out the form'

    return render_template('register.html',msg=msg, form=regform)



# http://localhost:5000/home - Home page, only accessible for logged in users
@app.route('/home')
def home():
    # Check if user is logged in
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])

    # User is not loggedin, redirect to login page
    return redirect(url_for('login'))


# http://localhost:5000/profile = Profile page, only accesible for logged in users
@app.route('/profile')
def profile():
    if 'loggedin' in session:
        # All account info for the user to display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM users WHERE id = %s", (session['id'],))
        account = cursor.fetchone()

        encrypted_email = account['email'].encode()

        file = open('symmetric.key', 'rb')
        key = file.read()
        file.close()
        f = Fernet(key)
        decrypted_email = f.decrypt(encrypted_email)

        # Show profile page with account info
        return render_template('profile.html', account=account, decrypted_email=decrypted_email)

    # User is not logged in, redirect to login page
    return redirect(url_for('login'))

@app.route('/card', methods=['GET', 'POST'])
def card():
    msg=''
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
        if SQL_registerCard(card_num,fname,lname,exp_date, cvv) == 0:
            msg = 'Card added'
        elif SQL_registerCard(card_num,fname,lname,exp_date,cvv) == 1:
            msg = "Error in adding card"

    else:
        print(regcard.fname.data,regcard.lname.data,regcard.card_num.data,regcard.exp_date.data,
              regcard.cvv.data)

    return render_template('registercard.html', msg=msg, form=regcard, cards=nList)


if __name__ == '__main__':
    app.run()
