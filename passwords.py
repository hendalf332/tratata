import os
import string
import csv
from os.path import exists as file_exists
import sys, readchar

def passprompt(prompt: str, out = sys.stdout) -> str:
    out.write(prompt); out.flush()
    password = ""
    while True:
        ch = str(readchar.readchar(), encoding='UTF-8')
        if ch == '\r':
            break
        elif ch == '\b':
            out.write('\b \b')
            password = password[0:len(password)-1]
            out.flush()
        else: 
            password += ch
            out.write('X')
            out.flush()
    print('\n')
    return password

fname="passwords.csv"
symb_list=['!', '£', '$', '%', '&','<','*','@','.']
lc_list=list(string.ascii_lowercase)
uc_list=list(string.ascii_uppercase)
dig_list=['0','1','2','3','4','5','6','7','8','9']

userList=[]
passList=[]
def importFile(): 
    if file_exists(fname):

        file = list(csv.reader(open(fname)))
        for row in file:
            userList.append(row[0])
            passList.append(row[1])
    else:
        print(f'File {fname} doesn\'t exist')
        file=open(fname,"w")
        file.close()
    # file.close()
    
    
def storeInFile():
    file=open(fname,"w")
    idx=0
    for user in userList:
        file.write(user+','+passList[idx]+'\n')
        idx+=1
    file.close()
def checkPass(password):
    passScore=0
    if len(password)>=8:
        passScore=1
    symbFlag=False
    lcFlag=False
    ucFlag=False
    digFlag=False
    for symb in symb_list:
        if symb in password:
            symbFlag=True
    for lcs in lc_list:
        if lcs in password:
            lcFlag=True  
    for ucs in uc_list:
        if ucs in password:
            ucFlag=True
    for dcs in dig_list:
        if dcs in password:
            digFlag=True
    if symbFlag==True:
        passScore+=1
    if lcFlag==True:
        passScore+=1 
    if ucFlag==True:
        passScore+=1
    if digFlag==True:
        passScore+=1 
    if passScore<3:
        print('PASSWORD is WEAK try again')
        return -1
    elif passScore<5:
        ans=input('\nYou password can be better Do you want to improve your password (y/n)?')
        if ans=='n':
            return 1
        else:
            return -1
    else:
        print('Your password is strong!!!')
        return 1


def new_identity(newID):
    if newID in userList:
        while newID in userList:
            newID=input('Enter new ID:')
    newPass=passprompt(f'Enter new password for user {newID}:')
    cPassRes=checkPass(newPass)
    while cPassRes<0:
        newPass=passprompt(f'Enter new password for user {newID}:')
        cPassRes=checkPass(newPass)
    confirmFlag=False
    cnt=0
    while confirmFlag==False and cnt<3:
        pass2=passprompt(f'Confirm new password for user {newID}:')
        if pass2==newPass:
            confirmFlag=True
        else:
            print('You typed wrong password try again!!!')
            cnt+=1
    if confirmFlag==False:
        return -1
    userList.append(newID) 
    passList.append(newPass)
    file=open(fname,"a")
    file.write(newID+','+newPass+'\n')
    file.close()
    
def menu():
    msg="""1) Create a new User ID
2) Change a password
3) Display all User IDs
4) Quit
Enter Selection:
"""
    try:
        ans=int(input(msg))
    except ValueError:
        print('Please enter integer value from menu 1,2 or 3!!!')
        return 0
    return ans
    
def main():
    os.system("clear")
    encstr=''
    importFile()
    while True:
        ans=menu()
        if ans==1:
            print('Create a new User ID')
            id=input('Enter a new ID:')
            new_identity(id)
            #storeInFile()
        elif ans==2:
            print('Changing PASSWORD!!!')
            uid=input('Enter User ID:')
            if uid in userList:
                flag=False
                while flag==False:
                    newPass=passprompt(f'Enter new password for user {uid}:')
                    prevpass=passList[userList.index(uid)]
                    if prevpass!=newPass:
                        flag=True
                    else:
                        print('Sorry but password the same!!!')
                    cPassRes=checkPass(newPass)
                    while cPassRes<0:
                        newPass=passprompt(f'Enter new password for user {uid}:')
                        cPassRes=checkPass(newPass)
                confirmFlag=False
                cnt=0
                while confirmFlag==False and cnt<3:
                    pass2=passprompt(f'Confirm new password for user {uid}:')
                    if pass2==newPass:
                        confirmFlag=True
                    else:
                        print('You typed wrong password try again!!!')
                        cnt+=1
                if confirmFlag==True:
                    passList[userList.index(uid)]=newPass
                storeInFile()
            else:
                print('Sorry Identificator doesn\'t exist!!!')
        elif ans==3:
            for idr in userList:
                print(idr)

        elif ans==4:
            print('Good Bye!!!')
            exit()
        else:
            print('Enter correct code 1,2 or 3 !!!')
        input()
        os.system("clear")
main()