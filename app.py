from main import TPExtractor
from flask import Flask, request, render_template
import time

app = Flask(__name__) 

@app.route('/')
def input():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def input_post():
    URL = request.form['URL']
    pages = request.form['pages']
    outFile = request.form['outFile']
    TPExtractor(["dummy", URL, pages, outFile])
    message = '<br><br>Your File is Ready to <a href="' + outFile + '.pdf"> Download </a>'
    return render_template("index.html") + message

if __name__ == '__main__':
    app.run()