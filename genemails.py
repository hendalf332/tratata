import random
from random import choice
from random import randint
import string
import secrets
import colorama
import os,sys
from colorama import init, Fore, Back, Style
# essential for Windows environment
init()
# all available foreground colors
FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
# all available background colors
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
# brightness values
BRIGHTNESS = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]
prevemail='z'
emails=['gmail.com','outlook.com','tutanota.com','gmx.com','yahoo.com','aol.com','mail.com','zoho.com','protonmail.com','mailerlite.com','ukr.net','mail.ru','yandex.ru']
firstnames=open('normalnames.txt','r').read().split('\n')
surnames=open('familii.txt','r').read().split('\n')

separator=['.','-','_','']
cletters=string.ascii_uppercase
        
def generate_email():
    fullname=''
    username=''
    global emails,firstnames,surnames,separator,cletters
    global prevemail
    for _ in range(randint(3,9)):
        username+=secrets.choice(string.ascii_lowercase)    
    typ=randint(1,9)
    fstnm=choice(firstnames)
    sndname=choice(surnames)
    if fstnm.endswith('a') and not ( sndname.endswith('a') or sndname.endswith('o')):
        sndname+='a'
    if not fstnm.endswith('a') and sndname.endswith('a'):
        sndname=sndname[:-1]
    if typ==1:
        fullname=fstnm+choice(separator)+sndname+'@'+choice(emails)
    elif typ==2:
        fullname=choice(cletters)+choice(separator)+choice(surnames)+'@'+choice(emails)
    elif typ==3:
        fullname=fstnm+choice(separator)+sndname+choice(separator)+ str(randint(1900,2030))+'@'+choice(emails)
    elif typ==4:
        fullname=fstnm+choice(separator)+ str(randint(1900,2030))+'@'+choice(emails)   
    elif typ==5:
        fullname=choice(cletters)+ choice(surnames)+choice(separator)+ str(randint(1900,2030)) +'@'+choice(emails) 
    elif typ==6:
        fullname=choice(firstnames)+choice(separator)+ username +'@'+choice(emails)
    elif typ==7:
        fullname=fstnm+username+ sndname +'@'+choice(emails)  
    elif typ==8:
        fullname=choice(surnames)+ choice(separator) + username +'@'+choice(emails)    
    if prevemail!=fullname:
        prevemail=fullname
        return fullname
    else:
        prevemail=fullname
        return None

def print_with_color(s, color=Fore.WHITE, brightness=Style.NORMAL, **kwargs):
    """Utility function wrapping the regular `print()` function 
    but with colors and brightness"""
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)


def main():
    cnt=0
    # num=input('Введіть кількість емейлів:')
    num=int(sys.argv[1])
    print('')
    print('*'*80)
    print('')
    while cnt<num:
        email=generate_email()
        if email:
            print_with_color(email, color=Back.RED+Fore.CYAN, brightness=Style.BRIGHT)
            cnt+=1
    print('')
    print('*'*80)
    print('') 
   
if __name__ == '__main__':
    main()