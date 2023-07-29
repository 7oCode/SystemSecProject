import os

import MySQLdb.cursors

from Login1 import *
from flask_mysqldb import MySQL
from flask import Flask, session
from cryptography.fernet import Fernet
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message

app = Flask(__name__)
bcrypt = Bcrypt()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_DB'] = 'sys_sec'
mysql = MySQL(app)


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

        filename = f"{username}.key"
        # filedir = r"""C:/Users/Student/Desktop/Modules/IT2656_SystemsSecurityProject/SystemSecProject/newP/symmetric_user"""
        # filepath = os.path.join(filedir, filename)
        with open(filename,'wb') as fo:
            fo.write(key)

        f = Fernet(key)

        encrypted_email = f.encrypt(email)

        cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s, 0, 0)', (username, hashpwd, encrypted_email, phone,))
        # cursor.execute('INSERT INTO users (username, password, email, phone, column1, column2) VALUES (%s, %s, %s, %s, 0, 0)',(username, hashpwd, encrypted_email, phone,))

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
        print("Pass not found?")
        return 2

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
        try:
            file = open(f'{username}.key', 'rb')
        except FileNotFoundError:
            print("File Not Found")
        key = file.read()
        file.close()
        f = Fernet(key)
        decrypted_email = f.decrypt(encrypted_email)
        print(f"Logged in successfully with {decrypted_email.decode()}")
        return 0
    else:
        print('Pass no match')
        return 2



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

    cursor.execute('SELECT * FROM card_info WHERE user_id = %s', (uID,))
    dupe = cursor.fetchone()
    print(dupe)
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
        cList = []
        for filename in os.listdir():
            if filename.endswith('_card.key') and filename.__contains__(str(uID)):
                cList.append(filename)

        n = 1
        for newcard in cList:
            if newcard == f"{uID}_{n}.key":
                n += 1


        # key = Fernet.generate_key()
        with open(f'{uID}_{n}_card.key', 'wb') as fo:
            fo.write(key)

        f = Fernet(key)

        encrypted_cvv = f.encrypt(cvv.encode())
        encrypted_card_no = f.encrypt(card_no.encode())

        cursor.execute('INSERT INTO card_info VALUES (NULL, %s, %s, %s, %s, 0, %s)', (fullname, encrypted_card_no, exp_date, encrypted_cvv, uID))
        mysql.connection.commit()
        return 0

def readCards(uID):
    print(type(uID))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM card_info WHERE user_id = %s', (uID,))
    cList = cursor.fetchall()
    cList = list(cList)
    print(cList)

    # file = open(f'_card.key', 'rb')
    # key = file.read()
    # print(key)
    # file.close()
    # f = Fernet(key)
    dList = []
    for filename in os.listdir():
        if filename.endswith('_card.key') and filename.__contains__(str(uID)):
            dList.append(filename)
    dList.sort()
    j = 0
    # for a in os.listdir():
    for i in range(len(cList)):
        encrypted_card = cList[i]['card_num'].encode()
        for d in dList:
            file = open(d, 'rb')
            key = file.read()
            file.close()
            f = Fernet(key)
            try:
                decrypted_card = f.decrypt(encrypted_card)
                cList[i]['card_num'] = decrypted_card.decode()
            except:
                continue
        # cList[j]['card_num'] = i['card_num']

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
    try:
        uNum = int(uCheck['rate_limit'])
    except TypeError:
        uNum = 0
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
    cursor = mysql.connect.cursor(MySQLdb.cursors.DictCursor)
    key = Fernet.generate_key()
    cursor.execute("SELECT * FROM card_info WHERE user_id = %s", (uID,))

    with open('symmetric_card.key', 'wb') as fo:
        fo.write(key)
    f = Fernet(key)

    cursor.execute('SELECT * FROM card_info WHERE card_num = %s', (cnum,))
    dupe = cursor.fetchone()
    decrypted_card = None
    try:
        c_num = dupe['card_num'].encode()
        decrypted_card = c_num.decode()
    except TypeError:
        decrypted_card = 0