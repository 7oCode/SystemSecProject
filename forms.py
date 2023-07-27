from wtforms import StringField, PasswordField,validators,IntegerField
from wtforms.validators import InputRequired, Length, Regexp
from flask_wtf import FlaskForm, RecaptchaField

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('Username required'),
                                                   Length(min=5, max=10, message='5-10 characters')],render_kw={"placeholder": "Username"})

    password = PasswordField('password', validators=[InputRequired('Password required'),
                                                     Length(min=8, max=20, message='At least 8 characters')],render_kw={"placeholder": "Password"})

    email = StringField('email', validators=[InputRequired('Email Required'),
                                              Length(min=4, max=20), Regexp(r'^(?!.*@mymail\.nyp\.edu\.sg).*@.*$')],render_kw={"placeholder": "Email"})
    phone = StringField('phone', validators=[InputRequired('Phone number required'),
                                             Length(min=8, max=15, message='Valid number please'),
                                             Regexp(r'^\+65[89]\d*$')], render_kw={"placeholder": "Phone Number"})

    recaptcha = RecaptchaField()


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired('Username required'),
                                                   Length(min=5, max=10, message='5-10 characters'),
                                                   ],render_kw={"placeholder": "Username"})

    password = PasswordField('password', validators=[InputRequired('Password required'),
                                                     Length(min=8, max=20,)],
                             render_kw={"placeholder": "Password"})

    recaptcha = RecaptchaField()


class RegisterCard(FlaskForm):
    fname = StringField('fname', validators=[InputRequired('First Name required'), Length(min=4, max=20, message='Proper name please'), Regexp(r'^[a-zA-Z]+$')], render_kw={'placeholder': 'First Name'})

    lname = StringField('fname', validators=[InputRequired('Last Name required'), Length(min=4, max=20, message='Proper name please'), Regexp(r'^[a-zA-Z]+$')], render_kw={'placeholder': 'Last Name'})

    exp_date = StringField('exp_date', validators=[InputRequired('Expiry date required'), Length(min=7, max=7, message='YYYY/MM Format'), Regexp(r'^20[0-3][0-9]/(0[1-9]|1[0-2])$')], render_kw={'placeholder': 'YYYY/MM'})
    cvv = StringField('cvv', validators=[InputRequired('CVV Required'), Length(min=3, max=3, message='CVV'), Regexp(r'^\d+$')], render_kw={'placeholder': 'CVV'})

    card_num = StringField('card_num', validators=[InputRequired('Card number required'), Length(min=16,max=16, message='Valid number please'),Regexp(r'^\d+$')], render_kw={'placeholder': 'Card Number'})


class UpdateCard(FlaskForm):
    card_num = StringField('card_num', validators=[InputRequired('Card number required'), Length(min=16,max=16, message='Valid number please'),Regexp(r'^\d+$')], render_kw={'placeholder': 'Card Number'})
    card_val = StringField('card_val', validators=[InputRequired('Budget needed'),Length(min=1, max=4, message='Max 9999 budget'),Regexp(r'^\d+$')], render_kw= {'placeholder': 'Value'})


class forgetPassword(FlaskForm):
    email = StringField('email', validators=[InputRequired('Email Required'),
                                           Length(min=4, max=20), Regexp(r'^(?!.*@mymail\.nyp\.edu\.sg).*@.*$')],render_kw={"placeholder": "Email"})


