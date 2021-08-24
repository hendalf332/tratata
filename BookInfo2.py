import sqlite3

with sqlite3.connect("bookinfo.db") as db:cursor=db.cursor()

print("Список авторов с местами рождения:")
cursor.execute("""SELECT * FROM Authors""")
for x in cursor.fetchall():
    print(x)
 
placeOfBirth=input("Введите место рождения автора:")
cursor.execute("""SELECT title,DatePublished,Author FROM Books,Authors WHERE Books.Author=Authors.name AND Authors.PlaceOfBirth=?""",[placeOfBirth])
for x in cursor.fetchall():
    print(x)

year=int(input("Введіть рік видання:"))
cursor.execute("""SELECT * FROM Books WHERE DatePublished>? ORDER BY DatePublished""",[year])
for x in cursor.fetchall():
    print(x)
db.close()