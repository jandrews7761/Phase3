from tkinter import *
import pymysql

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

    def logIn(self):
        pass
        # add code and sql here to determine if credentials match an account
        # if not, message an error back
        # if so, ascertain admin or reg user
        # withdraw homewin, and call either self.passHome() or self.adminHome()

    def register(self):
        # withdraw home window and create a new register window
        # the register button must call a registerNewUser method
        pass

    def registerNewUser(self):
        # add code to check if entries are valid
        # if not error
        # if so, try to insert into db with mysql, catch pass
        # if all successfull, message "account created"
        # withdraw (destroy?) register win, call passHome if all successfull
        pass

    def adminHome(self):
        # create adminHome page
        # buttons to call self.adminStationMgt, self.adminSuspMgt,
            # self.adminCardMgt,self.pflowReport, self.logOut
        pass

    def passHome(self):
        # buttons to call self.cardMgt, self.tripHist, self.logOut
        pass

    def adminStationMgt(self):
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
