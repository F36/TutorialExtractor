from urllib import request
from bs4 import BeautifulSoup
import json
import os
import sys
import pdfkit
import subprocess
import platform 

class TPExtractor:

    def __init__(self, argsList):
        self.start = '<!-- Tutorial Content Starts Here -->'
        self.end = '<!-- Tutorial Content Ends Here -->'
        self.domain = 'https://www.tutorialspoint.com'
        url = str(argsList[1])
        iters = int(argsList[2]) if len(argsList) > 2 else 1
        outFile = str(argsList[3]) if len(argsList) > 3 else 'out'
        for i in ['.html', '.pdf']:
            if os.path.exists(outFile + i):
                os.remove(outFile + i)
        for file in os.scandir('.'):
            if file.name.endswith(".html") or file.name.endswith(".pdf"):
                os.unlink(file.path)
        self.addToHTML(url, iters, outFile)
    
    def getPDF(self, filename = 'out'):

        def _get_pdfkit_config():
            """wkhtmltopdf lives and functions differently depending on Windows or Linux. We
            need to support both since we develop on windows but deploy on Heroku.
            Returns: A pdfkit configuration"""
            if platform.system() == 'Windows':
                return pdfkit.configuration(wkhtmltopdf=os.environ.get('WKHTMLTOPDF_BINARY', 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'))
            else:
                WKHTMLTOPDF_CMD = subprocess.Popen(['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf')], stdout=subprocess.PIPE).communicate()[0].strip()
                return pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)

        try:
            if 'DYNO' in os.environ:
                print ('loading wkhtmltopdf path on heroku')
                WKHTMLTOPDF_CMD = subprocess.Popen(
                    ['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf-pack')], # Note we default to 'wkhtmltopdf' as the binary name
                    stdout=subprocess.PIPE).communicate()[0].strip()
                print("DYNO")
                pdfkit.from_file(filename + '.html', filename + '.pdf', configuration=_get_pdfkit_config())
            else:
                print ('loading wkhtmltopdf path on localhost')
                MYDIR = os.path.dirname(__file__)    
                WKHTMLTOPDF_CMD = os.path.join(MYDIR + "/static/executables/bin/", "wkhtmltopdf.exe")
                pdfkit.from_file(filename + '.html', filename + '.pdf', configuration=_get_pdfkit_config())
        except Exception as e:
            print("Empty File Possible" + str(e))

    def getNext(self, content):
        try:
            soup = BeautifulSoup(content, 'html.parser')
            outerdiv = soup.find_all("div", attrs = {"id":"bottom_navigation"})
            innerdiv = [iter.find('div', attrs = {"class" : "nxt-btn"} ) for iter in outerdiv]
            nextURL = [iter.find('a')["href"] for iter in innerdiv]
            return nextURL[-1]
        except Exception as E:
            print(E)
            return False

    def absoluteLinks(self, content):
        domain = self.domain
        soup = BeautifulSoup(content, 'html.parser')
        for hyperlink in soup.find_all(href=True):
            try:
                request.urlopen(hyperlink["href"])
            except :
                hyperlink["href"] = domain + hyperlink["href"]
        for hyperlink in soup.find_all(src=True):
            try:
                request.urlopen(hyperlink["src"])
            except :
                hyperlink["src"] = domain + hyperlink["src"]
        return str(soup)

    def addToHTML(self, URL, iterations = 1, filename = 'out'):
        print(str(iterations) + " pages to go . . .")
        if iterations < 1:
            return self.getPDF(filename)
        req = request.urlopen(URL)
        html = req.read().decode('utf-8')
        content = html.split(self.start)[1].split(self.end)[0]
        content = self.absoluteLinks(content)
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