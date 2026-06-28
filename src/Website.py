# Flask template from https://stackoverflow.com/questions/33396064/flask-template-not-found

from flask import Flask, render_template, request
from json import dumps

from Helpers import checkFileName, formatKey, getValidSongs, useNextSunday


VALID_SONGS = dumps({"songs": [""] + getValidSongs()})

app = Flask(__name__, template_folder='website')


@app.route("/")
def main_page():
    return render_template("main.html", songs=VALID_SONGS,
                           filenameVal="", validFileName=1)


@app.route("/", methods=['POST'])
def process():
    songs, keys = [], []
    for i in range(4):
        if request.form[f"song{i}"].strip() and request.form[f"key{i}"].strip():
            songs.append(request.form[f"song{i}"])
            keys.append(formatKey(request.form[f"key{i}"]))
    filenameVal = useNextSunday() if "btn_Sun" in request.form else request.form["filename"]
    return render_template("main.html", songs=VALID_SONGS, filenameVal=filenameVal,
                           validFileName=int(checkFileName(filenameVal)))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
