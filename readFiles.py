from pathlib import Path
import os
from bs4 import BeautifulSoup
from collections import defaultdict
import nltk

class Parser:

    def __init__(self):
        self.html_path = "WEBPAGES_RAW/"
        self.data = defaultdict(int)

    def file_to_text(self, file_path):
        # takes in the html file path and return an open object if it can
        try:
            return open(file_path, "r")
        except:
            print("ERROR reading file at ", file_path)

    def read_all(self):
        # print(Path(path_to_html + str(i)))
        # print(os.getcwd())
        counter1 = 0
        while Path(self.html_path + str(counter1)).exists():
            counter2 = 0
            path = self.html_path + str(counter1) + "/" + str(counter2)
            while Path(path).exists():
                # print(counter1, counter2)
                self.file_to_text(path)
                counter2 += 1
            counter1 += 1

    def html_to_text(self, open_file):
        # Takes an open file and returns the text from it
        soup = BeautifulSoup(open_file, 'html.parser')
        tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title']
        raw_text = ""

        for tag in tags:
            for text in soup.find_all(tag):
                # print(text.getText())
                raw_text += text.getText().strip() + " "

        return raw_text

r = Parser()
# print(r.read_all())
print(nltk.word_tokenize(r.html_to_text(r.file_to_text("WEBPAGES_RAW/0/6"))))