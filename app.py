from main import TPExtractor
from flask import Flask, request, render_template

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
    return 'OK'

if __name__ == '__main__':
    app.run()