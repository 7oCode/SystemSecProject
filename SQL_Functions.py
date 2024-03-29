import os
# current sql function file
import MySQLdb.cursors

# from Login1 import *
from flask_mysqldb import MySQL
from flask import Flask, session
from cryptography.fernet import Fernet
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from datetime import datetime

app = Flask(__name__)
bcrypt = Bcrypt()
s = URLSafeTimedSerializer('Thisisasecret!')


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_DB'] = 'sys_sec'
mysql = MySQL(app)

#create audit log function
def add_audit_log(log_message, log_type):
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO audit_logs VALUES (NULL, %s, %s)', (log_message, log_type,))
    mysql.connection.commit()
    cursor.close()


def SQL_Register(username, password, email, phone, squest,s_ans):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
    dupe = cursor.fetchone()
    cursor.execute("SELECT email FROM users")
    eList = cursor.fetchall()
    eList = list(eList)
    dList = []
    for filename in os.listdir():
        if filename.endswith('.key') and filename.__contains__(username):
            dList.append(filename)

    dList.sort()
    for i in range(len(eList)):
        en_email = eList[i]['email'].encode()
        for d in dList:
            file = open(d,'rb')
            key = file.read()
            file.close()
            f = Fernet(key)
            try:
                de_email = f.decrypt(en_email)
                eList[i]['email'] = de_email.decode()
            except:
                continue


    print(dupe)
    if dupe or (username in eList):
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

        cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s, %s, 0, 0, 0, %s, %s)', (username, hashpwd, encrypted_email, phone, squest, s_ans))
        # cursor.execute('INSERT INTO users (username, password, email, phone, column1, column2) VALUES (%s, %s, %s, %s, 0, 0)',(username, hashpwd, encrypted_email, phone,))

        mysql.connection.commit()

        # Add a log entry for successful registration
        now = datetime.now()
        date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"Successful Registration for user '{username}' via username/password at time: {date_time_str}"
        # log_message = f"Successful registration for user {username} at time: {date_time_str}"
        add_audit_log(log_message, 'register')
        
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
        # print("TypeError Login")
        return 1
# '''
#             d = 'Default'
#             d_s = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#             d_s.execute("SELECT * FROM users WHERE username = %s", (d,))
#             d_check = d_s.fetchone()
#             d_num = int(d_check['rate_limit'])
#             if d_num < 3:
#                 d_num += 1
#                 d_s.execute("UPDATE users SET rate_limit = %s WHERE username = %s", (str(d_num), d,))
#                 return 1
#             else:
#                 d_s.execute("UPDATE users SET rate_limit = '0' WHERE username = %s", (d,))
#                 return 2
# '''
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

        # Add a log entry for successful login
        now = datetime.now()
        date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"Successful Login for user '{username}' via username/password at time: {date_time_str}"
        # log_message = f"Successful login for user {username} at time: {date_time_str}"
        add_audit_log(log_message, 'login')

        return 0
    else:
        print('Pass no match')

        # Add a log entry for unsuccessful login
        now = datetime.now()
        date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"Unsuccessful Login for user '{username}' via username/password at time: {date_time_str}"
        # log_message = f"Unsuccessful login for user {username} at time: {date_time_str}"
        add_audit_log(log_message, 'login')

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
    # print(dupe)
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
            if filename.endswith('_card.key') and filename.__contains__(uID):
                cList.append(filename)
        print(cList)


        n = 1
        for newcard in cList:
            n += 1
        print(n)

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
    cursor.execute('SELECT fullname, card_num,exp_date, budget FROM card_info WHERE user_id = %s', (uID,))
    cList = cursor.fetchall()
    cList = list(cList)

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
    print(cList)
    return cList

def SQL_rate_limit_def():
    d = 'Default'
    d_s = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    d_s.execute("SELECT rate_limit FROM users WHERE username = %s", (d,))
    d_check = d_s.fetchone()
    # print(d_check)
    d_num = int(d_check['rate_limit'])

    if d_num < 2:
        d_num += 1
        ds = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        ds.execute("UPDATE users SET rate_limit = %s WHERE username = %s", (str(d_num), d,))
        ds.execute("SELECT rate_limit FROM users WHERE username = %s", (d,))
        nCheck = ds.fetchone()
        mysql.connection.commit()
        print(nCheck)
        print('return 1')
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
    if uNum < 2:
        uNum += 1
        uNum = str(uNum)
        uS = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        uS.execute("UPDATE users SET rate_limit = %s WHERE username = %s", (uNum, username,))
        uS.execute("SELECT * FROM users WHERE username = %s", (username,))
        uCheck = uS.fetchone()
        mysql.connection.commit()
        return 1
    else:
        cursor.execute("UPDATE users SET rate_limit = '0' WHERE username = %s", (username,))
        mysql.connection.commit()
        return 2

def SQL_IrfanEmail(email):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users where username = %s", (euser,))
    eList = cursor.fetchone()
    if eList is None:
        return 1
    # eList = list(eList)
    # print(eList)
    dList = []
    # d = 0
    for filename in os.listdir():
        if filename.endswith('.key') and filename.__contains__(euser):
            dList.append(filename)
        # d += 1

    dList.sort()
    # print(dList)
    pList = []
    ddList = []

    en_email = eList['email'].encode()
    file = open(f'{euser}.key', "rb")
    key = file.read()
    file.close()
    f = Fernet(key)
    try:
        pe_email = eList['email']
        de_email = f.decrypt((en_email))
        eList['email'] = de_email.decode()
    except:
        return 1


def SQL_Check_Email(email,euser):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users where username = %s", (euser,))
    eList = cursor.fetchone()
    if eList is None:
        return 1
    # eList = list(eList)
    # print(eList)
    dList = []
    # d = 0
    for filename in os.listdir():
        if filename.endswith('.key') and filename.__contains__(euser):
            dList.append(filename)
        # d += 1

    dList.sort()
    # print(dList)
    pList = []
    ddList = []
    # for i in range(len(eList)):
    #     pList.append(eList['email'])

    #     for d in dList:
    #         file = open(d,'rb')
    #         key = file.read()
    #         file.close()
    #         f = Fernet(key)
    #         try:
    #             de_email = f.decrypt(en_email)
    #             eList[i]['email'] = de_email.decode()
    #             ddList.append(eList[i]['email'])
    #         except:
    #             continue
    en_email = eList['email'].encode()
    file = open(f'{euser}.key', "rb")
    key = file.read()
    file.close()
    f=Fernet(key)
    try:
        pe_email = eList['email']
        de_email = f.decrypt((en_email))
        eList['email'] = de_email.decode()
    except:
        return 1

    # print(eList)



    # cursor.execute("SELECT * FROM users WHERE email = %s and username = %s", (pe_email, euser,))
    # user = cursor.fetchone()
    # cursor.close()

    if eList['email'] == email:
        # # Email exists in the database
        # # Generate a time-limited token for email verification
        # token = s.dumps(email, salt='email-confirm')
        #
        # # Create a message with the verification link and send it via email
        # v_msg = Message('Confirm Email', sender='mohd.irfan.khan.9383@gmail.com', recipients=[email])  # Replace with your Gmail email
        # link = url_for('confirm_email1', token=token, _external=True)
        # v_msg.body = f'To reset your password, click the link: {link}. The link will expire in 3 minutes. Thank You!'
        # mail.send(v_msg)
        #
        # # Store the email in the session for further processing
        # session['email'] = email
        return 0
    else:
        # Email does not exist in the database
        return 1

def SQL_update_card(cnum, cval, uID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    key = Fernet.generate_key()
    cursor.execute("SELECT * FROM card_info WHERE user_id = %s", (uID,))
    cardList = cursor.fetchall()
    cardList = list(cardList)
    cList = []
    for filename in os.listdir():
        if filename.endswith('_card.key') and filename.__contains__(uID):
            cList.append(filename)


    for i in range(len(cardList)):
        encrypted_card = cardList[i]['card_num'].encode()
        for cardkey in cList:
            file = open(cardkey, 'rb')
            key = file.read()
            file.close()
            f = Fernet(key)
            try:
                decrypted_card = f.decrypt(encrypted_card)
                if decrypted_card.decode() == cnum:
                    cursor.execute("UPDATE card_info SET budget = %s WHERE card_num = %s AND user_id = %s",
                                   (cval, str(cardList[i]['card_num']), uID,))
                    mysql.connection.commit()
                    return 0
            except Exception as e:
                print(f"Error: {e}")
                continue


def SQL_RegisterGoogleUser(google_id, name, email, phone):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO users (google_id, username, password, email, phone_no) VALUES (%s, %s, %s, %s, %s)",
                   (google_id, name, "", email, phone))
    mysql.connection.commit()
    cursor.close()


def SQL_UpdatePasswordAndPhone(user_id, password, phone):
    cursor = mysql.connection.cursor()
    hashpwd = bcrypt.generate_password_hash(password)
    cursor.execute("UPDATE users SET password = %s, phone_no = %s WHERE id = %s", (hashpwd, phone, user_id))
    mysql.connection.commit()
    cursor.close()

def SQL_Update_Password(user,npass, sans):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE username = %s', (user,))
    uchange = cursor.fetchone()
    print(uchange)


    if uchange['securityanswer'] == sans:
        hashpwd = bcrypt.generate_password_hash(npass)
        cursor.execute("UPDATE users SET password = %s WHERE username = %s", (hashpwd,user,))
        mysql.connection.commit()
        cursor.execute('SELECT password FROM users WHERE username = %s', (user,))
        uUpdate = cursor.fetchone()
        print(uUpdate)
        print('epic style')
        return 0
    else:
        print("Error")
        return 1


def SQL_Check_User(username):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    ucheck = cursor.fetchone()

    if ucheck:
        nrate = '3'
        cursor.execute('UPDATE users SET rate_limit = %s WHERE username = %s', (nrate, username,))
        mysql.connection.commit()
        return 0
    else:
        print("Error")
        return 1

def check_ratelimit(username):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT rate_limit FROM users WHERE username = %s', (username,))
    getrate = cursor.fetchone()
    grate = int(getrate['rate_limit'])
    print(grate)
    return grate

def SQL_New_Transaction(cnum, trans, cost,uID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * from card_info where user_id = %s", (uID,))
    tcheck = cursor.fetchall()
    tcheck = list(tcheck)
    print(tcheck)

    dList = []
    for filename in os.listdir():
        if filename.endswith('_card.key') and filename.__contains__(str(uID)):
            dList.append(filename)
    dList.sort()

    for i in range(len(tcheck)):
        encrypted_card = tcheck[i]['card_num'].encode()
        for d in dList:
            file = open(d, 'rb')
            key = file.read()
            file.close()
            f = Fernet(key)
            try:
                decrypted_card = f.decrypt(encrypted_card)
                tcheck[i]['card_num'] = decrypted_card.decode()
            except:
                continue

    card_in = False
    for card in range(len(tcheck)):
        if cnum == tcheck[card]['card_num']:
            card_in = True
            cursor.execute('INSERT INTO transactions VALUES (NULL, %s, %s, %s, %s)', (cnum, cost, trans, uID,))
            mysql.connection.commit()
            return 0

    if card_in is False:
        return 1

def transactions(uID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT transaction, cost, card_num FROM transactions WHERE user_id = %s', (uID,))
    cList = cursor.fetchall()
    cList = list(cList)
    print(cList)
    return cList

def question(uID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT securityquestion FROM users WHERE username = %s", (uID,))
    ucheck = cursor.fetchone()
    uquest = ucheck['securityquestion']
    return uquest
