#!/usr/bin/env python

import csv
strings=['To Kill a Mockingbird, Harper Lee, 1960\n',
'A Brief History of Time, Stephen Hawking, 1988\n',
'The Great Gatsby F., Scott Fitzgerald, 1922\n',
'The Man Who Mistook His Wife for a Hat, Oliver Sacks, 1985\n',
'Pride and Prejudice, Jan Austen, 1813\n'
]

fname='Books.csv'
file=open(fname,'w')
for el in strings:
    file.write(str(el))
file.close()

rec=''
bname=input('Введіть\n\tНазва книги:')
author=input('\tАвтор книги:')
year=input('\tРік випуску книги:')
rec=bname + ', ' +author+', '+year+'\n'
file=open(fname,'a')
file.write(str(rec))
file.close()

books=''
file2=open(fname,'r')
books=file2.read()
file2.close()
print('-'*90+'\n')
print(books)
exit()

