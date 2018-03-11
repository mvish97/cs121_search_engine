from pathlib import Path
import os
from bs4 import BeautifulSoup
from collections import defaultdict
import nltk
from nltk.corpus import stopwords
from string import ascii_lowercase
import math

class Parser:

    def __init__(self):
        self.html_path = "WEBPAGES_RAW/"
        self.result_path = "data"
        self.data = {}
        self.corpus_size = 0

        for alpha in ascii_lowercase:
            self.data[alpha] = defaultdict(list)
        for num in range(0, 10):
            self.data[str(num)] = defaultdict(list)

    def file_to_text(self, file_path):
        # takes in the html file path and return an open object if it can
        try:
            return open(file_path, "r")
        except:
            print("ERROR reading file at ", file_path)

    def read_all(self):
        counter1 = 0
        while Path(self.html_path + str(counter1)).exists():
            counter2 = 0
            while Path(self.html_path + str(counter1) + "/" + str(counter2)).exists():
                # print(counter1, counter2)
                processed_html = self.html_to_text(self.file_to_text(self.html_path + str(counter1) + "/" + str(counter2)))

                self.add_to_dictionary(self.tokenize_file(processed_html[0]), self.tokenize_file(processed_html[1]),
                                       "{}/{}".format(counter1, counter2))
                counter2 += 1
                self.corpus_size += 1

            print("FOLDER: {} and FILES: {}".format(counter1, counter2))

            counter1 += 1

    def html_to_text(self, open_file):
        # Takes an open file and returns the text from it
        soup = BeautifulSoup(open_file, 'html.parser')
        raw_text = ""
        weighted_text = ""

        for tag in ['b', 'h1', 'h2', 'h3', 'title', 'body', 'strong']:
            for text in soup.find_all(tag):
                if tag != "body":
                    weighted_text += text.getText().strip() + " "
                else:
                    raw_text += text.getText().strip() + " "

        # print(self.tokenize_file(weighted_text))
        return raw_text, weighted_text

    def tokenize_file(self, html_text):
        # Takes in html as a string and adds it to a dictionary from one file
        text = nltk.word_tokenize(html_text)
        result = defaultdict(int)
        stop_words = set(stopwords.words('english'))

        for word in text:
            if len(word) > 0 and (word.lower().isalpha() or word.lower().isnumeric()) and word not in stop_words:
                result[word.lower()] += 1

        return result

    def add_to_dictionary(self, token_dict_raw, token_dict_weighted, file_id):
        # Adds the file tokens to the main dictionary
        for k, v in token_dict_raw.items():

            if k[0] in self.data:
                self.data[k[0]][k].append([file_id, v, 0, 0])

        for k, v in token_dict_weighted.items():
            if k[0] in self.data:
                if k in self.data[k[0]] and len(self.data[k[0]][k]) != 0 and self.data[k[0]][k][-1][0] == file_id:
                    self.data[k[0]][k][-1][2] = v
                else:
                    self.data[k[0]][k].append([file_id, 0, v, 0])

    def write_file(self):
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)
        for k, v in self.data.items():
            if os.path.exists(self.result_path + "/" + str(k)):
                os.remove(self.result_path + "/" + str(k))
            fh = open(self.result_path + "/" + str(k), "w")
            fh.write(str(v))
            fh.close()

    def calculate_tfidf(self):
        # Calculates the tf-idf for a given posting of a term and updates the posting
        for alpha, words in self.data.items():
            print("Calculating tf-idf for {}".format(alpha))
            for word, posting in words.items():
                idf = math.log(self.corpus_size/len(posting))

                for doc in posting:
                    # TF calculated with the word frequency and weighted word frequency bumped up 1.2 times
                    tf = 1 + math.log(doc[1] + (doc[2]*1.2))
                    tf_idf = round(tf * idf, 5)
                    doc[3] = tf_idf

if __name__ == '__main__':
    r = Parser()
    r.read_all()
    r.calculate_tfidf()
    r.write_file()

    # processed_html = r.html_to_text(r.file_to_text("WEBPAGES_RAW/0/6"))
    #
    # r.add_to_dictionary(r.tokenize_file(processed_html[0]), r.tokenize_file(processed_html[1]),
    #                        "{}/{}".format(0, 6))
    # r.corpus_size = 37000
    # r.calculate_tfidf()
    # for k, v in r.data.items():
    #     print(k, v)
    #print(r.tokenize_file((r.html_to_text(r.file_to_text("WEBPAGES_RAW/0/6")))))




