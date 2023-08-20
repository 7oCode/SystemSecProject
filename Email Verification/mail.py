from flask import *
from flask_mail import Mail, Message
from random import *
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
app = Flask(__name__)

app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'mohd.irfan.khan.9383@gmail.com'
app.config['MAIL_PASSWORD'] = 'cljfueogsjrjrbya'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
s = URLSafeTimedSerializer('Thisisasecret!')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    email = request.form['email']
    token = s.dumps(email, salt='email-confirm')

    msg = Message('Confirm Email', sender='mohd.irfan.khan.9383@gmail.com', recipients=[email])

    link = url_for('confirm_email', token=token, _external=True)

    msg.body = 'To confirm your email, click the link {} . The link will expire in 3 minutes! Thank You'.format(link)

    mail.send(msg)

    return render_template('thanks.html')

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=10)
    except SignatureExpired:
        return render_template('fail.html')
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=False)
