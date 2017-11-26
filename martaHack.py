from tkinter import *
from tkinter import messagebox
import pymysql
import hashlib
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import csv

class MultiColumnListbox(object):

    def __init__(self):
        self.tree = None
        self._setup_widgets()
        self._build_tree()

    def _setup_widgets(self):
        s = """click on header to sort by that column
to change width of column drag boundary
        """
        msg = ttk.Label(wraplength="4i", justify="left", anchor="n",
            padding=(10, 2, 10, 6), text=s)
        msg.pack(fill='x')
        container = ttk.Frame()
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
                command=lambda c=col: sortby(self.tree, c, 0))
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))

        for item in car_list:
            self.tree.insert('', 'end', values=item)
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(car_header[ix],width=None)<col_w:
                    self.tree.column(car_header[ix], width=col_w)



def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))



currencies = []
with open('Try.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    currencies = list(reader)


car_list = currencies
car_header = ["Time", "Source", "Destination", "Fare", "Card #"]

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Multicolumn Treeview/Listbox")
    listbox = MultiColumnListbox()
    root.mainloop()

class MartaHack:
    def __init__(self,homeWin):
        self.db = pymysql.connect(host='academic-mysql.cc.gatech.edu',
                             user='cs4400_Group_14',
                             password='_MlrJUuF',
                             db='cs4400_Group_14')
        self.cursor = self.db.cursor()

        self.bgColor1 = "SlateGray"
        self.bgColor2 = "tan2"
        self.fgColor1 = "burlywood"
        self.fgColor2 = "burlywood1"

        self.homeWin = homeWin
        self.homeWin.protocol("WM_DELETE_WINDOW",self.endProgram)
        self.homeWin.title("Log In")
        self.homeWin.configure(bg=self.bgColor1)

        topF = Frame(self.homeWin,bg=self.bgColor1)
        topF.grid(row=0,column=0,pady=15,padx=10)
        l1 = Label(topF,text="Username",bg=self.fgColor1)
        l1.grid(row=0,column=0,sticky=NSEW,pady=5,padx=5)
        l2 = Label(topF,text="Password",bg=self.fgColor1)
        l2.grid(row=1,column=0,sticky=NSEW,pady=5,padx=5)
        e1 = Entry(topF)
        e1.grid(row=0,column=1,sticky=NSEW,pady=5,padx=5)
        e2 = Entry(topF)
        e2.grid(row=1,column=1,sticky=NSEW,pady=5,padx=5)

        passF = Frame(self.homeWin,bg=self.bgColor1)
        passF.grid(row=1,column=0,pady=10,padx=20)
        b1 = Button(passF,text="Log In",bg=self.fgColor1,command=self.logIn)
        b1.grid(row=0,column=0,sticky=NSEW,pady=5,padx=5)
        b1=Button(passF,text="Register",bg=self.fgColor1,command=self.register)
        b1.grid(row=1,column=0,sticky=NSEW,pady=5,padx=5)

        self.userE = e1
        self.passE = e2

    def logIn(self):
        pwd = self.passE.get()
        encoded = pwd.encode('utf-8')
        m = hashlib.md5()
        m.update(encoded)
        hashed = m.hexdigest()
        usr = self.userE.get()
        query = '''select isPassenger where username = ''' + usr + ''' and pass = ''' + hashed
        #c = self.cursor.execute(query)
        #coding off network, instantiating variables
        c = 1
        if c == 0:
            messagebox.showerror("Login failed. Check your spelling and try again")
            pass
        elif c > 1:
            messagebox.showerror("MULTIPLE USERS HAVE THESE CREDENTIALS. I HAVE NO IDEA HOW THIS IS POSSIBLE, FUCK YOUR SHIT")
            pass
        else:
            #isAdmin = list(cursor.fetchall())[0]
            isAdmin = True
            print(isAdmin)
            if isAdmin:
                self.homeWin.withdraw()
                self.adminHome()
            else:
                self.homeWin.withdraw()
                self.passHome()
        # add code and sql here to determine if credentials match an account
        # if not, message an error back
        # if so, ascertain admin or reg user
        # withdraw homewin, and call either self.passHome() or self.adminHome()

    def register(self):
        # withdraw home window and create a new register window
        # the register button must call a registerNewUser method
        self.homeWin.withdraw()
        self.regWin = Toplevel()
        self.regWin.protocol("WM_DELETE_WINDOW",self.endProgram)
        self.regWin.title("Log In")
        self.regWin.configure(bg=self.bgColor1)

        topF = Frame(self.regWin,bg=self.bgColor1)
        topF.grid(row=0,column=0,pady=15,padx=10)
        l1 = Label(topF,text="Username",bg=self.fgColor1)
        l1.grid(row=0,column=0,sticky=NSEW,pady=5,padx=5)
        l2 = Label(topF,text="Email Address",bg=self.fgColor1)
        l2.grid(row=1,column=0,sticky=NSEW,pady=5,padx=5)
        e1 = Entry(topF)
        e1.grid(row=0,column=1,sticky=NSEW,pady=5,padx=5)
        e2 = Entry(topF)
        e2.grid(row=1,column=1,sticky=NSEW,pady=5,padx=5)
        l3 = Label(topF,text="Password",bg=self.fgColor1)
        l3.grid(row=2,column=0,sticky=NSEW,pady=5,padx=5)
        l4 = Label(topF,text="Confirm Password",bg=self.fgColor1)
        l4.grid(row=3,column=0,sticky=NSEW,pady=5,padx=5)
        e3 = Entry(topF)
        e3.grid(row=2,column=1,sticky=NSEW,pady=5,padx=5)
        e4 = Entry(topF)
        e4.grid(row=3,column=1,sticky=NSEW,pady=5,padx=5)

        botF = Frame(self.regWin,bg=self.bgColor1)
        botF.grid(row=1,column=0,pady=15,padx=10)
        self.v = StringVar()
        self.v.set("False")
        rb1 = Radiobutton(botF,text="Use my existing card",variable = self.v, value = "True",bg=self.fgColor1)
        rb1.grid(row=0,column=0,columnspan=2,pady=5,padx=5,sticky=NSEW)
        l5 = Label(botF,text= "Card Number",bg=self.fgColor1)
        l5.grid(row=1,column=0,pady=5,padx=5,sticky=NSEW)
        e5 = Entry(botF)
        e5.grid(row=1,column=1,pady=5,padx=5,sticky=NSEW)
        rb2 = Radiobutton(botF,text="Get a new breezecard",variable = self.v,value = "False",bg=self.fgColor1)
        rb2.grid(row=2,column=0,pady=5,padx=5,columnspan=2,sticky=NSEW)


    def registerNewUser(self):
        # add code to check if entries are valid
        # if not error
        # if so, try to insert into db with mysql, catch pass
        # if all successfull, message "account created"
        # withdraw (destroy?) register win, call passHome if all successfull
        self.regWin.destroy()
        self.passHome()
        pass

    def adminHome(self):
        # create adminHome page
        # buttons to call self.adminStationMgt, self.adminSuspMgt,
            # self.adminCardMgt,self.pflowReport, self.logOut
        self.adminHomeWin = Toplevel()
        pass

    def passHome(self):
        # buttons to call self.cardMgt, self.tripHist, self.logOut
        pass

    def adminStationMgt(self):
        # withdraw adminHome?? and then build new window
        # buttons to call self.viewStation, self.createStation
        pass

    def viewStation(self):
        pass

    def createStation(self):
        pass

    def adminSuspMgt(self):
        pass

    def adminCardMgt(self):
        pass

    def pflowReport(self):
        pass

    def cardMgt(self):
        pass

    def tripHist(self):
        pass

    def logOut(self):
        pass
        # must destroy all windows (a bunch of try excepts)
        # make logIn reappear

    def endProgram(self):
        try:
            self.cursor.close()
            self.db.commit()
            self.db.close()
        except:
            pass
        self.homeWin.destroy()




win = Tk()
MartaHack(win)
win.mainloop()
