from tkinter import *
import random
nList=[]
fname="numlist.csv"
def add_name():
    global nList
    res=entry_box.get()
    if res.isdigit():
        rLabel.insert(END,res)
        entry_box.delete(0,END)
        entry_box.focus()
    else:
        entry_box.delete(0, 'end')
        entry_box.focus()
    
def reset_sum():
    rLabel.delete(0,END)
    entry_box.focus()

def save_csv_file():
    tmp_list=rLabel.get(0,END)
    if tmp_list:
        file=open(fname,"w")
        for el in tmp_list:
            file.write(el+'\n')
        file.close()
        
window = Tk()
window.title("Список Чисел")
window.geometry("450x250")
label = Label(text = "Ціле число: ")
label.place(x = 10, y = 20, width = 100, height = 25)
entry_box = Entry (text = "Jktu")
entry_box.place(x = 100, y = 20, width = 100, height = 65)
button1 = Button(text = "Ввод числа", command = add_name)
button1.place(x = 10, y = 90, width = 110, height = 25)
rLabel = Listbox(width=150,height=200)
rLabel.place(x = 220, y = 20, width = 150, height = 200)
button2 = Button(text = "Відчишення списку", command = reset_sum)
button2.place(x = 10, y = 130, width = 110, height = 25)
button2 = Button(text = "Зберегтив в csv файл", command = save_csv_file)
button2.place(x = 10, y = 170, width = 110, height = 25)
window.mainloop()