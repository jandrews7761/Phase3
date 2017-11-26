from tkinter import *
from tkinter import messagebox
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import pymysql
import hashlib
import csv


### GO BACK AND CHANGE BUTTON COMMANDS

class MartaHack:
    def __init__(self,homeWin):
        # self.db = pymysql.connect(host='academic-mysql.cc.gatech.edu',
        #                      user='cs4400_Group_14',
        #                      password='_MlrJUuF',
        #                      db='cs4400_Group_14')
        # self.cursor = self.db.cursor()

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
        b1=Button(passF,text="Register",bg=self.fgColor1,command=self.adminSuspMgt)
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
        self.homeWin.withdraw()
        self.regWin = Toplevel()
        self.regWin.protocol("WM_DELETE_WINDOW", self.endProgram)
        self.regWin.title("Welcome to MARTA")
        self.regWin.configure(bg=self.bgColor1)

        topF = Frame(self.regWin, bg=self.bgColor1)
        topF.grid(row=0, column=0, pady=15, padx=10)
        l1 = Label(topF, text="Breeze Card", bg=self.bgColor1)
        l1.grid(row=0, column=0, sticky=NSEW, pady=5, padx=5)
        l2 = Label(topF, text="Mange Cards", bg=self.bgColor1)
        l2.grid(row=0, column=2, sticky=NSEW, pady=5, padx=5)
        l3 = Label(topF, text="Balance", bg=self.bgColor1)
        l3.grid(row=1, column=0, sticky=NSEW, pady=5, padx=5)

        root = Tk()
        tkvar = StringVar (root)
        # choices : Fill with sql query for breezecards)
        choices = {'BreezeCard1', 'BreezeCard2', 'BreezeCard3'}
        tkvar.set('BreezeCard 1')
        e1 = Entry(topF)
        e1.grid(row=0, column=1, sticky=NSEW, pady=5, padx=5)
        e2 = OptionMenu(topF, tkvar, *choices)
        e2.grid(row=1, column=1, sticky=NSEW, pady=5, padx=5)
        def change_dropdown(*args):
            print( tkvar.get())
        tkvar.trace('w', change_dropdown)



        l4 = Label(topF, text="Start at", bg=self.bgColor1)
        l4.grid(row=2, column=0, sticky=NSEW, pady=5, padx=5)
        l5 = Label(topF, text="Trip in Progress", bg=self.bgColor1)
        l5.grid(row=2, column=2, sticky=NSEW, pady=5, padx=5)
        l6 = Label(topF, text="Ending at", bg=self.bgColor1)
        l6.grid(row=3, column=0, sticky=NSEW, pady=5, padx=5)
        l7 = Label(topF, text="End Trip", bg=self.bgColor1)
        l7.grid(row=3, column=2, sticky=NSEW, pady=5, padx=5)
        e3 = Entry(topF)
        e3.grid(row=2, column=1, sticky=NSEW, pady=5, padx=5)
        e4 = Entry(topF)
        e4.grid(row=3, column=1, sticky=NSEW, pady=5, padx=5)

        botF = Frame(self.regWin, bg=self.bgColor1)
        botF.grid(row=1, column=0, pady=15, padx=10)
        self.v = StringVar()
        self.v.set("False")

        l8 = Label(botF, text="View Trip History", bg=self.bgColor2)
        l8.grid(row=1, column=0, pady=5, padx=5, sticky=NSEW)
        l9 = Label(botF, text="", bg=self.bgColor1)
        l9.grid(row=1, column=1, pady=5, padx=5, sticky=NSEW)
        l10 = Label(botF, text="Log Out", bg=self.bgColor2)
        l10.grid(row=1, column=2, pady=5, padx=5, sticky=NSEW)


    def adminStationMgt(self):
        # withdraw adminHome?? and then build new window
        # buttons to call self.viewStation, self.createStation
        pass

    def viewStation(self):
        pass

    def createStation(self):
        pass

    def adminSuspMgt(self):
        self.homeWin.withdraw()
        self.regWin = Toplevel()
        self.regWin.protocol("WM_DELETE_WINDOW", self.endProgram)
        self.regWin.title("Suspended Cards")
        self.regWin.configure(bg=self.bgColor1)

        topF = Frame(self.regWin, bg=self.bgColor1)
        topF.grid(row=0, column=0, pady=15, padx=10)
        listbox = Listbox(topF)
        listbox.pack()
        currencies = {}

        with open('Try2.csv') as f:
            next(f, None)  # Skip the header.
            reader = csv.reader(f, delimiter=',')
            for Card, Value, Owner in reader:
                currencies[f'{Card} {Value} {Owner}'] = Card

        for key in currencies:
            listbox.insert('end', key)
        listbox.grid(row=0, column=0)
        listbox.bind('<Key-Return>', lambda event: print(currencies[listbox.selection_get()]))

        botF = Frame(self.regWin, bg=self.bgColor1)
        botF.grid(row=1, column=0, pady=15, padx=10)
        b1 = Button(botF, text="Assign Selected Card to New Owner", bg=self.fgColor1, command=self.logIn)
        b1.grid(row=1, column=1, sticky=NSEW, pady=5, padx=5)
        b2 = Button(botF, text="Assign Selected Card to Previous Owner", bg=self.fgColor1, command=self.tripHist)
        b2.grid(row=2, column=1, sticky=NSEW, pady=5, padx=5)
        l1 = Label(botF, text="Assigning the card to an owner will unlock all accounts conflicted on the same Breeze Card.", bg=self.bgColor1)
        l1.grid(row=3, column=1, sticky=NSEW, pady=5, padx=5)


    def adminCardMgt(self):
        self.homeWin.withdraw()
        self.regWin = Toplevel()
        self.regWin.protocol("WM_DELETE_WINDOW", self.endProgram)
        self.regWin.title("Breeze Card Management")
        self.regWin.configure(bg=self.bgColor1)

        topF = Frame(self.regWin, bg=self.bgColor1)
        topF.grid(row=0, column=0, pady=15, padx=10)
        l1 = Label(topF, text="Owner", bg=self.bgColor1)
        l1.grid(row=0, column=0, sticky=NSEW, pady=5, padx=5)
        l2 = Label(topF, text="Card Number", bg=self.bgColor1)
        l2.grid(row=1, column=0, sticky=NSEW, pady=5, padx=5)
        e1 = Entry(topF)
        e1.grid(row=0, column=1, sticky=NSEW, pady=5, padx=5)
        e2 = Entry(topF)
        e2.grid(row=1, column=1, sticky=NSEW, pady=5, padx=5)
        l3 = Label(topF, text="Value between", bg=self.bgColor1)
        l3.grid(row=3, column=0, sticky=NSEW, pady=5, padx=5)
        e3 = Entry(topF)
        e3.grid(row=3, column=1, sticky=NSEW, pady=5, padx=5)
        l4 = Label(topF, text="and", bg=self.bgColor1)
        l4.grid(row=3, column=2, sticky=NSEW, pady=5, padx=5)
        e4 = Entry(topF)
        e4.grid(row=3, column=3, sticky=NSEW, pady=5, padx=5)


        rightF = Frame(self.regWin, bg=self.bgColor1)
        rightF.grid(row=0, column=2, pady=15, padx=10)
        b1 = Button(rightF, text="Reset", bg=self.fgColor1, command=self.logIn)
        b1.grid(row=1, column=1, sticky=NSEW, pady=5, padx=5)
        b2 = Button(rightF, text="Update Filter", bg=self.fgColor1, command=self.tripHist)
        b2.grid(row=2, column=1, sticky=NSEW, pady=5, padx=5)
        self.v = StringVar()
        self.v.set("False")
        rb1 = Radiobutton(rightF, text="Show Suspended Cards", variable=self.v, value="True", bg=self.fgColor1)
        rb1.grid(row=0, column=0, columnspan=2, pady=5, padx=5, sticky=NSEW)

        botF = Frame(self.regWin, bg=self.bgColor1)
        botF.grid(row=1, column=0, pady=15, padx=10)
        e5 = Entry(botF)
        e5.grid(row=1, column=0, sticky=NSEW, pady=5, padx=5)
        e6 = Entry(botF)
        e6.grid(row=2, column=0, sticky=NSEW, pady=5, padx=5)
        b3 = Button(botF, text="Set Value of Selected Card", bg=self.bgColor1, command=self.tripHist)
        b3.grid(row=1, column=1, sticky=NSEW, pady=5, padx=5)
        b4 = Button(botF, text="Set Value of Selected Card", bg=self.bgColor1, command=self.tripHist)
        b4.grid(row=2, column=1, sticky=NSEW, pady=5, padx=5)


        listbox = Listbox(botF)
        listbox.pack()
        currencies = {}

        with open('Try2.csv') as f:
            next(f, None)  # Skip the header.
            reader = csv.reader(f, delimiter=',')
            for Card, Value, Owner in reader:
                currencies[f'{Card} {Value} {Owner}'] = Card

        for key in currencies:
            listbox.insert('end', key)
        listbox.grid(row=0, column=0)
        listbox.bind('<Key-Return>', lambda event: print(currencies[listbox.selection_get()]))





    def pflowReport(self):
        pass

    def cardMgt(self):
        self.homeWin.withdraw()
        self.regWin = Toplevel()
        self.regWin.protocol("WM_DELETE_WINDOW", self.endProgram)
        self.regWin.title("Manage Cards")
        self.regWin.configure(bg=self.bgColor1)

        topF = Frame(self.regWin, bg=self.bgColor1)
        topF.grid(row=0, column=0, pady=15, padx=10)
        listbox = Listbox(topF)
        listbox.pack()
        currencies = {}

        with open('Try2.csv') as f:
            next(f, None)  # Skip the header.
            reader = csv.reader(f, delimiter=',')
            for Card, Value, Owner in reader:
                currencies[f'{Card} {Value} {Owner}'] = Card

        for key in currencies:
            listbox.insert('end', key)
        listbox.grid(row=0, column=0)
        listbox.bind('<Key-Return>', lambda event: print(currencies[listbox.selection_get()]))


        e1 = Entry(topF)
        e1.grid(row=1, column=0, sticky=NSEW, pady=5, padx=5)
        b1 = Button(topF, text="Add Card", bg=self.bgColor1, command=self.tripHist)
        b1.grid(row=1, column=1, sticky=NSEW, pady=5, padx=5)

        botF = Frame(self.regWin, bg=self.bgColor1)
        botF.grid(row=1, column=0, pady=15, padx=10)

        l1 = Label(botF, text="Add Value to Selected Card", bg=self.bgColor1)
        l1.grid(row=0, column=0, sticky=NSEW, pady=5, padx=5)

        l2 = Label(botF, text="Credit Card #", bg=self.bgColor1)
        l2.grid(row=1, column=0, sticky=NSEW, pady=5, padx=5)
        e2 = Entry(botF)
        e2.grid(row=1, column=1, sticky=NSEW, pady=5, padx=5)

        l3 = Label(botF, text="Value", bg=self.bgColor1)
        l3.grid(row=2, column=0, sticky=NSEW, pady=5, padx=5)
        e3 = Entry(botF)
        e3.grid(row=2, column=1, sticky=NSEW, pady=5, padx=5)

        b2 = Button(botF, text="Add Value", bg=self.bgColor1, command=self.tripHist)
        b2.grid(row=3, column=2, sticky=NSEW, pady=5, padx=5)


    def tripHist(self):
        self.homeWin.withdraw()
        self.regWin = Toplevel()
        self.regWin.protocol("WM_DELETE_WINDOW", self.endProgram)
        self.regWin.title("Trip History")
        self.regWin.configure(bg=self.bgColor1)

        topF = Frame(self.regWin, bg=self.bgColor1)
        topF.grid(row=0, column=0, pady=15, padx=10)
        l1 = Label(topF, text="Start Time", bg=self.bgColor1)
        l1.grid(row=0, column=0, sticky=NSEW, pady=5, padx=5)
        l2 = Label(topF, text="End Time", bg=self.bgColor1)
        l2.grid(row=1, column=0, sticky=NSEW, pady=5, padx=5)
        e1 = Entry(topF)
        e1.grid(row=0, column=1, sticky=NSEW, pady=5, padx=5)
        e2 = Entry(topF)
        e2.grid(row=1, column=1, sticky=NSEW, pady=5, padx=5)

        rightF = Frame(self.regWin, bg=self.bgColor1)
        rightF.grid(row=0, column=2, pady=15, padx=10)
        b1 = Button(rightF, text="Update", bg=self.fgColor1, command=self.logIn)
        b1.grid(row=0, column=0, sticky=NSEW, pady=5, padx=5)
        b1 = Button(rightF, text="Reset", bg=self.fgColor1, command=self.tripHist)
        b1.grid(row=0, column=1, sticky=NSEW, pady=5, padx=5)

        botF = Frame(self.regWin, bg=self.bgColor1)
        botF.grid(row=1, column=0, pady=15, padx=10)
        listbox = Listbox(botF)
        listbox.pack()
        currencies = {}

        with open('Try.csv') as f:
            next(f, None)  # Skip the header.
            reader = csv.reader(f, delimiter=',')
            for Fare, Start, Number, TimeS, TimeE in reader:
                currencies[f'{Fare} {Start} {Number} {TimeS} {TimeE}'] = Start

        # for key in currencies:
        #     listbox.insert('end', key)
        # listbox.grid(row=0, column=0)
        # listbox.bind('<Key-Return>', lambda event: print(currencies[listbox.selection_get()]))

        table = [start]

        headers = ["Time", "Source", "Destination", "Fare", "Card #"]

        row_format = "{:<8}  {:>8}  {:<8}  {:8}"
        listbox.insert(0, row_format.format(*headers, sp=" " * 2))
        for items in table:
            listbox.insert(END, row_format.format(*items, sp=" " * 2))

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
