# import MySQLdb.cursors
# from Login import *
import os

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
# a = [{'card_ID': 13, 'fullname': 'Jeff Cardd',
#       'card_num': 'gAAAAABkwm984dh3VEU44MkjNU1rVxQfTslPh2yWcABm5WjTa_YT116g2XFlFKgFGo9kuPDBs0y-pqeciAj7zsv9Cjt2-sauUsV2P-gF3PCjOxka4JsXRJM=',
#       'exp_date': '2025/11', 'cvv': 'gAAAAABkwm98T8ylEZx6RZkZZkpCmVk2S2tBGIlLGRWI5Mhaes7LxfPcIpV7i8-jDbkXVeCH8Z6NAO6NUuxK2qsNplXdP7wTzA==', 'budget': '0', 'user_id': '50'},
#      {'card_ID': 14, 'fullname': 'Jeff Neww', 'card_num': 'gAAAAABkwm-dMv04U0QNw4kagPWxzBedqSqTf3aHmal_WP-cGL1yPwSEFZToyj02pe2fVfXe4IHU8KXUJIbXsiPK0em6LJ4POlwjOWuWbOmYBWRmIY2Ze7U=',
#       'exp_date': '2025/05', 'cvv': 'gAAAAABkwm-dSmPLJfQTUxBb86Hey3reXsqqkD0dLgXdCBPygV7KHvhe7qDEhO96zD9HPeiHnMZ7jG22NRI2g6U6oKHreI2ZNg==', 'budget': '0', 'user_id': '50'}]
#
# for i in a:
#     print(i['card_num'])
# d = 'hello'
# print(d.index('l'))
#
# a = {}
# a.items()
a = ['symmetric1u.key', 'symmetric2u.key']
a.sort()
c = a[0]
print(c.__contains__('metric'))