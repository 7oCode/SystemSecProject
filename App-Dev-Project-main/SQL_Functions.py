from flask import Flask, render_template, request, redirect, url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
app = Flask(__name__)
mysql = MySQL(app)


# Enter database connection details
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_DB'] = 'pythonlogin'


"""Login, Register, Feedback, Card Creation and Updating, Purchases
Possible: 
User credential changes
Card credential changes
"""

def SQL_Register(username, password, email):
     # if username.isalpha() == False:
     #
     # cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    pass

