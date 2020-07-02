from main import TPExtractor, Generic
from flask import Flask, request, render_template, send_file
import time
import os
import copy

app = Flask(__name__) 

@app.route('/')
def input():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def input_post():
    URL = request.form['URL']
    pages = request.form['pages']
    outFile = request.form['outFile']
    print(outFile)
    oF = copy.deepcopy(outFile)
    if 'tutorialspoint' in str(URL):
        TPExtractor(["dummy", URL, pages, oF]).main()
    else:
        Generic(["dummy", URL, pages, oF]).main()
    print(outFile)
    message = '<br><br>Your File is Ready to <a href="' + outFile + '"> Download </a>'
    return render_template("index.html") + message

@app.route('/<outFile>')
def getDownload(outFile) :
    try:
        files = [str(f) for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            print(f)
        if str(outFile + '.pdf') in files:
            return send_file(filename_or_fp = str(outFile + '.pdf'), as_attachment=True), None
        return send_file(filename_or_fp = str(outFile + '.html'), as_attachment=True), None
    except Exception as E:
        print(E)
        return 'Error'

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=False)