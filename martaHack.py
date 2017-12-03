from tkinter import *
from tkinter import messagebox
import pymysql
import hashlib
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import csv
import random
from re import match

marta_header = ["Time", "Source", "Destination", "Fare", "Card #"]
marta_list = [("Time", "Source", "Destination", "Fare", "Card #")]

# THINGS TO DO: registerNewUser method needs to suspend buzzcards if new user
# has an old buzzcard
# more db.commit()
# create new station
# fix viewStation sql capability
# z fix viewStation -fare

class MultiColumnListbox(object):
    def __init__(self,frame,car_header,car_list):
        self.car_header = car_header
        self.car_list = car_list
        self.f = frame
        self.tree = None
        self._setup_widgets()
        self._build_tree()

    def _setup_widgets(self):
        container = ttk.Frame(self.f)
        container.grid(row=0, column=0,pady=10,padx=10)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(container,columns=self.car_header, show="headings")
        vsb = ttk.Scrollbar(container,orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(container,orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew')
        vsb.grid(column=1, row=0, sticky='ns')
        hsb.grid(column=0, row=1, sticky='ew')
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

    def _build_tree(self):
        for col in self.car_header:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: self.sortby(self.tree, c, 0))
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))

        for item in self.car_list:
            self.tree.insert('', 'end', values=item)
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(self.car_header[ix],width=None)<col_w:
                    self.tree.column(self.car_header[ix], width=col_w)

    def sortby(self,tree, col, descending):
        """sort tree contents when a column header is clicked on"""
        data = [(tree.set(child, col), child) \
            for child in tree.get_children('')]
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        tree.heading(col, command=lambda col=col: self.sortby(tree, col,
            int(not descending)))

    def gotClicked(self):
        #print(self.tree.item(self.tree.focus())['values'])
        return self.tree.item(self.tree.focus())['values']

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
        query = '''SELECT isAdmin FROM User WHERE Username = %s AND Password = %s'''
        c = self.cursor.execute(query,(usr,hashed))
        # c = 1 # instantiating variables when coding off network
        if c == 0:
            messagebox.showerror("Login failed","Check your spelling and try again")
            pass
        elif c > 1:
            messagebox.showerror("ARF","MULTIPLE USERS HAVE THESE CREDENTIALS. I HAVE NO IDEA HOW THIS IS POSSIBLE, FUCK YOUR SHIT")
        else:
            isAdmin = list(self.cursor.fetchall())[0][0]
            #print(isAdmin)
            if isAdmin:
                self.homeWin.withdraw()
                self.adminHome()
            else:
                self.homeWin.withdraw()
                self.passHome()

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

        butF = Frame(self.regWin,bg=self.bgColor1)
        butF.grid(row=2,column=0,pady=15,padx=10)
        b1 = Button(butF,text = "Create Account",command=self.registerNewUser,bg=self.fgColor1)
        b1.grid(row=0,column=0,pady=5,padx=5,sticky=NSEW)
        b2 = Button(butF,text = "Back to Log In", command = self.logOut)
        b2.grid(row=0,column=1,pady=5,padx=5,sticky=NSEW)

        self.usrE = e1
        self.eAddE = e2
        self.pass1e = e3
        self.pass2e = e4
        self.bzNumE = e5

    def registerNewUser(self):
        # add code to check if entries are valid
        # if not error
        # if so, try to insert into db with mysql, catch pass
        # if all successfull, message "account created"
        # withdraw (destroy?) register win, call passHome if all successfull
        failed = False
        print(len(self.bzNumE.get()),self.v.get())
        if self.usrE.get() == "":
            failed = True
            messagebox.showerror("No Username Provided","Enter a username")
        elif self.pass1e.get() != self.pass2e.get() :
            failed = True
            messagebox.showerror("Password Mismatch","Check that both passwords are identical")
        elif len(self.pass1e.get()) < 8:
            failed = True
            messagebox.showerror("Password too short","Password needs to be at least eight characters")
        elif len(self.bzNumE.get()) != 16 and self.v.get() == "True":
            failed = True
            messagebox.showerror("Invalid Buzzcard","Buzzcard must be 16 characters")
        elif not match ("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z0-9]+)$", self.eAddE.get()):
            failed = True
            messagebox.showerror("Invalid Email","Please enter a valid email address")
        else:
            sql1 = '''SELECT
                        Username, Email
                    FROM
                        Passenger
                    WHERE
                        Username = %s
                            OR email = %s'''
            sql2 = '''SELECT
                        BelongsTo
                    FROM
                        Breezecard
                    WHERE
                        BreezecardNum = %s'''
            sql3 = '''SELECT Username FROM User WHERE Username = %s'''
            c1 = self.cursor.execute(sql1,(self.usrE.get(),self.eAddE.get()))
            c3 = self.cursor.execute(sql3,self.usrE.get())
            if c1 >= 1 or c3 >= 1:
                # either the username or email is in use
                failed = True
                messagebox.showerror("Cannot create account","This email address and/or username is in use")
        if not failed:
            # after this point, nothing can fail
            # did the user have their own buzznum, either way insert data
            autoGen = False
            if self.v.get() == "True":
                c2 = self.cursor.execute(sql2,(self.bzNumE.get()))
                if c2 >= 1:
                    autoGen = True
                    # SUSPEND THE BUZZCARD
                else:
                    bzNum = self.bzNumE.get()
            elif self.v.get() == "False" or autoGen:
                # AUTO GENERATE HERE
                bzNum = self.autoGenerate()
                # AUTO GENERATE HERE
            sql1 = '''INSERT INTO User VALUES (%s,%s,%s)'''
            sql2 = '''INSERT INTO Passenger VALUES (%s,%s)'''
            # hash password
            pwd = self.pass1e.get()
            encoded = pwd.encode('utf-8')
            m = hashlib.md5()
            m.update(encoded)
            passHash = m.hexdigest()
            # try to insert into sql, if anything goes wrong, error to user
            try:
                self.cursor.execute(sql1,(self.usrE.get(),passHash,False))
                self.cursor.execute(sql2,(self.usrE.get(),self.eAddE.get()))
                messagebox.showinfo("Success","Account successfully created with buzzcard: " + bzNum)
                self.db.commit()
                self.regWin.destroy()
                self.passHome()
            except:
                messagebox.showerror("An Error Occured","Please check your network connection and try again")

    def autoGenerate(self):
        # AUTO GENERATE A NUMBER HERE
        bzNum = random.randint(1000000000000000,9999999999999999)
        # AUTO GENERATE A NUMBER HERE
        bzNum = str(bzNum)
        sql = '''SELECT BreezecardNum FROM breezecard WHERE BreezecardNum = %s'''
        c = cursor.execute(sql,(bzNum))
        if c == 0:
            return bzNum
        else:
            return self.autoGenerate()

    def adminHome(self):
        # create adminHome page
        # buttons to call self.adminStationMgt, self.adminSuspMgt,
            # self.adminCardMgt,self.pflowReport, self.logOut
        self.adminHomeWin = Toplevel(bg=self.bgColor1)
        self.adminHomeWin.protocol("WM_DELETE_WINDOW",self.endProgram)
        self.adminHomeWin.title("Administrator Home")

        b1 = Button(self.adminHomeWin,text="Passenger Flow Report", command = self.pFlowReport,bg=self.fgColor1)
        b1.pack(padx=10,pady=5)

        b2 = Button(self.adminHomeWin,text="Suspended Cards", command=self.adminSuspMgt,bg=self.fgColor1)
        b2.pack(padx=10,pady=5)

        b3 = Button(self.adminHomeWin,text= "Breeze Card Management", command = self.adminCardMgt,bg=self.fgColor1)
        b3.pack(padx=10,pady=5)

        b4 = Button(self.adminHomeWin,text="Station Management", command = self.adminStationMgt,bg=self.fgColor1)
        b4.pack(padx=10,pady=5)

        b5 = Button(self.adminHomeWin,text="Log Out", command= self.logOut, bg=self.fgColor1)
        b5.pack(padx=10,pady=15)

    def passHome(self):
        # buttons to call self.cardMgt, self.tripHist, self.logOut
        self.homeWin.withdraw()
        self.passHomeWin = Toplevel()
        self.passHomeWin.protocol("WM_DELETE_WINDOW", self.endProgram)
        self.passHomeWin.title("Welcome to MARTA")
        self.passHomeWin.configure(bg=self.bgColor1)

        topF = Frame(self.passHomeWin, bg=self.bgColor1)
        topF.grid(row=0, column=0, pady=15, padx=10)
        l1 = Label(topF, text="Breeze Card", bg=self.bgColor1)
        l1.grid(row=0, column=0, sticky=NSEW, pady=5, padx=5)
        l2 = Button(topF, text="Manage Cards", bg=self.fgColor1, command=self.cardMgt)
        l2.grid(row=0, column=2, sticky=NSEW, pady=5, padx=5)
        l3 = Label(topF, text="Balance", bg=self.bgColor1)
        l3.grid(row=1, column=0, sticky=NSEW, pady=5, padx=5)

        #root = Tk()
        tkvar = StringVar()
        # choices : Fill with sql query for breezecards)
        choices = {'BreezeCard1', 'BreezeCard2', 'BreezeCard3'}
        tkvar.set('BreezeCard 1')
        e1 = Entry(topF)
        e1.grid(row=1, column=1, sticky=NSEW, pady=5, padx=5)
        e2 = OptionMenu(topF, tkvar, *choices)
        e2.grid(row=0, column=1, sticky=NSEW, pady=5, padx=5)
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

        botF = Frame(self.passHomeWin, bg=self.bgColor1)
        botF.grid(row=1, column=0, pady=15, padx=10)
        self.v = StringVar()
        self.v.set("False")

        l8 = Button(botF, text="View Trip History", bg=self.fgColor1, command = self.tripHist)
        l8.grid(row=1, column=0, pady=5, padx=5, sticky=NSEW)
        l9 = Label(botF, text="", bg=self.bgColor1)
        l9.grid(row=1, column=1, pady=5, padx=5, sticky=NSEW)
        l10 = Label(botF, text="Log Out", bg=self.bgColor2)
        l10.grid(row=1, column=2, pady=5, padx=5, sticky=NSEW)

    def adminStationMgt(self):
        # withdraw adminHome?? and then build new window
        # buttons to call self.viewStation, self.createStation
        #self.adminHomeWin.withdraw()
        self.aStatMgtWin = Toplevel()
        #self.aStatMgtWin.protocol("WM_DELETE_WINDOW", self.endProgram)
        self.aStatMgtWin.title("Station Listing")
        self.aStatMgtWin.configure(bg=self.bgColor1)
        topF = Frame(self.aStatMgtWin, bg=self.bgColor1)
        topF.grid(row=0, column=0, pady=15, padx=10)
        header = ["Station Name", "Stop ID", "Fare", "Status"]
        data = self.adminStationMgtQuery()
        print(data)
        self.stationMgtListBox = MultiColumnListbox(topF,header,data)
        botF = Frame(self.aStatMgtWin, bg=self.bgColor1)
        botF.grid(row=1, column=0, pady=15, padx=10)
        b1 = Button(botF, text="View Station", bg=self.fgColor1, command=self.viewStation)
        b1.grid(row=1, column=1, sticky=NSEW, pady=5, padx=5)
        b2 = Button(botF, text="Create New Station", bg=self.fgColor1, command=self.createStation)
        b2.grid(row=2, column=1, sticky=NSEW, pady=5, padx=5)

    def adminStationMgtQuery(self):
        sql = '''SELECT
                    Name, stopID, EnterFare, ClosedStatus
                FROM
                    Station'''
        self.cursor.execute(sql)
        return list(self.cursor.fetchall())

    def viewStation(self):
        x = self.stationMgtListBox.gotClicked()
        try:
            x[0]
            failed = False
        except:
            failed = True
            messagebox.showerror("No Selected Station", "Please select a station first")
        if not failed:
            self.viewStationWin = Toplevel(width= 200, height=100)
            #self.viewStationWin.protocol("WM_DELETE_WINDOW", self.endProgram)
            self.viewStationWin.title("Station Detail -" + x[0] )
            self.viewStationWin.configure(bg=self.bgColor1)
            viewS = Frame(self.viewStationWin, bg=self.bgColor1)
            viewS.grid(row=0, column=0, pady=15, padx=10)
            l1 = Label(viewS, text=x[0], bg=self.bgColor1)
            l1.grid(row=0, column=0, sticky=NSEW, pady=5, padx=5)
            l1.config(font = "bold 24")
            l2 = Label(viewS, text= "Stop " + str(x[1]), bg=self.bgColor1, fg = "red")
            l2.grid(row=0, column=2, sticky=NSEW, pady=5, padx=5)
            l2.config(font = "16")
            l3 = Label(viewS, text = "Fare" , bg=self.bgColor1)
            l3.grid(row = 1, column = 0, pady=0, padx=0)
            e1 = Entry(viewS)
            e1.insert(0, '$')

            e1.grid(row =1, column = 1)
            l4 = Label(viewS, text = "Nearest Intersection" , bg=self.bgColor1)
            l4.grid(row = 2, column = 0, pady=10, padx=10)
            l4.config(font = "12")
            b1 = Button(viewS, text = "Update Fare", bg=self.fgColor1, command=self.updateFare)
            b1.grid(row = 1, column = 2)
            self.updateFare = e1

            ##need something for nearest intersection to get to say what it is or if its a train station
            self.varStat = IntVar()
            print(self.varStat.get())
            c = Checkbutton(viewS, text = "Open Station", variable = self.varStat, command = self.getVarStat)
            c.grid(row=3, column=0)
            l5 = Label(viewS, text = "When checked, passengers can enter at this station.", bg = self.bgColor1)
            l5.grid(row=3, column =1)
            l5.config(font = "10")

            print(self.stationMgtListBox.gotClicked())
            #self.aStatMgtWin.withdraw()

    def getVarStat(self):
        print(self.varStat.get())

    def updateFare(self):
        print(self.updateFare.get())

    def createStation(self):
        print(self.stationMgtListBox.gotClicked())

    def adminSuspMgt(self):
        #self.adminHomeWin.withdraw()
        self.aSusWin = Toplevel()
        #self.aSusWin.protocol("WM_DELETE_WINDOW", self.endProgram)
        self.aSusWin.title("Suspended Cards")
        self.aSusWin.configure(bg=self.bgColor1)

        topF = Frame(self.aSusWin, bg=self.bgColor1)
        topF.grid(row=0, column=0, pady=15, padx=10)
        header = ["Card #", "New Owner", "Date Suspended", "Previous owner"]
        data = [("34567890","Conn Man","6/5/3","Avery"),
                ("3456789","Moo Daddy","56/78/92","Moo Son")]
        self.SuspCardListBox = MultiColumnListbox(topF,header,data)
        botF = Frame(self.aSusWin, bg=self.bgColor1)
        botF.grid(row=1, column=0, pady=15, padx=10)
        b1 = Button(botF, text="Assign Selected Card to New Owner", bg=self.fgColor1, command=self.assignSuspCardNewOwner)
        b1.grid(row=1, column=1, sticky=NSEW, pady=5, padx=5)
        b2 = Button(botF, text="Assign Selected Card to Previous Owner", bg=self.fgColor1, command=self.assignSuspCardOldOwner)
        b2.grid(row=2, column=1, sticky=NSEW, pady=5, padx=5)
        l1 = Label(botF, text="Assigning the card to an owner will unlock all accounts conflicted on the same Breeze Card.", bg=self.bgColor1)
        l1.grid(row=3, column=1, sticky=NSEW, pady=5, padx=5)

    def assignSuspCardNewOwner(self):
        sql = '''Update ‘cs4400_Group_14’.’Breezecard’  
        set BelongsTo = %s 
        where BreezecardNum = %s;
        
        Delete BreezecardNum from ‘cs4400_Group_14’.’Conflict’ 
        where BreezecardNum = %s;
                    '''
        self.cursor.execute(sql, Username, cardSelected, cardSelected)

    def assignSuspCardOldOwner(self):
        sql = '''Delete BreezecardNum from ‘cs4400_Group_14’.’Conflict’ 
        where BreezecardNum = %s
                '''
        self.cursor.execute(sql, cardSelected

    def adminCardMgt(self):
        #self.adminHomeWin.withdraw()
        self.aCardWin = Toplevel()
        #self.aCardWin.protocol("WM_DELETE_WINDOW", self.endProgram)
        self.aCardWin.title("Breeze Card Management")
        self.aCardWin.configure(bg=self.bgColor1)

        topF = Frame(self.aCardWin, bg=self.bgColor1)
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

        rightF = Frame(self.aCardWin, bg=self.bgColor1)
        rightF.grid(row=1, column=0, pady=15, padx=10)
        b1 = Button(topF, text="Reset", bg=self.fgColor1, command=self.logIn)
        b1.grid(row=1, column=4, sticky=NSEW, pady=5, padx=5)
        b2 = Button(topF, text="Update Filter", bg=self.fgColor1, command=self.tripHist)
        b2.grid(row=2, column=4, sticky=NSEW, pady=5, padx=5)
        self.v = StringVar()
        self.v.set("False")
        rb1 = Radiobutton(topF, text="Show Suspended Cards", variable=self.v, value="True", bg=self.fgColor1)
        rb1.grid(row=0, column=4, columnspan=1, pady=5, padx=5, sticky=NSEW)

        botF = Frame(self.aCardWin, bg=self.bgColor1)
        botF.grid(row=2, column=0, pady=15, padx=10)
        e5 = Entry(botF)
        e5.grid(row=1, column=0, sticky=NSEW, pady=5, padx=5)
        e6 = Entry(botF)
        e6.grid(row=2, column=0, sticky=NSEW, pady=5, padx=5)
        b3 = Button(botF, text="Set Value of Selected Card", bg=self.bgColor1, command=self.tripHist)
        b3.grid(row=1, column=1, sticky=NSEW, pady=5, padx=5)
        b4 = Button(botF, text="Set Value of Selected Card", bg=self.bgColor1, command=self.tripHist)
        b4.grid(row=2, column=1, sticky=NSEW, pady=5, padx=5)
        header = ["Card #", "New Owner", "Date Suspended", "Previous owner"]
        data = [("34567890", "Conn Man", "6/5/3", "Avery"),
                ("3456789", "Moo Daddy", "56/78/92", "Moo Son")]
        self.AdminCardListBox = MultiColumnListbox(rightF, header, data)

    def pFlowReport(self):
        #self.adminHomeWin.withdraw()
        self.pFlowWin=Toplevel()
        self.pFlowWin.title("Passenger Flow Report")
        #self.pFlowWin.protocol("WM_DELETE_WINDOW",self.endProgram)
        self.pFlowWin.configure(bg=self.bgColor1)

        topF = Frame(self.pFlowWin,bg = self.bgColor1)
        topF.grid(row=0,column=0,pady=15,padx=10)

        l0 = Label(topF,text="yyyy-mm-dd hh:mm:ss",bg=self.bgColor1)
        l0.grid(row=0,column=1,sticky=NSEW)
        l1 = Label(topF,text="Start Time",bg=self.fgColor1,width=10)
        l1.grid(row=1,column=0,pady=5,padx=10,sticky=NSEW)
        l2 = Label(topF,text="End Time",bg=self.fgColor1)
        l2.grid(row=2,column=0,pady=5,padx=10,sticky=NSEW)
        e1 = Entry(topF,width=20)
        e1.grid(row=1,column=1,pady=5,padx=10,sticky=NSEW)
        e2 = Entry(topF)
        e2.grid(row=2,column=1,pady=5,padx=10,sticky=NSEW)
        b1 = Button(topF,text="Update",bg=self.fgColor1, command=self.pFlowUpdate, width=8)
        b1.grid(row=1,column=2,rowspan=2,pady=5,padx=10,sticky=EW)
        b2 = Button(topF,text="Revert",bg=self.fgColor1, command=self.pFlowRevert, width=8)
        b2.grid(row=1,column=3,rowspan=2,pady=5,padx=10,sticky=EW)
        #b3 = Button(topF,text="Home",bg=self.fgColor1, command= self.goToAdminHome, width=8)
        #b3.grid(row=1,column=4,rowspan=2,pady=5,padx=10,sticky=EW)

        self.startTimeE = e1
        self.endTimeE = e2
        botF = Frame(self.pFlowWin)
        botF.grid(row=1,pady=15,padx=10)
        data = self.pFlowQuery()
        header = ["Station Name", "Passengers In", "Pasengers Out", "Flow", "Revenue"]
        self.pFlowListBox = MultiColumnListbox(botF,header,data)
        self.pFlowContainer = botF

    def pFlowRevert(self):
        self.pFlowWin.destroy()
        self.pFlowReport()

    def pFlowUpdate(self):
        # CHECK FOR VALID DATETIMES
        data = self.pFlowQuery()
        del self.pFlowListBox
        header = ["Station Name", "Passengers In", "Pasengers Out", "Flow", "Revenue"]
        #print(data)
        self.pFlowListBox = MultiColumnListbox(self.pFlowContainer,header,data)
        # POPULATE TABLE WITH VALUES

    def pFlowQuery(self):
        sql = '''SELECT
                    t1.statName AS StationName,
                    t1.flowOut AS flowOut,
                    COUNT(Trip.BreezeCardNum) AS flowIn,
                    COUNT(Trip.breezecardNum) - t1.flowOut AS flow,
                    t1.revenue
                FROM
                    (SELECT
                        Station.name AS statName,
                            COUNT(Trip.BreezeCardNum) AS flowOut,
                            SUM(TripFare) AS revenue,
                            Trip.StartsAt AS startID
                    FROM
                        Station
                    INNER JOIN Trip ON Station.StopID = Trip.StartsAt
                    WHERE
                        Trip.startTime >= %s
                            AND Trip.startTime <= %s
                    GROUP BY Trip.StartsAt) AS t1
                        INNER JOIN
                    Trip ON t1.startID = Trip.endsAt
                WHERE
                    Trip.startTime >= %s
                        AND Trip.startTime <= %s
                GROUP BY StationName'''
        p = "^$|(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})"
        if self.startTimeE.get() == "" or not match(p,self.startTimeE.get()):
            startTime = "1970-01-01 1:00:00"
        else:
            startTime = self.startTimeE.get()
        if self.endTimeE.get() == "" or not     match(p,self.endTimeE.get()):
            endTime = "2025-01-01 12:00:00"
        else:
            endTime = self.endTimeE.get()

        if not match(p,self.startTimeE.get()) or not match(p, self.endTimeE.get()):
            messagebox.showerror("Incorrect formatting", "Incorrect starttime/endtime formats. Please enter as yyyy-mm-dd hh:mm:ss. Currently displaying all data")
        try:
            c = self.cursor.execute(sql,(startTime, endTime, startTime, endTime))
            return list(self.cursor.fetchall())
        except:
            messagebox.showerror("Incorrect formatting", "Incorrect starttime/endtime formats. Please enter as yyyy-mm-dd hh:mm:ss")

    def goToAdminHome(self):
        pass

    def cardMgt(self):
        self.passHomeWin.withdraw()
        self.passCardWin = Toplevel()
        self.passCardWin.protocol("WM_DELETE_WINDOW", self.endProgram)
        self.passCardWin.title("Manage Cards")
        self.passCardWin.configure(bg=self.bgColor1)

        topF = Frame(self.passCardWin, bg=self.bgColor1)
        topF.grid(row=0, column=0, pady=15, padx=10)
        header = ["Card #", "New Owner", "Date Suspended", "Previous owner"]
        data = [("34567890", "Conn Man", "6/5/3", "Avery"),
                ("3456789", "Moo Daddy", "56/78/92", "Moo Son")]
        self.PassCardListBox = MultiColumnListbox(topF, header, data)

        e1 = Entry(topF)
        e1.grid(row=1, column=0, sticky=NSEW, pady=5, padx=5)
        b1 = Button(topF, text="Add Card", bg=self.bgColor1, command=self.addCard)
        b1.grid(row=1, column=1, sticky=NSEW, pady=5, padx=5)

        botF = Frame(self.passCardWin, bg=self.bgColor1)
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

        b2 = Button(botF, text="Add Value", bg=self.bgColor1, command=self.addValue)
        b2.grid(row=3, column=2, sticky=NSEW, pady=5, padx=5)

    def addValue(self):
        sql = '''Update ‘cs4400_Group_14’.’Breezecard’  
            set Value = %s 
            where BreezeCardNum = %s;
            '''
        self.cursor.execute(sql, valueNew, cardSelected)

    def addCard(self):
        sql = '''Insert into ‘cs4400_Group_14’.’Breezecard’ (‘BreezecardNum’, ‘Value’, ‘BelongsTo’) 
        values (%s, 0, %s);
        '''
        self.cursor.execute(sql, BreezeCardNum, Username)

    def tripHist(self):
        self.passHomeWin.withdraw()
        self.tripHistWin = Toplevel()
        self.tripHistWin.protocol("WM_DELETE_WINDOW", self.endProgram)
        self.tripHistWin.title("Trip History")
        self.tripHistWin.configure(bg=self.bgColor1)

        topF = Frame(self.tripHistWin, bg=self.bgColor1)
        topF.grid(row=0, column=0, pady=15, padx=10)
        l1 = Label(topF, text="Start Time", bg=self.bgColor1)
        l1.grid(row=0, column=0, sticky=NSEW, pady=5, padx=5)
        l2 = Label(topF, text="End Time", bg=self.bgColor1)
        l2.grid(row=1, column=0, sticky=NSEW, pady=5, padx=5)
        e1 = Entry(topF)
        e1.grid(row=0, column=1, sticky=NSEW, pady=5, padx=5)
        e2 = Entry(topF)
        e2.grid(row=1, column=1, sticky=NSEW, pady=5, padx=5)

        rightF = Frame(self.tripHistWin, bg=self.bgColor1)
        rightF.grid(row=0, column=2, pady=15, padx=10)
        b1 = Button(rightF, text="Update", bg=self.fgColor1, command=self.logIn)
        b1.grid(row=0, column=0, sticky=NSEW, pady=5, padx=5)
        b1 = Button(rightF, text="Reset", bg=self.fgColor1, command=self.tripHist)
        b1.grid(row=0, column=1, sticky=NSEW, pady=5, padx=5)

        botF = Frame(self.tripHistWin, bg=self.bgColor1)
        botF.grid(row=1, column=0, pady=15, padx=10)
        header = ["Card #", "New Owner", "Date Suspended", "Previous owner"]
        data = [("34567890", "Conn Man", "6/5/3", "Avery"),
                ("3456789", "Moo Daddy", "56/78/92", "Moo Son")]
        self.TripHistListBox = MultiColumnListbox(topF, header, data)

    def tripHistQuery(self):
        sql = '''SELECT
                    t2.startTime,
                    t2.source AS source,
                    Station.name AS destination,
                    t2.fare,
                    t2.bzNum
                FROM
                    (SELECT
                        t1.StartTime,
                            t1.sourceNode AS source,
                            Trip.EndsAt AS destination,
                            t1.fare,
                            t1.bzNum
                    FROM
                        (SELECT
                        Trip.StartTime,
                            Station.Name AS sourceNode,
                            Trip.Tripfare AS fare,
                            Trip.breezecardNum AS bzNum
                    FROM
                        Trip
                    INNER JOIN Station ON Station.StopID = Trip.StartsAt
                    WHERE
                        BreezecardNum = %s) AS t1
                    INNER JOIN Trip ON t1.StartTime = Trip.StartTime
                    WHERE
                        Trip.BreezecardNum = %s) AS t2
                        INNER JOIN
                    Station ON t2.destination = Station.stopID
                ORDER BY startTime DESC'''

    def logOut(self):
        self.endProgram()
        homeWin = Tk()
        self.__init__(homeWin)
        homeWin.mainloop()
        # must destroy all windows (a bunch of try excepts)
        # make logIn reappear

    def endProgram(self):
        try:
            self.cursor.close()
            self.db.commit()
            self.db.close()
            print("successfully closed like everything")
        except:
            pass
        # CLOSE EVERY WIN IN A SEPERATE TRY STATEMENT
        self.homeWin.destroy()


win = Tk()
MartaHack(win)
win.mainloop()
print("DONE!")