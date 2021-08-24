from tkinter import *
import sqlite3
import random
with sqlite3.connect("TestScores.db") as db:cursor=db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS TestScores(id integer PRIMARY KEY,StudentsName text NOT NULL,sgrade integer NOT NULL);""")

def addToDatabase():
    sname=sname_box.get()
    sgrade=sgrade_box.get()
    if sname!="" and sgrade!="":
        cursor.execute("""SELECT * FROM TestScores WHERE StudentsName=?""",[sname])
        res=cursor.fetchall()
        if res:
            print('Такий студент ' + sname + ' вже існує!!!')
            cursor.execute("UPDATE TestScores SET sgrade=? WHERE StudentsName=?",(sgrade,sname))
            db.commit()
        else:
            print(sname+' Студента ще немає створимо нового!!!')
            cursor.execute("""INSERT INTO TestScores(StudentsName, sgrade)
VALUES(?,?)""",(sname,sgrade))
            db.commit()
def clearClick():
    sname_box.delete(0,END)
    sgrade_box.delete(0,END)
    sname_box.focus()
window = Tk()
window.title("TestScores")
window.geometry("450x150")
label = Label(text = "Enter Student's name: ")
label.place(x = 30, y = 20, width = 110, height = 25)
sname_box = Entry (text = "")
sname_box.place(x = 150, y = 20, width = 120, height = 25)

rLabel = Label(text = "Enter Student's grade:" )
rLabel.place(x = 30, y = 50, width = 120, height = 40)
sgrade_box = Entry (text = "Enter Student's grade")
sgrade_box.place(x = 150, y = 60, width = 120, height = 25)

sname_box ["justify"] = "left"
sgrade_box ["justify"] = "left"
num = sname_box.get()



AddButton = Button(text = "Add", command = addToDatabase)
AddButton.place(x = 100, y = 90, width = 80, height = 25)

ClearButton = Button(text = "Clear", command = clearClick)
ClearButton.place(x = 200, y = 90, width = 80, height = 25)
window.mainloop()