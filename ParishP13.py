import tkinter
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import sqlite3
###-------------------------------------------------ABOUT PROGRAM----------------------------------------------------------------------##
# ParishP13
# Programer: Aidan Parish
# Email: aparish2@cnm.edu

# Purpose: This is a GUI app that accesses a database and allows the user to make additions, subtractions, and updates to the entries
# in that database. It also displays the entries of that DataBase in a table. This program uses TKinter with TTK Treeview as the GUI framework, and 
# sqlite3 as the database framework.

# For the creation of the GUI, I referenced a youtube video by Capt. Paul DJ Oamen. Here is the URL for that video:

# https://youtu.be/dxOPaIX4qt4.

# I made manay modifications to the program that Oamen made in his video. I have entirely different variable names and different function 
# names with modified functionality. In the video, Oamen connects to a database that they made in Mysql. I decided to use sqlite3 instead, 
# so I created a DataBase initialization program which will be turned in alongside this program; as well as the actual db file for the 
# database. 

# Since the program in the video uses mysql and I am using sqlite3, I had to make several  modifcations to the code that accesses certain 
# values in my database to make it work with sqlite3. As a result, my functions are quite different.

# Additionally, the values in my database are different than the data in the video. I decided to make my database about different types of
# cars and their different specifications. Furthermore, the layout of my GUI is a little different. I had to make sizing adjustments for all
# of the frames and paddings, the MainFrame is larger to accomadate more content, and there is an additional button with additional utility 
# that the video does not include. I also have different labels and a different background color scheme.


###-------------------------------------------------GUI CONSTRUCTION----------------------------------------------------------------##

class Database_GUI_Connector:
    def __init__(self, root):
        self.root=root
        titlespace= " "
        self.root.title(120 * titlespace + "Car Specs Table")
        self.root.geometry("890x725+300+0")
        self.root.resizable(width=False, height=False)

        MainFrame=Frame(self.root, bd=10, width=770, height=700, relief=RIDGE, bg='#857ff8')
        MainFrame.grid()

        TitleFrame=Frame(MainFrame, bd=7, width=770, height=100, padx=12, relief=RIDGE)
        TitleFrame.grid(row=0, column=0)
        TopFrame=Frame(MainFrame, bd=5, width=770, height=500, relief=RIDGE)
        TopFrame.grid(row=1, column=0)

        LeftFrame=Frame(TopFrame, bd=5, width=770, height=400, padx=2, relief=RIDGE, bg='cadet blue')
        LeftFrame.pack(side=LEFT)
        LeftFrame1=Frame(LeftFrame, bd=5, width=600, height=200, padx=12, pady=43, relief=RIDGE)
        LeftFrame1.pack(side=TOP)

        RightFrame1=Frame(TopFrame, bd=5, width=100, height=400, relief=RIDGE, padx=2, bg='cadet blue')
        RightFrame1.pack(side=RIGHT)
        RightFrame2=Frame(RightFrame1,bd=5, width=90, height=300, padx=3, pady=12, relief=RIDGE)
        RightFrame2.pack(side=TOP)

        ##--------------------------------------------------VARIABLES--------------------------------------------------------------##
        
        Carmake=StringVar()
        Carmodel=StringVar()
        Horsepower=StringVar()
        Carweight=StringVar()
        Caraccel=StringVar()

        ##--------------------------------------------------FUNCTIONS--------------------------------------------------------------##

        def Exit():
            Exit = tkinter.messagebox.askyesno("Car Specs Table","Would you like to close the program?")
            if Exit>0:
                root.destroy()
                return

        def Reset_Entry_Fields():   
            self.entCarmake.delete(0, END)
            self.entCarmodel.delete(0, END)
            self.entHorsepower.delete(0, END)
            self.entCarweight.delete(0, END)
            self.entCaraccel.delete(0, END)

        def AddData():
            if Carmake.get()=="" or Carmodel.get()=="" or Horsepower.get()=="":
                tkinter.messagebox.showerror("Please enter the correct values." )
            else:
                conn=sqlite3.connect('car_records.db')
                curs=conn.cursor()
                curs.execute("INSERT INTO car_records VALUES(:carmake, :carmodel, :horsepower, :carweight, :zerotosixtytime)", 
                (Carmake.get(), 
                Carmodel.get(), 
                Horsepower.get(), 
                Carweight.get(), 
                Caraccel.get()
                ))
                conn.commit()
                conn.close()
                tkinter.messagebox.showinfo("Record Entry Form", "Record Added Successfully.")

        def DisplayData():
           
                conn=sqlite3.connect('car_records.db')
                curs=conn.cursor()
                curs.execute("SELECT * FROM car_records")
                results=curs.fetchall()
                if len(results) !=0:
                    self.car_records.delete(*self.car_records.get_children())
                    for row in results:
                        self.car_records.insert('', END, values=row)
  
                conn.commit()
                conn.close()
                
        def CarInfo(ev):
            viewInfo=self.car_records.focus()
            carData=self.car_records.item(viewInfo)
            row=carData['values']
            Carmake.set(row[0])
            Carmodel.set(row[1])
            Horsepower.set(row[2])
            Carweight.set(row[3])
            Caraccel.set(row[4])

        def Update():
            conn=sqlite3.connect('car_records.db')
            curs=conn.cursor()
            curs.execute("""UPDATE car_records SET carmake=:carmake, carmodel=:carmodel, horsepower=:horsepower, carweight=:carweight, zerotosixtytime=:zerotosixtytime WHERE carmodel=:carmodel""", ( 
            Carmake.get(),
            Carmodel.get(), 
            Horsepower.get(), 
            Carweight.get(), 
            Caraccel.get()
            ))
            conn.commit()
            DisplayData()
            conn.close()
            tkinter.messagebox.showinfo("Record Entry Form", "Record Updated Cuccessfully.")

        def Delete_from_DataBase():
            conn=sqlite3.connect('car_records.db')
            curs=conn.cursor()
            curs.execute("""DELETE FROM car_records WHERE carmodel=:carmodel""",(Carmodel.get(),))
            conn.commit()
            DisplayData()
            conn.close()
            tkinter.messagebox.showinfo("Record Delete Form", "Record Deleted From Database")
            Reset_Entry_Fields()
    
        def Search_Database_byCarMake():
            try:
                conn=sqlite3.connect('car_records.db')
                curs=conn.cursor()
                curs.execute("""SELECT * FROM car_records WHERE carmake=:carmake""", (Carmake.get(),))

                row=curs.fetchone()
            
                Carmake.set(row[0])
                Carmodel.set(row[1])
                Horsepower.set(row[2])
                Carweight.set(row[3])
                Caraccel.set(row[4])

                conn.commit()
            except:
                tkinter.messagebox.showinfo("Record Search Form", "Record Not Found")
                Reset_Entry_Fields()
            conn.close()

        def Search_Database_byCarModel():
            try:
                conn=sqlite3.connect('car_records.db')
                curs=conn.cursor()
                curs.execute("""SELECT * FROM car_records WHERE carmodel=:carmodel""", (Carmodel.get(),))

                row=curs.fetchone()
                
                Carmake.set(row[0])
                Carmodel.set(row[1])
                Horsepower.set(row[2])
                Carweight.set(row[3])
                Caraccel.set(row[4])

                conn.commit()
            except:
                tkinter.messagebox.showinfo("Record Search Form", "Record Not Found")
                Reset_Entry_Fields()
            conn.close()

        ##--------------------------------------------------WIDGETS----------------------------------------------------------------##
        
        self.lblTitle=Label(TitleFrame, font=('arial',40,'bold'), text="Car Specs Table", bd=7)
        self.lblTitle.grid(row=0, column=0, padx=205)

        self.lblCarmake=Label(LeftFrame1, font=('arial',12,'bold'), text="Car Make", bd=7)
        self.lblCarmake.grid(row=1, column=0,sticky=W, padx=5)
        self.entCarmake=Entry(LeftFrame1, font=('arial',12,'bold'), bd=5, width=44, justify='left',
        textvariable=Carmake)
        self.entCarmake.grid(row=1, column=1,sticky=W, padx=5)
        

        self.lblCarmodel=Label(LeftFrame1, font=('arial',12,'bold'), text="Car Model", bd=7)
        self.lblCarmodel.grid(row=2, column=0,sticky=W, padx=5)
        self.entCarmodel=Entry(LeftFrame1, font=('arial',12,'bold'), bd=5, width=44, justify='left',
        textvariable=Carmodel)
        self.entCarmodel.grid(row=2, column=1,sticky=W, padx=5)


        self.lblHorsepower=Label(LeftFrame1, font=('arial',12,'bold'), text="Horsepower", bd=7)
        self.lblHorsepower.grid(row=3, column=0,sticky=W, padx=5)
        self.entHorsepower=Entry(LeftFrame1, font=('arial',12,'bold'), bd=5, width=44, justify='left',
        textvariable=Horsepower)
        self.entHorsepower.grid(row=3, column=1,sticky=W, padx=5)
        

        self.lblCarweight=Label(LeftFrame1, font=('arial',12,'bold'), text="Curb Weight", bd=7)
        self.lblCarweight.grid(row=4, column=0,sticky=W, padx=5)
        self.entCarweight=Entry(LeftFrame1, font=('arial',12,'bold'), bd=5, width=44, justify='left',
        textvariable=Carweight)
        self.entCarweight.grid(row=4, column=1,sticky=W, padx=5)


        self.lblCaraccel=Label(LeftFrame1, font=('arial',12,'bold'), text="0-60 Time (seconds)", bd=7)
        self.lblCaraccel.grid(row=5, column=0,sticky=W, padx=5)
        self.entCaraccel=Entry(LeftFrame1, font=('arial',12,'bold'), bd=5, width=44, justify='left',
        textvariable=Caraccel)
        self.entCaraccel.grid(row=5, column=1,sticky=W, padx=5)

    ##----------------------------------------------TABLE TREEVIEW-------------------------------------------------------------------##
   
        scroll_y=Scrollbar(LeftFrame, orient=VERTICAL)
        scroll_x=Scrollbar(LeftFrame, orient=HORIZONTAL)
        self.car_records=ttk.Treeview(LeftFrame, height=14, columns=("Carmake","Carmodel","Horsepower","Carweight",
        "Caraccel"), yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        
            
        self.car_records.heading("Carmake", text="Car Make")
        self.car_records.heading("Carmodel", text="Car Model")
        self.car_records.heading("Horsepower", text="Horsepower")
        self.car_records.heading("Carweight", text="Curb Weight")
        self.car_records.heading("Caraccel", text="0-60 time (seconds)")

        self.car_records['show']='headings'

        self.car_records.column("Carmake", width=70)
        self.car_records.column("Carmodel", width=100)
        self.car_records.column("Horsepower", width=100)
        self.car_records.column("Carweight", width=100)
        self.car_records.column("Caraccel", width=70)

        self.car_records.pack(fill=BOTH, expand=1)
        self.car_records.bind("<ButtonRelease-1>",CarInfo) 
        #DisplayData()
    ##----------------------------------------------BUTTONS--------------------------------------------------------------------------##

        self.btnAddNew=Button(RightFrame2, font=('arial',16,'bold'), text="Add New Entry", bd=4, pady=1, padx=35,
        width=8, height=2, command=AddData).grid(row=0, column=0, padx=1)

        self.btnDisplay=Button(RightFrame2, font=('arial',16,'bold'), text="Refresh Table", bd=4, pady=1, padx=35,
        width=8, height=2, command=DisplayData).grid(row=1, column=0, padx=1)

        self.btnUpdate=Button(RightFrame2, font=('arial',16,'bold'), text="Update Entry", bd=4, pady=1, padx=35,
        width=8, height=2, command=Update).grid(row=2, column=0, padx=1)

        self.btnDelete=Button(RightFrame2, font=('arial',16,'bold'), text="Delete Entry", bd=4, pady=1, padx=35,
        width=8, height=2, command=Delete_from_DataBase).grid(row=3, column=0, padx=1)

        self.btnSearchMake=Button(RightFrame2, font=('arial',16,'bold'), text="Search by Make", bd=4, pady=1, padx=35,
        width=8, height=2, command=Search_Database_byCarMake).grid(row=4, column=0, padx=1)

        self.btnSearchModel=Button(RightFrame2, font=('arial',16,'bold'), text="Search by Model", bd=4, pady=1, padx=35,
        width=8, height=2, command=Search_Database_byCarModel).grid(row=5, column=0, padx=1)

        self.btnReset=Button(RightFrame2, font=('arial',16,'bold'), text="Reset Fields", bd=4, pady=1, padx=35,
        width=8, height=2, command=Reset_Entry_Fields).grid(row=6, column=0, padx=1)

        self.btnExit=Button(RightFrame2, font=('arial',16,'bold'), text="Exit App", bd=4, pady=1, padx=35,
        width=8, height=2, command=Exit).grid(row=7, column=0, padx=1)


    ##--------------------------------------------------END OF PROGRAM--------------------------------------------------------------------##

if __name__ =='__main__':
    root=Tk()
    application=Database_GUI_Connector(root)
    root.mainloop()
