from collections import defaultdict
import math
import json

class Searcher():

    def __init__(self):
        self.result = []
        self.result_path = "data"
        self.corpus_size = 37497
        self.bookkeeper = "WEBPAGES_CLEAN/" + "bookkeeping.json"
        self.local_dict = {}
        try:
            # The bookkeeping JSON object
            self.bookkeeping_obj = json.loads(open(self.bookkeeper).read())
        except:
            print("Error opening bookkeeping file, check path")
            return

    def get_data(self, search_term):
        if search_term[0] not in self.local_dict:
            file = open("{}/{}".format(self.result_path, search_term[0])).read()

            # Store the evaluated data in the local dictionary
            self.local_dict[search_term[0]] = eval(file.replace("<class 'list'>", 'list'))

        # Calculate tfidf for query
        self.calculate_tfidf(self.local_dict[search_term[0]][search_term])
        # Sort local dict
        self.local_dict[search_term[0]][search_term].sort(key=lambda tup: tup[2], reverse=True)
        # Return the values for the query
        return self.local_dict[search_term[0]][search_term]

    def calculate_tfidf(self, posting):
        # Calculates the tf-idf for a given posting of a term and updates the posting
        idf = math.log(self.corpus_size/len(posting))

        for doc in posting:
            tf = 1 + math.log(doc[1])
            tf_idf = round(tf * idf, 5)
            doc[2] = tf_idf

    def get_urls(self, queries):
        counter_urls = defaultdict(int)
        counter_word_count = defaultdict(int)
        for query in queries.strip().split():
            for d in self.get_data(query):
                counter_urls[d[0]] += 1
                counter_word_count[d[0]] += d[2]

        results = sorted(counter_urls.items(), key=lambda x: (-x[1], -counter_word_count[x[0]]))
        for i in range(5):
            print("{}. {}".format(i + 1, self.bookkeeping_obj[results[i][0]]))


if __name__ == '__main__':

    query = input("Enter your query (quit to end program): ")

    while(query != "quit"):
        searcher = Searcher()
        searcher.get_urls(query)
        query = input("\n Enter your query (quit to end program): ")

    print("Have a nice day!")

    # results = searcher.get_data('irvine')
    #
    # file = "WEBPAGES_CLEAN/" + "bookkeeping.json"
    #
    # lib = open(file).read()
    #
    # jsonObj = json.loads(lib)
    #
    # for doc in results:
    #     print(doc[0], doc[1], doc[2], jsonObj[doc[0]])








