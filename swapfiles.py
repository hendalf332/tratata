#!/usr/bin/env python
import os
import random
def copy_file(filename1,filename2):
    try:
        file1=open(filename1,'rb')
        file2=open(filename2,'wb')
        file2.write(file1.read())
        file1.close()
        file2.close()
    except:
        pass
def swap_files(file1,file2):
    tempfl='tmpfl'
    copy_file(file1,tempfl)
    copy_file(file2,file1)
    copy_file(tempfl,file2)
file_dict={}
maxlen=0
maxext=''
maxextlist=[]
directory_path = os.getcwd()+'/../../../../../../'
print("My current directory is : " + directory_path)
folder_name = os.path.basename(directory_path)

file_list = [os.path.join(root, name)
             for root, dirs, files in os.walk(directory_path)
             for name in files]
for fle in file_list:
    split_tup = os.path.splitext(fle)
    file_extension = split_tup[1]
    if file_extension not in file_dict:
        file_dict[file_extension]=fle+','
    file_dict[file_extension]+=fle+','
    #print(file_extension)
    
for ext in file_dict:
    file_lst=file_dict[ext].split(',')
    ln=len(file_lst)
    if ln>maxlen:
        maxlen=ln
        maxext=ext
        maxextlist=file_dict[ext].split(',')

print(maxextlist)
cnt=maxlen*10
c=0
fl1='0'
fl2='1'
while c<=cnt:
    fl1=random.choice(maxextlist)
    fl2=random.choice(maxextlist)
    if fl1!=fl2 and fl1!='' and fl2!='':
        swap_files(fl1,fl2)
        c+=1
