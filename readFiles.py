from pathlib import Path
import os
from bs4 import BeautifulSoup
from collections import defaultdict
import nltk
from nltk.corpus import stopwords
from string import ascii_lowercase

class Parser:

    def __init__(self):
        self.html_path = "WEBPAGES_RAW/"
        self.data = {}

        for alpha in ascii_lowercase:
            self.data[alpha] = defaultdict(list)

    def file_to_text(self, file_path):
        # takes in the html file path and return an open object if it can
        try:
            return open(file_path, "r")
        except:
            print("ERROR reading file at ", file_path)

    def read_all(self):
        counter1 = 74
        while Path(self.html_path + str(counter1)).exists():
            counter2 = 496
            while Path(self.html_path + str(counter1) + "/" + str(counter2)).exists():
                # print(counter1, counter2)
                self.add_to_dictionary(self.tokenize_file(self.html_to_text(\
                    self.file_to_text(self.html_path + str(counter1) + "/" + str(counter2)))),\
                    "{}/{}".format(counter1, counter2))
                counter2 += 1
            counter1 += 1

    def html_to_text(self, open_file):
        # Takes an open file and returns the text from it
        soup = BeautifulSoup(open_file, 'html.parser')
        tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'br', 'title', 'P', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'BR', 'TITLE']
        raw_text = ""

        for tag in tags:
            for text in soup.find_all(tag):
                # print(text.getText())
                raw_text += text.getText().strip() + " "

        return raw_text

    def tokenize_file(self, html_text):
        # Takes in html as a string and adds it to a dictionary from one file
        text = nltk.word_tokenize(html_text)
        result = defaultdict(int)
        stop_words = set(stopwords.words('english'))

        for word in text:
            if len(word) > 0 and word[0].lower().isalpha() and word not in stop_words:
                result[word.lower()] += 1

        return result

    def add_to_dictionary(self, token_dict, file_id):
        # Adds the file tokens to the main dictionary
        for k, v in token_dict.items():
            self.data[k[0]][k].append((file_id, v, 0))

if __name__ == '__main__':

    r = Parser()
    r.read_all()
    print(r.data)
    # print(r.tokenize_file((r.html_to_text(r.file_to_text("WEBPAGES_RAW/74/496")))))




