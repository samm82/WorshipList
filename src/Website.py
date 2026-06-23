# Flask template from https://stackoverflow.com/questions/33396064/flask-template-not-found

from flask import Flask, render_template, request

from Helpers import checkFileName

app = Flask(__name__, template_folder='website')

@app.route("/")
def main_page():
    return render_template("main.html", filenameVal="", validFileName=1)

@app.route("/", methods=['POST'])
def process_filename():
    # request form from id in html file
    filenameVal = request.form["filename"]
    return render_template("main.html", filenameVal=filenameVal,
                           validFileName=int(checkFileName(filenameVal)))

if __name__== '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
