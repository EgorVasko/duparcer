from flask import Flask, render_template, redirect
import socket, subprocess

application = Flask(__name__)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


hostname = get_ip_address()  # socket.gethostname()


@application.route("/")
def main():
    return redirect("/result", code=302)


@application.route("/run")
def run():
    #import lxmlparcer
    subprocess.call("lxmlparcer.py", shell = True)
    return redirect("/result-var", code=302)


@application.route('/result')
def result():
    return render_template('result.html')


@application.route('/result-var')
def result_var():
    from lxmlparcer import output_in_var
    please = output_in_var
    print(please[:100], type(please))
    return render_template('result.html', please=please) # output_in_var #


if __name__ == "__main__":
    application.env = "Working"
    application.debug = True
    application.run(host=hostname, port=5000)
