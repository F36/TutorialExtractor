from urllib import request
from bs4 import BeautifulSoup
import json
import os
import pdfkit

class TPExtractor:
    def __init__(self):
        self.start = '<!-- Tutorial Content Starts Here -->'
        self.end = '<!-- Tutorial Content Ends Here -->'
        self.domain = 'https://www.tutorialspoint.com/'

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

    def addToHTML(self, URL, iterations = 1, filename = 'out'):
        if iterations < 1:
            return self.getPDF(filename)
            
        req = request.urlopen(URL)
        html = req.read().decode('utf-8')
        content = html.split(self.start)[1].split(self.end)[0]
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
    ob = TPExtractor()
    ob.addToHTML('https://www.tutorialspoint.com/data_structures_algorithms/index.htm', 3)
