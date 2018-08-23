from flask import Flask, request, Response, redirect
from flask_mail import Mail, Message
from flask_cors import CORS
import requests


app = Flask(__name__)
app.config['MAIL_SERVER'] = 'mail.fri.uni-lj.si'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
mail = Mail(app)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/mail/", methods=["POST"])
def send_mail():
    address = request.form.get('E-mail')
    subject = request.form.get('Subject')
    content = request.form.get('Message')
    msg = Message(subject, sender=address, recipients=['info@biolab.si'])
    msg.body = content
    mail.send(msg)
    return redirect("https://singlecell.biolab.si/contact/")


@app.route('/install/', methods=['GET'])
def download():
    os_download = request.args.get('os')
    url = ""
    r = requests.get("https://singlecell.biolab.si/download/files/filenames.set")
    versions = {}
    for line in r.iter_lines():
        key, value = str(line).split('=')
        os = key.split("'")[1]
        versions[os] = value.strip("\'")
    if os_download == 'mac':
        url = "https://singlecell.biolab.si/download/files/"
        url += versions['MACOS_BUNDLE']
    elif os_download == 'windows':
        url = "https://singlecell.biolab.si/download/files/"
        url += versions['WIN64_STANDALONE']

    return redirect(url)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5000)
# if __name__ == '__main__':

