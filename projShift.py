import os
import string
alphabet=list(string.ascii_lowercase)
alphabet.append(' ')
alphabet_upper=list(string.ascii_uppercase)
punct=list(string.punctuation)
for x in range(0,9):
    punct.append(str(x))
def menu():
    msg="""1) Make a code
2) Decode a message
3) Quit
Enter your selection:
"""
    try:
        ans=int(input(msg))
    except ValueError:
        print('Please enter integer value from menu 1,2 or 3!!!')
        return 0
    return ans

def encode(str,num):
    res=''
    num=num%len(alphabet)
    for symb in str:
        if symb in alphabet:
            pos=(alphabet.index(symb)-alphabet.index('a'))
            if (pos+num)>=len(alphabet):
                res=res+alphabet[(pos+num)%len(alphabet)]
            else:
                res=res+alphabet[pos+num]
        elif symb in alphabet_upper:
            pos=(alphabet_upper.index(symb)-alphabet_upper.index('A'))
            if (pos+num)>=len(alphabet_upper):
                res=res+alphabet_upper[(pos+num)%len(alphabet_upper)]
            else:
                res=res+alphabet_upper[pos+num]
        elif symb in punct:
            pos=(punct.index(symb)-punct.index('!'))
            if (pos+num)>=len(punct):
                res=res+punct[(pos+num)%len(punct)]
            else:
                res=res+punct[pos+num]
    return res
    
def decode(str,num):
    res=''
    num=num%len(alphabet)
    for symb in str:
        if symb in alphabet:
            pos=(alphabet.index(symb)-alphabet.index('a'))
            if (pos-num)<0:
                res=res+alphabet[len(alphabet)+(pos-num)]
            else:
                res=res+alphabet[pos-num]
        elif symb in alphabet_upper:
            pos=(alphabet_upper.index(symb)-alphabet_upper.index('A'))
            if (pos-num)<0:
                res=res+alphabet_upper[len(alphabet_upper)+(pos-num)]
            else:
                res=res+alphabet_upper[pos-num]
        elif symb in punct:
            pos=(punct.index(symb)-punct.index('!'))
            if (pos-num)<0:
                res=res+punct[len(punct)+(pos-num)]
            else:
                res=res+punct[pos-num]
    return res

def main():
    print(string.ascii_lowercase)
    os.system("clear")
    encstr=''
    while True:
        ans=menu()
        if ans==1:
            print('Make a code')
            str=input('Enter string:')
            key=int(input('Enter key:'))
            encstr=encode(str,key)
            print(encstr)
        elif ans==2:
            print('Decode message!!!')
            dec_str=input('Enter encrypted string:')
            dec_key=int(input('Enter decode key:'))
            str=decode(dec_str,dec_key)
            print(str)
        elif ans==3:
            print('Good bye!!')
            exit()
        else:
            print('Enter correct code 1,2 or 3 !!!')
        input()

main()