#git push heroku +HEAD:master
# https://blog.pythonanywhere.com/169/
# flask render_template insert html

from flask import Flask, render_template, redirect, url_for, request, session
from flask import Flask, flash, redirect, render_template, request, session, abort
import socket, subprocess
import lxmlparcer
import os
#from flask import Markup

app = Flask(__name__, template_folder="templates")


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


hostname = get_ip_address()  # socket.gethostname()


@app.route("/home")
def home():
    return render_template('base.html')


@app.route("/run")
def run():
    #import lxmlparcer
    #subprocess.call("lxmlparcer.py", shell = True)
    #please = output_in_var # Markup(output_in_var)
    scalpingresult = lxmlparcer.all()
    return render_template('result.html', please=scalpingresult) #output_in_var #

# Route for handling the login page logic
'''@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            #session['key'] = login(request.form.get('username'), request.form.get('password'))
            return redirect(url_for("home"))
    return render_template('login.html', error=error)'''


@app.before_request
def _check_user_login():
    if not request.path.startswith('/static/') and \
            not request.path in ['/urls', '/that', '/do', '/not', '/require', '/login','/']:
        if not 'key' in session:
            return redirect(url_for('login'))

@app.route('/')
def login():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return home()


@app.route('/login', methods=['POST'])      # https://pythonspot.com/login-authentication-with-flask/
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        session['key'] = (request.form.get('username'), request.form.get('password'))
        # session['key'] = do_admin_login(request.form.get('username'), request.form.get('password')) # ???
    else:
        flash('wrong password!')
    return login()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


# app name
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
# defining function
    message = "You was redirected to home because of faulty request (404) <br>"
    return render_template('base.html', message = message)


if __name__ == "__main__":
    app.env = "Working"
    app.debug = True
    app.secret_key = os.urandom(12)
    app.run(host=hostname, port=5000)
