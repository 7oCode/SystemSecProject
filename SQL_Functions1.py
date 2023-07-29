import MySQLdb.cursors

from Login import *
from flask_mysqldb import MySQL
from flask import Flask, session
from cryptography.fernet import Fernet
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
import logging

# Initialize the logging configuration
logging.basicConfig(
    filename='audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
bcrypt = Bcrypt()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Dbsibm1001.'
app.config['MYSQL_DB'] = 'sys_sec'
mysql = MySQL(app)

def audit_log(action, username):
    # This function will log the action and the username to the audit.log file
    logger.info(f"Action: {action}, Username: {username}")


def SQL_Register(username, password, email, phone):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    dupe = cursor.fetchone()
    print(dupe)
    if dupe:
        return 1
    else:
        hashpwd = bcrypt.generate_password_hash(password)
        email = email.encode()

        key = Fernet.generate_key()
        with open('symmetric_user.key', 'wb') as fo:
            fo.write(key)

        f = Fernet(key)

        encrypted_email = f.encrypt(email)

        cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s, 0, 0)', (username, hashpwd, encrypted_email, phone,))
        # cursor.execute('INSERT INTO users (username, password, email, phone, column1, column2) VALUES (%s, %s, %s, %s, 0, 0)',(username, hashpwd, encrypted_email, phone,))

        # Log the user registration in the database
        audit_log(action="SQL User Registration", username=username)

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
            # d = 'Default'
            # d_s = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # d_s.execute("SELECT * FROM users WHERE username = %s", (d,))
            # d_check = d_s.fetchone()
            # d_num = int(d_check['rate_limit'])
            # if d_num < 3:
            #     d_num += 1
            #     print(d_num)
            #     d_s.execute("UPDATE users SET rate_limit = %s WHERE username = %s", (str(d_num), d,))
            #     return 1
            # else:
            #     d_s.execute("UPDATE users SET rate_limit = '0' WHERE username = %s", (d,))
            #     return 2
        return 1

        # '''if userlogin and bcrypt.check_password_hash(user_hashpwd, password):
        #     #Create session data, data can be accessed in other routes
        #     session['loggedin'] = True
        #     session['id'] = userlogin['id']
        #     session['username'] = userlogin['username']'''

    #updated for session management
    if userlogin and bcrypt.check_password_hash(user_hashpwd, password):
        # Make the session last beyond the browser being closed
        session.permanent = True
        session['loggedin'] = True
        session['id'] = userlogin['user_ID']
        session['username'] = userlogin['username']

        encrypted_email = userlogin['email'].encode()

        file = open('symmetric_user.key', 'rb')
        key = file.read()
        file.close()
        f = Fernet(key)
        decrypted_email = f.decrypt(encrypted_email)
        print(f"Logged in successfully with {decrypted_email.decode()}")

        # Log the login attempt
        if result == 0:
            audit_log(action="SQL Login Success", username=username)
        elif result == 1:
            audit_log(action="SQL Login Failure - Incorrect Username/Password", username=username)
        elif result == 2:
            audit_log(action="SQL Login Failure - Account Locked", username=username)

        return 0
    else:
        print('Pass no match')
        return 2

#login done

# cvv must be encrypted
#assumption: Person -> Cards
#               1..1     1..*
def SQL_registerCard(card_no, fname, lname, exp_date, cvv, uID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    key = Fernet.generate_key()
    fullname = fname + ' ' + lname
    with open('symmetric_card.key', 'wb') as fo:
        fo.write(key)

    f = Fernet(key)

    cursor.execute('SELECT * FROM card_info WHERE card_num = %s', (card_no,))
    dupe = cursor.fetchone()
    decrypted_card = None
    try:
        c_num = dupe['card_num'].encode()
        decrypted_card = c_num.decode()
    except TypeError:
        decrypted_card = 0

    print(decrypted_card)
    if decrypted_card == card_no:
        return 1
    else:
        # mysql.connection.commit()

        # key = Fernet.generate_key()
        with open('symmetric_card.key', 'wb') as fo:
            fo.write(key)

        f = Fernet(key)

        encrypted_cvv = f.encrypt(cvv.encode())
        encrypted_card_no = f.encrypt(card_no.encode())

        cursor.execute('INSERT INTO card_info VALUES (NULL, %s, %s, %s, %s, 0, %s)', (fullname, encrypted_card_no, exp_date, encrypted_cvv, uID))
        mysql.connection.commit()

        audit_log(action="SQL Card Registration", username=username)  # Assuming you have a 'username' variable here

        return 0

def readCards(uID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM card_info WHERE user_id = %s', (str(uID),))
    cList = cursor.fetchall()
    cList = list(cList)
    file = open('symmetric_card.key', 'rb')
    key = file.read()
    file.close()
    f = Fernet(key)
    j = 0
    for i in cList:
        encrypted_card = i['card_num'].encode()
        decrypted_card = f.decrypt(encrypted_card)
        i['card_num'] = decrypted_card.decode()
        cList[j]['card_num'] = i['card_num']
        j+=1
    return cList

def SQL_rate_limit_def():
    d = 'Default'
    d_s = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    d_s.execute("SELECT * FROM users WHERE username = %s", (d,))
    d_check = d_s.fetchone()
    d_num = int(d_check['rate_limit'])
    if d_num < 3:
        d_num += 1
        ds = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        ds.execute("UPDATE users SET rate_limit = %s WHERE username = %s", (d_num, d,))
        ds.execute("SELECT * FROM users WHERE username = %s", (d,))
        nCheck = ds.fetchone()
        mysql.connection.commit()
        print(nCheck)
        return 1
    else:
        d_s.execute("UPDATE users SET rate_limit = '0' WHERE username = %s", (d,))
        mysql.connection.commit()
        print('Return 2')
        return 2

def SQL_rate_limit_user(username):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    uCheck = cursor.fetchone()
    uNum = int(uCheck['rate_limit'])
    if uNum < 3:
        uNum += 1
        uNum = str(uNum)
        uS = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        uS.execute("UPDATE users SET rate_limit = %s WHERE username = %s", (uNum, username,))
        uS.execute("SELECT * FROM users WHERE username = %s", (username,))
        uCheck = uS.fetchone()
        mysql.connection.commit()
        print(uCheck)
        return 1
    else:
        cursor.execute("UPDATE users SET rate_limit = '0' WHERE username = %s", (username,))
        mysql.connection.commit()
        print('Return 2')
        return 2


def SQL_Check_Email(email):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    user = cursor.fetchone()
    cursor.close()

    if user:
        # Email exists in the database
        # Generate a time-limited token for email verification
        token = s.dumps(email, salt='email-confirm')

        # Create a message with the verification link and send it via email
        v_msg = Message('Confirm Email', sender='mohd.irfan.khan.9383@gmail.com', recipients=[email])  # Replace with your Gmail email
        # link = url_for('confirm_email1', token=token, _external=True)
        v_msg.body = f'To reset your password, click the link: {link}. The link will expire in 3 minutes. Thank You!'
        mail.send(v_msg)

        # Store the email in the session for further processing
        session['email'] = emailtop

        return True
    else:
        # Email does not exist in the database
        return 1

def SQL_update_card(cnum, cval, uID):
    pass