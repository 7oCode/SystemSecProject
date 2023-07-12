from flask import Flask, render_template, request, session, redirect, url_for
from config import CLIENT_SECRET, TOKEN, REDIRECT_URI, OAUTH_URL
from zenora import APIClient


app = Flask(__name__)
app.config["SECRET_KEY"] = 'verysecret'
client = APIClient(TOKEN, client_secret=CLIENT_SECRET)


@app.route("/")
def home():
    if 'token' in session:
        bearer_client = APIClient(session.get('token'), bearer=True)
        current_user = bearer_client.users.get_current_user()
        return render_template('index.html', current_user=current_user)

    return render_template("index.html", oauth_uri=OAUTH_URL)

@app.route("/oauth/callback")
def callback():
    code = request.args['code']
    access_token = oauth_response = client.oauth.get_access_token(code, REDIRECT_URI).access_token
    session['token'] = access_token
    return redirect('/')

    return oauth_response.access_token


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
