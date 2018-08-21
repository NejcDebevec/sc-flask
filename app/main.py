from flask import Flask, request, Response, redirect
import requests


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


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

