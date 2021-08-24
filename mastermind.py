#!/usr/bin/env python
import random
colors=["aqua", "black",  "blue",  "blueviolet",  "brown", "cyan",  "darkblue", "green" ,"pink",  "plum",  "powderblue",  "purple", "red", "silver", "snow", "violet",  "wheat",  "white",  "whitesmoke","yellow","yellowgreen"]

def generate_randlst():
    randlst=[]
    for i in range(0,4):
        randlst.append(random.choice(colors))
    return randlst
    
def main():
    print('Colors: '+str(colors))
    randlst=generate_randlst()
    ulist=[]
    attempt=0
    correct_list=[]
    incorrect_list=[]
    while True:
        while True:
            flag=True
            ulist=list(map(str, input("Enter list of 4th colors:").lower().split()))
            for el in ulist:
                if el not in colors:
                    flag=False
            if flag==True:
                break
            else:
                print('Enter correct color form list colors '+str(colors))
                    
        attempt+=1
        score=0
        cnt=0
        
        for clr in ulist:
            if clr in randlst:
                if ulist[cnt]==randlst[cnt]:
                    score+=1
                    correct_list.append(clr)
                    while True:
                        if clr in incorrect_list:
                            incorrect_list.remove(clr)
                        else: 
                            break
                else:
                    if clr not in correct_list:
                        incorrect_list.append(clr)

            cnt+=1
        print(f'[+]Colors in correct position {len(correct_list)}')
        print(f'[-]Colors in incorrect position {len(incorrect_list)}')
        del ulist[:]
        del correct_list[:]
        del incorrect_list[:]
        if score==4:
            print(f'You have won!!!\nNumber of attempts {attempt=}')
            break
        else:
            score=0
        
main()