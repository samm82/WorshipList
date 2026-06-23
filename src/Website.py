# Flask template from https://stackoverflow.com/questions/33396064/flask-template-not-found

from flask import Flask, render_template, request

app = Flask(__name__, template_folder='website')

@app.route("/")
def welcome_page():
    return render_template("main.html")

@app.route("/file2", methods=['POST'])
def second_page():
    html_data = request.form["enter_value"]
    return render_template("file2.html", html_data=html_data)
# request form from id in html file

if __name__== '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)