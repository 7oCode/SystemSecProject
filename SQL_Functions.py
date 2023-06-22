from Login import *
from flask_mysqldb import MySQL
from flask import Flask, session
from cryptography.fernet import Fernet

app = Flask(__name__)
bcrypt = Bcrypt()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_DB'] = 'sys_sec'
mysql = MySQL(app)


def SQL_Register(username, password, email):

        hashpwd = bcrypt.generate_password_hash(password)
        email = email.encode()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        dupe = cursor.fetchone()
        if dupe:
            return 1
        else:
            mysql.connection.commit()
            msg='Successful Registration :)'

            key = Fernet.generate_key()
            with open('symmetric.key', 'wb') as fo:
                fo.write(key)

            f = Fernet(key)

            encrypted_email = f.encrypt(email)

            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s)',(username, hashpwd, encrypted_email))
            mysql.connection.commit()
            return 0

def SQL_Login(username, password):
    #Check if account exists using MySQL
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))

    #Fetch one record and return result
    ## Need to change ##
    userlogin = cursor.fetchone()
    user_hashpwd = userlogin['password']

    if userlogin and bcrypt.check_password_hash(user_hashpwd, password):
        #Create session data, data can be accessed in other routes
        session['loggedin'] = True
        session['id'] = userlogin['id']
        session['username'] = userlogin['username']

        encrypted_email = userlogin['email'].encode()

        file = open('symmetric.key', 'rb')
        key = file.read()
        file.close()
        f = Fernet(key)
        decrypted_email = f.decrypt(encrypted_email)
        print(f"Logged in successfully with {decrypted_email.decode()}")
        return 0
    else:
        return 1
