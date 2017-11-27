import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import csv

class MultiColumnListbox(object):

    def __init__(self,frame):
        self.f = frame
        self.tree = None
        self._setup_widgets()
        self._build_tree()

    def _setup_widgets(self):
        s = """click on header to sort by that column
        to change width of column drag boundary
        """
        msg = ttk.Label(self.f,wraplength="4i", justify="left", anchor="n",
            padding=(10, 2, 10, 6), text=s)
        msg.pack(fill='x')
        container = ttk.Frame(self.f)
        container.pack(fill='both', expand=True)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=car_header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)


    def _build_tree(self):
        for col in car_header:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: self.sortby(self.tree, c, 0))
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))

        for item in car_list:
            self.tree.insert('', 'end', values=item)
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(car_header[ix],width=None)<col_w:
                    self.tree.column(car_header[ix], width=col_w)



    def sortby(self,tree, col, descending):
        """sort tree contents when a column header is clicked on"""
        data = [(tree.set(child, col), child) \
            for child in tree.get_children('')]
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        tree.heading(col, command=lambda col=col: self.sortby(tree, col,
            int(not descending)))




car_list = [("Time", "Source", "Destination", "Fare", "Card #")]
car_header = ["Time", "Source", "Destination", "Fare", "Card #"]
root = tk.Tk()
root.title("Multicolumn Treeview/Listbox")
Label = tk.Label(root,text= "is this working?")
Label.grid(row=0,column=0)
frame = tk.Frame(root)
frame.grid(row=1,column=0)
listbox = MultiColumnListbox(frame)
root.mainloop()
