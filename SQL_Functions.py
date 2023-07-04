# import Bcrypt as Bcrypt

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
    try:
        user_hashpwd = userlogin['password']
    except TypeError:
        return 1

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
#login done

#assumption: 1 person, multiple cards, unique name, unique number
def SQL_registerCard(fname, lname, card_num, exp_date, cvv):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('Select * from card_info where card_num = %s', (card_num,))
    usercard = cursor.fetchone()
    try:
        u_card = usercard['card_num'].encode()
        file = open('symmetric.key', 'rb')
        key = file.read()
        file.close()
        f = Fernet(key)
        dec_card = f.decrypt(u_card)
        de_card = dec_card.decode()
    except:
        return 1

    if de_card == card_num:
        return 2
    else:
        n_card = f.encrypt(card_num)
        cursor.execute("Insert into card_info values (NULL, concat_ws(' ', %s, %s), %s, %s, %s", (fname, lname, n_card, exp_date,cvv,))
        print('Card added')
        mysql.connection.commit()
        return 0



