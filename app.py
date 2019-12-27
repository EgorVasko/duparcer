from flask import Flask, render_template
import socket

application = Flask(__name__)


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


hostname = get_ip_address()  # socket.gethostname()


@application.route("/")
def main():
    return "<h2><a href = 'run'>Run program</a></h2><br>" \
           "<h2><a href = 'result'>Result</a></h2><br>"


@application.route("/run")
def run():
    import lxmlparcer
    return "<a href = 'result'>Result</a>"


@application.route('/result')
def result():
    return render_template('result.html')


if __name__ == "__main__":
    application.env = "Working"
    application.debug = True
    application.run(host=hostname, port=5000)
