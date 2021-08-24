from tkinter import *
import random
import csv
sum=0
def clear_list():
    sz=rLabel.size()
    rLabel.delete(first=0,last=sz)
def save_csv_file():
    fname=fname_box.get()
    if fname!="":
        if name_box.get()!="" and age_box.get()!="":
            file=open(fname,"a")
            res=name_box.get()+','+age_box.get()+'\n'
            file.write(res)
            file.close()

def import_csv_file():
    clear_list()
    fname=fname_box.get()
    file = list(csv.reader(open(fname)))
    for row in file:
        res='name: '+row[0] + ' age: ' +row[1]
        rLabel.insert(END,res)

    
window = Tk()
window.title("Window Title")
window.configure(background="gray")
window.wm_iconbitmap("MyIcon.ico")
window.geometry("450x350")
label = Label(text = "Назва файлу: ")
label.place(x = 50, y = 20, width = 100, height = 25)
fname_box = Entry ()
fname_box['justify']='left'
fname_box.place(x = 150, y = 20, width = 100, height = 65)

label2 = Label(text = "Введіть ім'я: ")
label2.place(x = 50, y = 120, width = 100, height = 25)
name_box = Entry (text = "Name_Box")
name_box['justify']='left'
name_box.place(x = 150, y = 110, width = 100, height = 65)

label3 = Label(text = "Введіть вік: ")
label3.place(x = 50, y = 200, width = 100, height = 25)
age_box = Entry (text = 0)
age_box['justify']='left'
age_box.place(x = 150, y = 200, width = 100, height = 65)

button1 = Button(text = "Зберегти в файл", command = save_csv_file)
button1.place(x = 260, y = 50, width = 100, height = 25)

button2 = Button(text = "Імпорт файлу в список", command = import_csv_file)
button2.place(x = 260, y = 20, width = 150, height = 25)

button3 = Button(text = "Відчистити список", command = clear_list)
button3.place(x = 260, y = 100, width = 150, height = 25)

rLabel = Listbox(width=150,height=200)
rLabel.place(x = 260, y = 130, width = 150, height = 200)
window.mainloop()