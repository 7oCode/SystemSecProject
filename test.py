# import MySQLdb.cursors
# from Login import *
from flask import *

from flask_mysqldb import MySQL
# from cryptography.fernet import Fernet
# from flask_bcrypt import Bcrypt
#
import MySQLdb.cursors
#
app = Flask(__name__)
# # bcrypt = Bcrypt()
#
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_DB'] = 'sys_sec'
mysql = MySQL(app)
# #
# # def sql():
# #     username = 'Default'
# #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# #     cursor.execute("SELECT * FROM users WHERE username = %s",(username))
# #     check = cursor.fetchone()
# #     return check
# #
# # print(sql())
# j = '0'
# b = int(j)
# print(type(b))
# b += 1
# c = str(b)
# print(type(c), c)
#
# cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# cursor.execute("UPDATE card_info SET budget = 1000 WHERE fullname = 'Jeff Card'")
# mysql.connection.commit()
# a = 1
# if a:
#     print('y')
# else:
#     print('n')
# s = '50'
# b=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
# b.execute('SELECT * FROM card_info WHERE user_id = %s', (s,))
# a = b.fetchone()
# print(a)