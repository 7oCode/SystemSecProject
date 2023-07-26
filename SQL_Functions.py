import MySQLdb.cursors

from Login import *
from flask_mysqldb import MySQL
from flask import Flask, session
from cryptography.fernet import Fernet
from flask_bcrypt import Bcrypt

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

        cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s, 0)', (username, hashpwd, encrypted_email, phone,))
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
        return 0
    else:
        print('Pass no match')
        return 2
#login done

# cvv must be encrypted
#assumption: Person -> Cards
#               1..1     1..*
def SQL_registerCard(card_no, fname, lname, exp_date, cvv, userID):
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

        cursor.execute('INSERT INTO card_info VALUES (NULL, %s, %s, %s, %s, 0, %s)', (fullname, encrypted_card_no, exp_date, encrypted_cvv, str(userID)))
        mysql.connection.commit()
        return 0

def readCards():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM card_info')
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

def SQL_update_card(cnum, cval, uID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM card_info WHERE card_num = %s", (cnum,))
    dCheck = cursor.fetchone
    if dCheck:
        file = open('symmetric_card.key','rb')
        key = file.read()
        file.close()
        f = Fernet(key)
        update = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        update.execute("UPDATE card_info SET budget = %s WHERE user_id = %s AND card_num = %s", (cval, uID, cnum,))
        print(update.fetchone())
        mysql.connection.commit()
        return 0
    else:
        return 1

