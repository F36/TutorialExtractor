from main import TPExtractor
from flask import Flask, request, render_template, send_file
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
    message = '<br><br>Your File is Ready to <a href="./' + outFile + '"> Download </a>'
    return render_template("index.html") + message

@app.route('/<outFile>')
def getDownload(outFile) :
    try:
        return send_file(filename_or_fp = str('./' + outFile + '.pdf'), as_attachment=True)
    except Exception as E:
        print(E)

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)