import sqlite3
import os
def menu():
    os.system("clear")
    msg="""Main Menu
1) View phone book
2) Add to phone book
3) Search for surname
4) Delete person from
phone book
5) Quit
Enter your selection:
"""
    ans=int(input(msg))
    return ans
def main():    
    with sqlite3.connect("phonebook.db") as db:cursor=db.cursor()
    while True:
        ans=menu()
        if ans==1:
            cursor.execute("SELECT * FROM phonebook")
            for x in cursor.fetchall():
                print(x)
        elif ans==2:
            fstnm=input("Enter firstname:")
            srname=input("Enter surname:")
            number=input("Enter phonenumber:")
            if fstnm!="" and srname!="" and number!="":
                cursor.execute("""INSERT INTO phonebook(firstname, surname, phonenumber)
VALUES(?, ?, ?)""",(fstnm, srname, number))
                db.commit()
        elif ans==3:
            srname=input("Enter surname:")
            if srname!="":
                cursor.execute("""SELECT * FROM phonebook WHERE surname=?""",[srname])
                for x in cursor.fetchall():
                    print(x)
        elif ans==4:
            id=input("Enter man identificator:")
            cursor.execute("""DELETE FROM phonebook WHERE id=?""",[id])
            db.commit()
        elif ans==5:
            db.close()
            print("Good Bye!!!")
            exit()
        else:
            print('Command doesn\'t exist!!!')
        input()

main()