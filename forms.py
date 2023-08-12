from wtforms import StringField, PasswordField,validators,IntegerField, TextAreaField, SelectField, FileField, ValidationError
from wtforms.validators import InputRequired, Length, Regexp
from flask_wtf import FlaskForm, RecaptchaField
from flask_mysqldb import MySQL
from Login1 import *
from SQL_Functions import *

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_DB'] = 'sys_sec'
mysql = MySQL(app)

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('Username required'),
                                                   Length(min=5, max=10, message='5-10 characters')],
                           render_kw={"placeholder": "Username"})

    password = PasswordField('password', validators=[InputRequired('Password required'),
                                                     Regexp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'),
                                                     Length(min=8, max=20, message='At least 8 characters')],
                             render_kw={"placeholder": "Password"})


    phone = StringField('phone', validators=[InputRequired('Phone number required'),
                                             Length(min=8, max=15, message='Valid number please'),
                                             Regexp(r'^\+65[89]\d*$')], render_kw={"placeholder": "Phone Number"})
    secquestions = [("Q1: Will I play Genshin Impact?"), ("Q2: What is 2+2?")]
    securityquestions = SelectField("Select a question", choices=secquestions, validators=[InputRequired()])

    s_ans = StringField('answer', validators=[InputRequired('Answer required'),
                                                   ],
                           render_kw={"placeholder": "Answer"})

    recaptcha = RecaptchaField()


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('Username required'),
                                                   Length(min=5, max=10, message='5-10 characters'),
                                                   ],render_kw={"placeholder": "Username"})

    password = PasswordField('password', validators=[InputRequired('Password required'),
                                                     Length(min=8, max=20,)],
                             render_kw={"placeholder": "Password"})

    # recaptcha = RecaptchaField()


class RegisterCard(FlaskForm):
    fname = StringField('fname', validators=[InputRequired('First Name required'),
                                             Length(min=4, max=20, message='Proper name please'),
                                             Regexp(r'^[a-zA-Z]+$')], render_kw={'placeholder': 'First Name'})

    lname = StringField('fname', validators=[InputRequired('Last Name required'),
                                             Length(min=4, max=20, message='Proper name please'),
                                             Regexp(r'^[a-zA-Z]+$')], render_kw={'placeholder': 'Last Name'})

    exp_date = StringField('exp_date', validators=[InputRequired('Expiry date required'),
                                                   Length(min=7, max=7, message='YYYY/MM Format'),
                                                   Regexp(r'^20[0-3][0-9]/(0[1-9]|1[0-2])$')],
                           render_kw={'placeholder': 'YYYY/MM'})

    cvv = StringField('cvv', validators=[InputRequired('CVV Required'), Length(min=3, max=3, message='CVV'),
                                         Regexp(r'^\d+$')], render_kw={'placeholder': 'CVV'})

    card_num = StringField('card_num', validators=[InputRequired('Card number required'),
                                                   Length(min=16,max=16, message='Valid number please'),
                                                   Regexp(r'^\d+$')], render_kw={'placeholder': 'Card Number'})


class UpdateCard(FlaskForm):
    card_num = StringField('card_num', validators=[InputRequired('Card number required'),
                                                   Length(min=16,max=16, message='Valid number please'),
                                                   Regexp(r'^\d+$')], render_kw={'placeholder': 'Card Number'})

    card_val = StringField('card_val', validators=[InputRequired('Budget needed'),
                                                   Length(min=1, max=4, message='Max 9999 budget'),
                                                   Regexp(r'^\d+$')], render_kw= {'placeholder': 'Value'})


class forgetPassword(FlaskForm):
    email = StringField('email', validators=[InputRequired('Email Required'),
                                           Length(min=4, max=20), Regexp(r'^(?!.*@mymail\.nyp\.edu\.sg).*@.*$')],
                        render_kw={"placeholder": "Email"})
    # Regexp(r'^(?!.*@mymail\.nyp\.edu\.sg).*@.*$')
    username = StringField('username', validators=[InputRequired('Username required'),
                                                   Length(min=5, max=10, message='5-10 characters'),
                                                   ],render_kw={"placeholder": "Username"})




class changePassword(FlaskForm):
    npassword = PasswordField('npassword', validators=[InputRequired('New password Required'), Length(min=8, max=20),
                                                       Regexp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')],
                           render_kw={'placeholder': 'New Password'})

    opassword = PasswordField('opassword', validators=[InputRequired('Old password Required'), Length(min=8, max=20),
                                                       Regexp(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')],
                           render_kw={'placeholder': 'Old Password'})

    # Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]+$")

    # secquestions = [("Q1: Will I play Genshin Impact?"), ("Q2: What is 2+2?")]
    # securityquestions = SelectField("Select a question", choices=secquestions, validators=[InputRequired()])
    securityquestion = StringField('question', render_kw={'readonly': True, "style": "width: 350px"})

    s_ans = StringField('answer', validators=[InputRequired('Answer required')],
                        render_kw={"placeholder": "Answer"})

class newTransaction(FlaskForm):
    card_num = StringField('card_num', validators=[InputRequired('Card number required'),
                                                   Length(min=16,max=16, message='Valid number please'),
                                                   Regexp(r'^\d+$')], render_kw={'placeholder': 'Card Number'})

    transaction = TextAreaField("transaction", validators=[InputRequired('Enter Transaction'), Length(min=4, max=100, message="Too short")],
                                render_kw={"placeholder" : "Enter transaction here"})

    cost = StringField("cost", validators=[InputRequired('Enter cost'), Length(min=1, max=4, message='Only numbers allowed'),
                                           Regexp(r'^\d+$')],
                        render_kw={"placeholder": "Cost"})



ALLOWED_EXTENSIONS = {'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class UploadForm(FlaskForm):
    pdf_file = FileField('Upload docx File')

    def validate_pdf_file(self, field):
        if not allowed_file(field.data):
            raise ValidationError('Only docx files are allowed.')


# Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]+$")