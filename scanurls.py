import argparse
import os
import requests
from itertools import product,combinations
from multiprocessing import Pool,Process,Queue,Lock
import multiprocessing
import re
from collections import Counter
import sys
DEBUGFLAG=False
HELP_MSG=f"""
USAGE python {sys.argv[0]} -t <URLTEMPLATE> -l <MAXIMUMLENGTHOFURL> -d <PATH_OR_LINK_TO_DICTIONARY>
Template format:
? - any key supported in url domain names
* - expands to number of ?(anycharacters) according to <MAXIMUMLENGTHOFURL> parameter
if there is no * <MAXIMUMLENGTHOFURL> can be missed
[a-z] - characters range can be any characters supported in url domain names addresses
[a-z]{chr(0x7b)}1,3{chr(0x7d)} - quantifiers which correspond to 3 characters from range of characters 
(mega|test|porno|tube) - any word from list choose from alternatives like in regular expressions
						alternatives also supports quantifiers like characters ranges
$ - will be replaced by each word from the dictionary link or path to the dictionary -d option					

EXAMPLES:
python {sys.argv[0]} -t 'https://base[0-9]{chr(0x7b)}0,3{chr(0x7d)}.(com|org|net)' -l 44
python {sys.argv[0]} -t 'https://[a-z]ou?ube[0-9]{chr(0x7b)}0,3{chr(0x7d)}.com' -l 44
python {sys.argv[0]} -t 'https://anywebsite.com/$' -d https://github.com/trickest/wordlists/raw/main/technologies/bagisto-all-levels.txt 
"""

template_list=list()

def get_arguments():
    parser=argparse.ArgumentParser(HELP_MSG)
    parser.add_argument('-t', required=True, default=None,dest='http_template',help='<URLTEMPLATE>')
    parser.add_argument('-l', required=False, default=None,dest='http_length',help='<MAXURLLENGTH>')
    parser.add_argument('-d', required=False, default=None,dest='dictionary',help='Dictionary(PATH|URL)')

    options = parser.parse_args()
    if not options.http_template:
        parser.error("[-] Please specify an URL TEMPLATE, use --help for more info")
    return options

def myprint(*msg, **kwargs):
	global DEBUGFLAG
	if DEBUGFLAG:
		print(*msg, **kwargs)

def myinput(*msg, **kwargs):
	global DEBUGFLAG
	if DEBUGFLAG:
		input(*msg, **kwargs)

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def superProc(queue):
	HEADERS= {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36'}
	myprint("superproc started")
	while True:


		while not queue.empty():

			link=queue.get()	
			myprint(link)
			if link.startswith('TERMINATE'):
				print('superproc TERMINATED')
				return
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

def caluclate_order(mystr):
	idxres={}
	idxres['[']=find(mystr,"[")
	idxres['(']=find(mystr,"(")
	myprint(idxres)	
	order=[]
	idxres['[']=find(mystr,"[")
	idxres['(']=find(mystr,"(")
	myprint(idxres)
	order=[]
	if len(idxres['['])>0 or len(idxres['('])>0:
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
	return order	

def reformat_httptemplate(http_template):
	http_template_list=[]
	global template_list
	wildcharlist=[]
	strt,end=[],[]
	res=re.search(r'(\(\?(?:[^()]+\|)+[^()]+\))',http_template,flags=re.I|re.M)
	if res:
		items=res[1][2:-1].split('|')
		for item in items:
			myprint(item)
			new_template=re.sub(r'(\(\?(?:[^()]+\|)+[^()]+\))',item,http_template,1)
			myprint(new_template)
			http_template_list.append([new_template,caluclate_order(new_template)])
			http_template_list= reformat_httptemplate(new_template)			
		#http_template = re.sub('(\(\?(?:[^()]+\|)+[^()]+\))',"",http_template,1)
		myprint(http_template)
		myprint(http_template_list)
		# input()
	res=re.search(r"(\[.\-.\]|\((?:[^()]+\|)*[^()]+\))(\{(?:\d\,)?\d\})",http_template,flags=re.I|re.M)	
	if res:
		strtnum,endnum=1,1
		myprint(res[0])
		myprint("startposition ", res.start())
		if res[0][0]=='[':
			strt,end=res[0].split("-")
		
		if res[2]:
			myprint(res[2][1:-1])
			if "," in res[2]:
				strtnum,endnum=map(int,res[2][1:-1].split(","))
			else:
				strtnum=endnum=int(res[2][1:-1])
			# myprint("start ",strt[1],' end ',end[0])
		myprint(strtnum,endnum)
		charlist=''
		if res[0][0]=='[':
			for ch in range(ord(strt[1]),ord(end[0])+1):
				charlist+=chr(ch)
			myprint(charlist)
			for it in range(0,endnum):
				wildcharlist.append((res[1],charlist))
		elif res[0][0]=='(':
			myprint('( Skobki',res[2])
			for it in res[1][1:-1].split('|'):
				wildcharlist.append((res[1],it))
		myprint(wildcharlist)
		if res[2]:
			for it in range(strtnum,endnum+1):
				http_template_list.append(http_template)
				myprint("res*it:",res[1]*it," it=",it," startnum ",strtnum,' endnum ',endnum)
				http_template_list[-1]=re.sub("(\[.\-.\]|\((?:[^()]+\|)*[^()]+\))(\{(?:\d\,)?\d\})",res[1]*it,http_template_list[-1],1)
		else:
			http_template=re.sub("(\[.\-.\]|\((?:[^()]+\|)*[^()]+\))(\{(?\d\,)?\d\})","!",http_template,1)
			http_template_list.append(http_template)
		myprint(http_template)
		for idx,item in enumerate(http_template_list):
			order=caluclate_order(item)
			myprint("order")
			myprint(order)
			myprint(f"item: {item}")
			http_template_list[idx]=[item,order]
			if not "{" in item:
				template_list.append([item,order])
	else:
		order=caluclate_order(http_template)
		template_list.append([http_template,order])


	myprint(http_template_list)
	for item,order in http_template_list:				
		if "{" in item:
			myprint(f"bracket in {item}")
			http_list=reformat_httptemplate(item)
	myprint(http_template_list)
	return http_template_list

def main():
	global DEBUGFLAG
	HEADERS= {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36'}
	queue=Queue()
	chrStr="qwertyuiopasdfghjklzxcvbnm1234567890-_"
	masks_list=[]
	wildcharlist=[]
	stringlist=[]
	all_http_results=[]
	supercharlist=[]
	http_template_list=[]
	word_list=list()
	word_dictionary=None
	PROC_NUM=5
	numbcomb=1 #number of possible urls 
	wordCounter=0
	wordProduct=None
	options=get_arguments()
	http_template=options.http_template
	if not options.http_length:
		http_length=44

	else:
		http_length=options.http_length
	if options.dictionary:
		word_dictionary=options.dictionary
	if word_dictionary:
		if re.match(r'^(https?|ftp)',word_dictionary):
			res=requests.get(word_dictionary,headers=HEADERS)
			if res.status_code==200:
				word_list=res.text.split('\n')
			else:
				print('[-] The dictionary incorrect')	
				return

		elif os.path.exists(word_dictionary):
			word_list=open(word_dictionary,'r',encoding='utf-8').read().split('\n')	
		else:
			word_dictionary=None
			print('[-] The dictionary incorrect')
			return
		word_list=list(set(word_list))
		word_list=[re.sub(r"\d+","",el) for el in word_list if len(el.strip())>2 ]
		wordCounter=Counter(http_template)
		wordCounter=wordCounter['$']
		myprint(wordCounter)
		wordProduct=iter(product(word_list,repeat=wordCounter))
		myinput()
	order=caluclate_order(http_template)
				
	myprint(order)
	http_template_list=reformat_httptemplate(http_template)
	myprint(template_list)
	http_template_list=template_list
	# input()
	myprint(http_template_list)
	myinput()
	http_template_list=[ [http_template,order] for http_template,order in http_template_list if "(?" not in http_template and isinstance(http_template, str)]
	myprint(http_template)
	myprint(http_template_list)
	myinput("http template list")
	for idx,(http_template,order) in enumerate(http_template_list):
		myprint(http_template,end=' ')
		myprint(type(http_template))

		results=re.findall(r"\(.+\)\?",http_template,flags=re.I|re.M)
		myprint('results',results)
		for res in results:
			myprint(res)
			if res.endswith('?'):
				myprint('+? - no sign')
				new_template=re.sub("\(((?:[^()]+\|)*[^()]+)\)\?","",http_template,1)
				order=caluclate_order(new_template)
				http_template_list.append([new_template,order])			
		results=re.findall("\[.+\]\?",http_template,flags=re.I|re.M)
		myprint('results',results)
		for res in results:
			myprint(res)
			if res.endswith('?'):
				print('+? - no sign')
				new_template=re.sub("\[.+\]\?","",http_template,1)
				order=caluclate_order(new_template)
				http_template_list.append([new_template,order])					
		
	myprint(http_template_list)
	# myinput()
	for idx,(http_template,order) in enumerate(http_template_list):
		wildcharlist=[]
		if len(order)==0:
			http_template_list[idx]=[http_template,order,[]]


		for item in order:
			if item=='(':
				res=re.search(r"\(((?:[^()]+\|)*[^()]+)\)\??",http_template,flags=re.I|re.M)
				if res:
					myprint(f"startposition {http_template}  ", res.start(),'results ',res)

					wildcharlist.append((res[1],res[1].split("|")))
					
					http_template_list[idx][0]=re.sub("\(((?:[^()]+\|)*[^()]+)\)\??","!",http_template_list[idx][0],1)
					http_template=re.sub("\(((?:[^()]+\|)*[^()]+)\)\??","!",http_template,1)
					if len(http_template_list[idx])==3:
						http_template_list[idx][2]=wildcharlist
					else:
						http_template_list[idx].append(wildcharlist)
					myprint(wildcharlist)
					myprint(http_template)
					myprint(http_template_list)

					# myinput()
			if item=='[':
				res=re.search(r"\[(.\-.)\]\??",http_template,flags=re.I|re.M)	
				if res:
					myprint(f"startposition {http_template}  ", res.start(),'results ',res)

					myprint(res[0])
					strt,end=res[0].split("-")				
					myprint("start ",strt[1],' end ',end[0])
					charlist=''
					for ch in range(ord(strt[1]),ord(end[0])+1):
						if chr(ch) not in ['?','[',']','(',')','!','*','{','}','$']:
							charlist+=chr(ch)
					myprint(charlist)
					wildcharlist.append((res[0],charlist))
					myprint(wildcharlist)
					http_template_list[idx][0]=re.sub("(\[.\-.\])\??","!",http_template_list[idx][0],1)
					http_template=re.sub("(\[.\-.\])\??","!",http_template,1)
					myprint(http_template)
					if len(http_template_list[idx])==3:
						http_template_list[idx][2]=wildcharlist
					else:
						http_template_list[idx].append(wildcharlist)
					myprint(http_template_list)
					if DEBUGFLAG:
						myinput()


	# myinput()
	procs=[]
	for num in range(0,PROC_NUM):
		prc=Process(target=superProc,args=(queue,))
		prc.start()
		procs.append(prc)
	for (http_template,order,wildcharlist) in http_template_list:
		masks_list=[]
		supercharlist=[]
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
		for wldchr,chrlst in wildcharlist:
			supercharlist.append(chrlst)
		myprint("supercharlist ",supercharlist)		
		

		for mask,length in masks_list:
			all_combinations=product(chrStr,repeat=length)
			for combination in all_combinations:
				generated_string = ''.join(combination)
				resstr=mask
				for nch in generated_string:
					if resstr[resstr.index('?')-1]!='\\':
						resstr=resstr.replace('?',nch,1)
				if wildcharlist:
					newresstr=resstr
					
					tmpres=[]


					results=iter(product(*supercharlist))
					for item in results:
						myprint(item)
						for ch in item:

							newresstr=newresstr.replace('!',ch,1)
							if not "!" in newresstr:
								myprint(newresstr)
								while queue.qsize()>1000000:
									pass
								if '$' in newresstr and wordProduct:
									for words in wordProduct:
										newresstr2=newresstr
										for word in words:										
											newresstr2=newresstr2.replace('$',word,1)
										newresstr2=re.sub(r"\\(\?|\$|\*|\!)",r'\1',newresstr2)
										queue.put(newresstr2)
								else:
									newresstr=re.sub(r"\\(\?|\$|\*|\!)",r'\1',newresstr)
									queue.put(newresstr)
								break
						newresstr=resstr

				else:
					if not resstr in all_http_results:
						myprint(resstr,' ',len(resstr))
						all_http_results.append(resstr)
						while queue.qsize()>1000000:
							pass

						if '$' in resstr and wordProduct:
							for words in wordProduct:
								newresstr=resstr
								for word in words:										
									newresstr=newresstr.replace('$',word,1)
								newresstr=re.sub(r"\\(\?|\$|\*|\!)",r'\1',newresstr)
								queue.put(newresstr)
						else:
							resstr=re.sub(r"\\(\?|\$|\*|\!)",r'\1',resstr)
							queue.put(resstr)
	for _ in range(PROC_NUM):
		queue.put('TERMINATE')
	myprint(all_http_results)

if __name__ == '__main__':
	multiprocessing.freeze_support()
	main()