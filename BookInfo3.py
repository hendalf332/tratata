import sqlite3
fname="books.txt"
with sqlite3.connect("bookinfo.db") as db:cursor=db.cursor()

aName=input("Введіть ім'я автора:")

cursor.execute("""SELECT * FROM Books WHERE Author=?""",[aName])
rec=""
file=open(fname,"w")
for el in cursor.fetchall():
    for x in el:
        rec=rec + str(x) + ' - '
    rec=rec[:-2]
    file.write(rec+'\n')
    print(rec)
    rec=''
file.close()
db.close()