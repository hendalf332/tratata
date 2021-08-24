from tkinter import *
import random
a=0
b=0
def click():
    global a
    global b
    res=entry_box.get()
    if entry_box.get()!="":
        try:
            if int(res) in range(0,100):
                photo=PhotoImage(file='.\pics\\'+ str(res) + '.gif')
                rLabel.image=photo
                rLabel.photo_ref =photo
                rLabel.config(image=photo)
                rLabel["image"]=photo
            else:
                photo=PhotoImage(file='.\pics\\no.gif')
                rLabel.image=photo
                rLabel.photo_ref =photo
                rLabel.config(image=photo)
        except ValueError:
            print('Введіть числове значення 1,2,3,...!!!')
    else:
        rLabel["text"]="Введіть відповідь!!!"
window = Tk()
window.title("Живопис")
window.geometry("500x550")
label = Label(text = "Введіть\nномер\nкартинки:")
label.place(x = 50, y = 20, width = 100, height = 55)
entry_box = Entry (text = "Jktu")
entry_box.place(x = 150, y = 20, width = 100, height = 65)
rp=random.randint(1,3)
photo=PhotoImage(file='.\pics\\'+str(rp)+'.gif')
rLabel = Label(window,image = photo)
rLabel.place(x = 260, y = 10, width = 237, height = 400)
output_box = Message(text = "text")
output_box ["bg"] = "red"
output_box ["fg"] = "white"
output_box ["relief"] = "sunken"
entry_box ["justify"] = "center"
num = entry_box.get()
button1 = Button(text = "Показати\nзображення", command = click)
button1.place(x = 160, y = 90, width = 100, height = 35)
window.mainloop()