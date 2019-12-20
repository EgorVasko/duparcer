from flask import Flask, render_template

application = Flask(__name__)


@application.route("/")
def main():
    return "<a href = 'run'>Run program</a><br>" \
           "<a href = 'result'>Result</a><br>"


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
    application.run()
