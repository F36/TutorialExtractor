from urllib import request
from bs4 import BeautifulSoup
import json
import os
import sys
import pdfkit

class TPExtractor:

    def __init__(self, argsList):
        self.start = '<!-- Tutorial Content Starts Here -->'
        self.end = '<!-- Tutorial Content Ends Here -->'
        self.domain = 'https://www.tutorialspoint.com/'
        url = str(argsList[1])
        iters = int(argsList[2]) if len(argsList) > 2 else 1
        outFile = str(argsList[3]) if len(argsList) > 3 else 'out'
        for i in ['.html', '.pdf']:
            if os.path.exists(outFile + i):
                os.remove(outFile + i)
        self.addToHTML(url, iters, outFile)
    
    def getPDF(self, filename = 'out'):
        try:
            pdfkit.from_file(filename + '.html', filename + '.pdf')
        except Exception as e:
            print("Empty File Possible" + e)

    def getNext(self, content):
        try:
            soup = BeautifulSoup(content, 'html.parser')
            outerdiv = soup.find_all("div", attrs = {"id":"bottom_navigation"})
            innerdiv = [iter.find('div', attrs = {"class" : "nxt-btn"} ) for iter in outerdiv]
            nextURL = [iter.find('a')["href"] for iter in innerdiv]
            return self.domain + nextURL[-1]
        except Exception as E:
            print(E)
            return False

    def absoluteHREFs(self, content):
        return content

    def addToHTML(self, URL, iterations = 1, filename = 'out'):
        print(str(iterations) + " pages to go . . .")
        if iterations < 1:
            return self.getPDF(filename)
        req = request.urlopen(URL)
        html = req.read().decode('utf-8')
        content = html.split(self.start)[1].split(self.end)[0]
        content = self.absoluteHREFs(content)
        htmlFilename = filename + '.html'
        if os.path.exists(htmlFilename):
            fileOption = 'a'
        else:
            fileOption = 'w'
        
        f = open(htmlFilename, fileOption)
        f.write(content + '<hr><hr>')
        f.close()
        
        nextURL = self.getNext(content)
        if not nextURL:
            self.addToHTML(URL, iterations = 0, filename = filename)
        else:
            self.addToHTML(nextURL, iterations = iterations - 1, filename = filename)

#  TEST
if __name__ == '__main__':
    argsList = sys.argv
    TPExtractor(argsList)