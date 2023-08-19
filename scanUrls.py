import requests
from itertools import product,combinations
from multiprocessing import Pool,Process,Queue,Lock
import multiprocessing
import re
from collections import Counter
import sys
DEBUGFLAG=False
def myprint(*msg, **kwargs):
	global DEBUGFLAG
	if DEBUGFLAG:
		print(*msg, **kwargs)

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def superProc(queue):
	HEADERS= {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36'}
	print("superproc started")
	while True:


		while not queue.empty():

			link=queue.get()	
			myprint(link)
			try:
				res=requests.get(link,headers=HEADERS)
				if res.status_code==200:
					print(f"{link=} exists")
					try:
						res1=re.search(r'<title>([^>]+)<\/title>',res.text)
						if res1:
							print(f"{link=} Title:{res1[1]}")


					except:
						pass

				else:
					myprint(f"{link} {res.status_code}")

			except:
				myprint("[-]Connection problems")

def main():
	global DEBUGFLAG

	queue=Queue()
	chrStr="qwertyuiopasdfghjklzxcvbnm1234567890-_"
	masks_list=[]
	wildcharlist=[]
	stringlist=[]
	all_http_results=[]
	PROC_NUM=5

	if len(sys.argv)<2:
		sys.exit(0)
	else:
		http_template=sys.argv[1]
		http_length=int(sys.argv[2])
		idxres={}
		idxres['[']=find(http_template,"[")
		idxres['(']=find(http_template,"(")
		myprint(idxres)
		order=[]
		if len(idxres['['])>0 and len(idxres['('])>0:
			while len(idxres['['])>0 and len(idxres['('])>0:
				if min(idxres['['])<min(idxres['(']):
					idxres['['].remove(min(idxres['[']))
					order.append("[")
				else:
					idxres['('].remove(min(idxres['(']))
					order.append("(")
			if len(idxres['['])>0 and len(idxres['('])==0:
				for item in idxres['[']:
					order.append("[")
			if len(idxres['('])>0 and len(idxres['['])==0:
				for item in idxres['(']:
					order.append('(')
					
			myprint(order)
			if DEBUGFLAG:
				input()
			for item in order:
				if item=='(':
					res=re.search(r"\(((?:\w+,)+\w+)\)",http_template,flags=re.I|re.M)
					if res:
						wildcharlist.append((res[1],res[1].split(",")))
						http_template=re.sub("\(((?:\w+,)+\w+)\)","!",http_template,1)

						print(wildcharlist)
						print(http_template)
						# input()
				if item=='[':
					res=re.search(r"\[(.\-.)\]",http_template,flags=re.I|re.M)	
					if res:
						myprint(res[0])
						strt,end=res[0].split("-")				
						myprint("start ",strt[1],' end ',end[0])
						charlist=''
						for ch in range(ord(strt[1]),ord(end[0])+1):
							charlist+=chr(ch)
						myprint(charlist)
						wildcharlist.append((res[0],charlist))
						myprint(wildcharlist)
						http_template=re.sub("(\[.\-.\])","!",http_template,1)
						myprint(http_template)
						if DEBUGFLAG:
							input()
		

		else:

			results=re.findall(r"\[(.\-.)\]",http_template,flags=re.I|re.M)
			totallength=1
			for res in results:
				strt,end=res.split("-")

				myprint(strt,end)
				charlist=''
				for ch in range(ord(strt),ord(end)+1):
					charlist+=chr(ch)
				myprint(charlist)
				totallength*=len(charlist)
				wildcharlist.append((res,charlist))

			print(wildcharlist)
			http_template=re.sub("(\[.\-.\])","!",http_template)

			results=re.findall(r"\(((?:\w+,)+\w+)\)",http_template,flags=re.I|re.M)
			for res in results:
				wildcharlist.append((res,res.split(",")))
			print(wildcharlist)
			http_template=re.sub("\(((?:\w+,)+\w+)\)","!",http_template)

		myprint(http_template)
		input()
		for idx,ch in enumerate(http_template):
			if ch=='*':
				delta=http_length-len(http_template)
				for i in range(1,delta+2):
					newmask=http_template.replace('*','?'*i)
					cntr=Counter(newmask)
					masks_list.append((newmask,cntr['?']))
		if len(masks_list)==0:
			masks_list.append((http_template,Counter(http_template)['?']))
		myprint(masks_list)
		# input()

		procs=[]
		for num in range(0,PROC_NUM):
			prc=Process(target=superProc,args=(queue,))
			prc.start()
			procs.append(prc)

		for mask,length in masks_list:
			all_combinations=product(chrStr,repeat=length)
			for combination in all_combinations:
				generated_string = ''.join(combination)
				resstr=mask
				for nch in generated_string:
					resstr=resstr.replace('?',nch,1)
				if wildcharlist:
					newresstr=resstr
					supercharlist=[]
					tmpres=[]
					for wldchr,chrlst in wildcharlist:
						supercharlist.append(chrlst)
					myprint("supercharlist ",supercharlist)

					results=list(product(*supercharlist))
					for item in results:
						# print(item)
						for ch in item:

							newresstr=newresstr.replace('!',ch,1)
							if not "!" in newresstr:
								myprint(newresstr)
								queue.put(newresstr)
								break
						newresstr=resstr

				else:
					if not resstr in all_http_results:
						myprint(resstr,' ',len(resstr))
						all_http_results.append(resstr)
						queue.put(resstr)
		myprint(all_http_results)

if __name__ == '__main__':
	multiprocessing.freeze_support()
	main()