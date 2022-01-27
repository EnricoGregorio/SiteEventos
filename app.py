from distutils.log import debug
from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)

app.secret_key = "t6723ew9r987sad34ty48t7"

@app.route('/')
def showHomePage():
    pageHome = render_template('index.html')
    return pageHome

@app.route('/cadastro')

if __name__ == "__app__":
    app.run(debug=True)
