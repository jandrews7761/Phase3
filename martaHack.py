from tkinter import *
from tkinter import messagebox
import pymysql
import hashlib
import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import csv


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
            print(isAdmin)
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
        if self.usrE.get() == "":
            failed = True
            messagebox.showerror("No Username Provided","Enter a username")
        elif self.pass1e.get() != self.pass2e.get() :
            failed = True
            messagebox.showerror("Password Mismatch","Check that both passwords are identical")
        elif len(self.pass1e.get()) < 8:
            failed = True
            messagebox.showerror("Password too short","Password needs to be at least eight characters")
        elif len(self.bzNumE.get()) != 16 and self.v == "True":
            failed = True
            messagebox.showerror("Invalid Buzzcard","Buzzcard must be 16 characters")
        # CHECK FOR EMAIL ADDRESS VALIDITY
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
                        Brezecard
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
            if self.v == "True":
                c2 = self.cursor.execute(sql2,(self.bzNumE.get()))
                if c2 >= 1:
                    autoGen = True
                    # SUSPEND THE BUZZCARD
                else:
                    bzNum = self.bzNumE.get()
            elif self.v == "False" or autoGen:
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
                messagebox.showinfo("Success","Account successfully created")
                self.db.commit()
                self.regWin.destroy()
                self.passHome()
            except:
                messagebox.showerror("An Error Occured","Please check your network connection and try again")

    def autoGenerate(self):
        # AUTO GENERATE A NUMBER HERE
        bzNum = 1234567891234568
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
        self.adminHomeWin = Toplevel()
        self.adminHomeWin.title("Administer Home")

        b1 = Button(self.adminHomeWin,text="Passenger Flow Report", command = self.pFlowReport,bg=self.fgColor1)
        b1.pack()

        b2 = Button(self.adminHomeWin,text="Suspended Cards", command=self.adminSuspMgt,bg=self.fgColor1)
        b2.pack()

        b3 = Button(self.adminHomeWin,text= "Breeze Card Management", command = self.adminCardMgt,bg=self.fgColor1)
        b3.pack()

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
        pass

    def viewStation(self):
        pass

    def createStation(self):
        pass

    def adminSuspMgt(self):
        self.adminHomeWin.withdraw()
        self.aSusWin = Toplevel()
        self.aSusWin.protocol("WM_DELETE_WINDOW", self.endProgram)
        self.aSusWin.title("Suspended Cards")
        self.aSusWin.configure(bg=self.bgColor1)

        topF = Frame(self.aSusWin, bg=self.bgColor1)
        topF.grid(row=0, column=0, pady=15, padx=10)
        listbox = Listbox(topF)
        listbox.pack()
        currencies = {}

        # with open('Try2.csv') as f:
        #     next(f, None)  # Skip the header.
        #     reader = csv.reader(f, delimiter=',')
        #     for Card, Value, Owner in reader:
        #         currencies[f'{Card} {Value} {Owner}'] = Card
        #
        # for key in currencies:
        #     listbox.insert('end', key)
        # listbox.grid(row=0, column=0)
        # listbox.bind('<Key-Return>', lambda event: print(currencies[listbox.selection_get()]))

        botF = Frame(self.aSusWin, bg=self.bgColor1)
        botF.grid(row=1, column=0, pady=15, padx=10)
        b1 = Button(botF, text="Assign Selected Card to New Owner", bg=self.fgColor1, command=self.logIn)
        b1.grid(row=1, column=1, sticky=NSEW, pady=5, padx=5)
        b2 = Button(botF, text="Assign Selected Card to Previous Owner", bg=self.fgColor1, command=self.tripHist)
        b2.grid(row=2, column=1, sticky=NSEW, pady=5, padx=5)
        l1 = Label(botF, text="Assigning the card to an owner will unlock all accounts conflicted on the same Breeze Card.", bg=self.bgColor1)
        l1.grid(row=3, column=1, sticky=NSEW, pady=5, padx=5)

    def adminCardMgt(self):
        self.adminHomeWin.withdraw()
        self.aCardWin = Toplevel()
        self.aCardWin.protocol("WM_DELETE_WINDOW", self.endProgram)
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
        rightF.grid(row=0, column=2, pady=15, padx=10)
        b1 = Button(rightF, text="Reset", bg=self.fgColor1, command=self.logIn)
        b1.grid(row=1, column=1, sticky=NSEW, pady=5, padx=5)
        b2 = Button(rightF, text="Update Filter", bg=self.fgColor1, command=self.tripHist)
        b2.grid(row=2, column=1, sticky=NSEW, pady=5, padx=5)
        self.v = StringVar()
        self.v.set("False")
        rb1 = Radiobutton(rightF, text="Show Suspended Cards", variable=self.v, value="True", bg=self.fgColor1)
        rb1.grid(row=0, column=0, columnspan=2, pady=5, padx=5, sticky=NSEW)

        botF = Frame(self.aCardWin, bg=self.bgColor1)
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

        # with open('Try2.csv') as f:
        #     next(f, None)  # Skip the header.
        #     reader = csv.reader(f, delimiter=',')
        #     for Card, Value, Owner in reader:
        #         currencies[f'{Card} {Value} {Owner}'] = Card
        #
        # for key in currencies:
        #     listbox.insert('end', key)
        # listbox.grid(row=0, column=0)
        # listbox.bind('<Key-Return>', lambda event: print(currencies[listbox.selection_get()]))

    def pFlowReport(self):
        self.adminHomeWin.withdraw()
        self.pFlowWin=Toplevel()
        self.pFlowWin.title("Passenger Flow Report")
        self.pFlowWin.protocol("WM_DELETE_WINDOW",self.endProgram)
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
        b3 = Button(topF,text="Home",bg=self.fgColor1, command= self.goToAdminHome, width=8)
        b3.grid(row=1,column=4,rowspan=2,pady=5,padx=10,sticky=EW)

        self.startTimeE = e1
        self.endTimeE = e2

    def pFlowRevert(self):
        self.pFlowWin.destroy()
        self.pFlowReport()

    def pFlowUpdate(self):
        # CHECK FOR VALID DATETIMES
        data = self.pFlowQuery()
        # POPULATE TABLE WITH VALUES

    def pFlowQuery(self):
        sql = '''SELECT
                    t1.statName AS StationName,
                    t1.flowOut AS flowOut,
                    COUNT(Trip.BreezeCardNum) AS flowIn,
                    COUNT(trip.breezecardNum) - t1.flowOut AS flow,
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
                        trip.startTime >= %s
                            AND trip.startTime <= %s
                    GROUP BY Trip.StartsAt) AS t1
                        INNER JOIN
                    trip ON t1.startID = trip.endsAt
                WHERE
                    trip.startTime >= %s
                        AND trip.startTime <= %s
                GROUP BY StationName'''
        c = cursor.execute(sql,(self.startTimeE.get(), self.endTimeE.get(), self.startTimeE.get(), self.endTimeE.get()))
        return list(cursor.fetchall())

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
        listbox = Listbox(topF)
        listbox.pack()
        currencies = {}

        # with open('Try2.csv') as f:
        #     next(f, None)  # Skip the header.
        #     reader = csv.reader(f, delimiter=',')
        #     for Card, Value, Owner in reader:
        #         currencies[f'{Card} {Value} {Owner}'] = Card
        #
        # for key in currencies:
        #     listbox.insert('end', key)
        # listbox.grid(row=0, column=0)
        # listbox.bind('<Key-Return>', lambda event: print(currencies[listbox.selection_get()]))


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
        pass

    def addCard(self):
        pass

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
        listbox = Listbox(botF)
        listbox.pack()
        currencies = {}

        # with open('Try.csv') as f:
        #     next(f, None)  # Skip the header.
        #     reader = csv.reader(f, delimiter=',')
        #     for Fare, Start, Number, TimeS, TimeE in reader:
        #         currencies[f'{Fare} {Start} {Number} {TimeS} {TimeE}'] = Start

        # for key in currencies:
        #     listbox.insert('end', key)
        # listbox.grid(row=0, column=0)
        # listbox.bind('<Key-Return>', lambda event: print(currencies[listbox.selection_get()]))

        # table = [start]
        #
        # headers = ["Time", "Source", "Destination", "Fare", "Card #"]
        #
        # row_format = "{:<8}  {:>8}  {:<8}  {:8}"
        # listbox.insert(0, row_format.format(*headers, sp=" " * 2))
        # for items in table:
        #     listbox.insert(END, row_format.format(*items, sp=" " * 2))

    def tripHistQuery(self):
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
        # CLOSE EVERY WIN IN A SEPERATE TRY STATEMENT
        self.homeWin.destroy()


win = Tk()
MartaHack(win)
win.mainloop()
print("DONE!")
