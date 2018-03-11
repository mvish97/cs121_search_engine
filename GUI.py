import tkinter
from searchFiles import Searcher


class SearchGUI:
    def __init__(self, master):
        self.master = master
        self.default_font = ("Helvetica", 16)
        self.master.title("Search System")
        self.search_system = Searcher()

        self.query = tkinter.StringVar()
        self.results = tkinter.StringVar()
        self.results.set("Results appear here")

        self.search_box = tkinter.Label(master=self.master, text="Search Query: ", font=self.default_font)
        self.search_box.grid(row=1, column=1, padx=20, pady=20, sticky=tkinter.W + tkinter.N)

        vcmd = master.register(self.validate)
        self.query_entry = tkinter.Entry(master, validate="key", validatecommand=(vcmd, '%P'))
        self.query_entry.grid(row=1, column=2, padx=20, pady=20, sticky=tkinter.W + tkinter.N)

        self.results_label = tkinter.Label(master, textvariable=self.results, anchor=tkinter.W, justify=tkinter.LEFT,
                                           wraplength=700, background="#c1d9ff", font=self.default_font)
        self.results_label.grid(row=2, column=1, columnspan=3, ipadx=20, ipady=20, padx=20, pady=20,
                                sticky=tkinter.W + tkinter.N)

        self.search_button = tkinter.Button(master, text="Search", command=lambda: self.search())
        self.search_button.grid(row=1, column=3, padx=5, pady=5, sticky=tkinter.E)

        self.quit_button = tkinter.Button(master, text="Quit", command=master.quit)
        self.quit_button.grid(row=3, column=2, padx=5, pady=5, sticky=tkinter.S)

    def validate(self, query):
        # if not query:
        #     self.results.set("Value Error. Try again.")
        #     return False
        try:
            self.query = str(query)
            return True
        except ValueError:
            self.results.set("Value Error. Try again.")
            return False

    def search(self):
        self.results.set(self.search_system.get_urls(self.query))


if __name__ == '__main__':
    root = tkinter.Tk()
    my_gui = SearchGUI(root)
    root.mainloop()
