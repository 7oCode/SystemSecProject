from flask import Flask, render_template, request, redirect, url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_bcrypt import Bcrypt
import re
import cryptography
from cryptography.fernet import Fernet

app = Flask(__name__)
bcrypt = Bcrypt()

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'very secret'

# Enter database connection details
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_DB'] = 'pythonlogin'

# Initialize MySQL
mysql = MySQL(app)

# http://localhost:5000/P_SQL/ - this will be the login page, we need to use both GET and POST requests
@app.route('/', methods=['GET','POST'])
def homepage():
    return redirect(url_for('login'))

@app.route('/WebApp', methods=['GET', 'POST'])
def login():

    #Output message is something is wrong
    msg=''

    #Check if username and password requests exists (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Variables for easy access
        username = request.form['username']
        password = request.form['password']

        #Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))

        #Fetch one record and return result
        ## Need to change ##
        account = cursor.fetchone()
        user_hashpwd = account['password']

        if account and bcrypt.check_password_hash(user_hashpwd, password):
            #Create session data, data can be accessed in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']

            encrypted_email = account['email'].encode()

            file = open('symmetric.key', 'rb')
            key = file.read()
            file.close()
            f = Fernet(key)
            decrypted_email = f.decrypt(encrypted_email)

            #Redirect to home page
            print(f"Logged in successfully with {decrypted_email.decode()}")
            return redirect(url_for('home'))
    else:
        #Account doesn't exist or username/password incorrect
        msg = 'Incorrect username/password'

    #Login form with message (if any)
    return render_template('index.html', msg='')


#http://localhost:5000/P_SQL/logout - the logout page
@app.route('/logout')
def logout():
    #Remove session data, the user will be logged out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    #Redirect to login page
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        hashpwd = bcrypt.generate_password_hash(password)
        email = email.encode()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        dupe = cursor.fetchone()
        if not dupe:
            msg = 'Duplicate found'
        else:
            mysql.connection.commit()
            msg='Successful Registration :)'

        key = Fernet.generate_key()
        with open('symmetric.key', 'wb') as fo:
            fo.write(key)

        f = Fernet(key)

        encrypted_email = f.encrypt(email)

        cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)',(username, hashpwd, encrypted_email))
        mysql.connection.commit()
        msg = 'Successful registration'


    elif request.method == 'POST':
        #Form is empty (no POST Data)
        msg='Please fill out the form'

    return render_template('register.html', msg=msg)


#http://localhost:5000/home - Home page, only accessible for logged in users
@app.route('/home')
def home():
    #Check if user is logged in
    if 'loggedin' in session:
        return render_template('home.html',username=session['username'])

    #User is not loggedin, redirect to login page
    return redirect(url_for('login'))


#http://localhost:5000/profile = Profile page, only accesible for logged in users
@app.route('/profile')
def profile():
    if 'loggedin' in session:
        #All account info for the user to display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts WHERE id = %s", (session['id'],))
        account = cursor.fetchone()

        #Show profile page with account info
        return render_template('profile.html', account=account)

    # User is not logged in, redirect to login page
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
