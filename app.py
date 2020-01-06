#git push heroku +HEAD:master
# https://blog.pythonanywhere.com/169/
# flask render_template insert html

from flask import Flask, render_template, redirect
import socket, subprocess
import lxmlparcer
#from flask import Markup

application = Flask(__name__)


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


hostname = get_ip_address()  # socket.gethostname()


@application.route("/")
def main():
    return render_template('base.html')


@application.route("/run")
def run():
    #import lxmlparcer
    #subprocess.call("lxmlparcer.py", shell = True)
    #please = output_in_var # Markup(output_in_var)
    scalpingresult = lxmlparcer.all()
    return render_template('result.html', please=scalpingresult) #output_in_var #


if __name__ == "__main__":
    application.env = "Working"
    application.debug = True
    application.run(host=hostname, port=5000)
