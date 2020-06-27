from urllib import request
from bs4 import BeautifulSoup
import json
import os

class TPExtractor:
    def __init__(self):
        self.start = '<!-- Tutorial Content Starts Here -->'
        self.end = '<!-- Tutorial Content Ends Here -->'
        self.sep = 'hr{ border: 1px dashed #000; width: 50%; margin: auto; margin-top: 5%; margin-bottom: 5%; }>'
    def TutorialsPoint(self, URL, iterations = 1, filename = 'out'):
        if iterations < 1:
            return
        req = request.urlopen(URL)
        html = req.read().decode('utf-8')
        content = html.split(self.start)[1].split(self.end)[0]
        filename += '.html'
        if os.path.exists(filename):
            fileOption = 'a'
        else:
            fileOption = 'w'
            content = self.sep + content
        
        f = open(filename, fileOption)
        f.write(content + '<hr>')
        f.close()

#  TEST
# if __name__ == '__main__':
#     ob = TPExtractor()
#     ob.TutorialsPoint('https://www.tutorialspoint.com/data_structures_algorithms/index.htm')
