from collections import defaultdict
import math
class Searcher():

    def __init__(self):
        self.result = []
        self.result_path = "data"
        self.corpus_size = 37497


    def searchFiles(self, searchTerm):
        file_name = "{}/{}".format(self.result_path, searchTerm[0])

        file = open(file_name).read()

        data = eval(file.replace("<class 'list'>", 'list'))

        self.calculateTFIDF(data[searchTerm])

        data[searchTerm] = sorted(data[searchTerm], key = lambda tup: tup[2], reverse=True)

        for doc in data[searchTerm]:
            print(doc[0], doc[2])





    def calculateTFIDF(self, posting):
        # Calculates the tf-idf for a given posting of a term and updates the posting
        idf = math.log(self.corpus_size/len(posting))

        for doc in posting:
            tf = 1 + math.log(doc[1])
            tf_idf = round(tf * idf, 5)
            doc[2] = tf_idf







if __name__ == '__main__':
    searcher = Searcher()

    searcher.searchFiles('information')

