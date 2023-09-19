import argparse
import readchar
import os
import mimetypes
import requests
from requests.exceptions import ConnectionError
from requests.auth import HTTPBasicAuth
import psutil
from itertools import product,combinations
from multiprocessing import Pool,Process,Queue,Lock,Manager
import multiprocessing
import time
from datetime import datetime
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
(mega,test,porno,tube) - any word from list choose from alternatives like in regular expressions
						alternatives also supports quantifiers like characters ranges
$ - will be replaced by each word from the dictionary link or path to the dictionary -d option	
You can add list of dictionaries separated by comma 				
HOTKEYS:
's' - 	suspend scaning
'r' - 	resume scaning
'q' - 	quit program
'n' -   go to the next directory if -s

EXAMPLES:
python {sys.argv[0]} -t 'https://base[0-9]{chr(0x7b)}0,3{chr(0x7d)}.(com,org,net)' -l 44
python {sys.argv[0]} -t 'https://[a-z]ou?ube[0-9]{chr(0x7b)}0,3{chr(0x7d)}.com' -l 44
python {sys.argv[0]} -t 'https://anywebsite.com/$' -d https://github.com/trickest/wordlists/raw/main/technologies/bagisto-all-levels.txt 
"""

def downloadFile(url:str,dnldfile:str):
    with open(dnldfile, 'wb') as handle:
        response = requests.get(url, stream=True)
        hdrs=response.headers
        print(f"Content-Type {hdrs['Content-Type']}")
        if not response.ok:
            print("ok")
        for block in response.iter_content(1024):
         if not block:
             break
         handle.write(block)


def count_lines(file_path, chunk_size=8192):
    line_count = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            line_count += Counter(chunk)['\n']
    return line_count

def word_generator(filenamelist):
    word = '' 
    for filename in filenamelist:
        if filename.startswith('http://') or filename.startswith('https://'):
            path=urlparse(filename).path
            filename=os.path.basename(path)

        try:
            with open(filename, 'r') as file:
                while True:
                    char = file.read(1) 

                    if not char:
                       
                        if word:
                            yield word
                        break

                    if char not in ('\r', '\n'):
                        word += char 
                    else:
                        if word:
                            yield word 
                            word = '' 
        except FileNotFoundError:
            print(f"The file '{filename}' was not found.")


template_list=list()
def clr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def get_arguments():
    parser=argparse.ArgumentParser(HELP_MSG)
    parser.add_argument('-t', required=True, default=None,dest='http_template',help='<URLTEMPLATE>')
    parser.add_argument('-l', required=False, default=None,dest='http_length',help='<MAXURLLENGTH>')
    parser.add_argument('-a', required=False, default=None,dest='useragent',help='<USERAGENT>')
    parser.add_argument('-d', required=False, default=None,dest='dictionary',help='Dictionary(PATH|URL)')
    parser.add_argument('-H', required=False, default=None,dest='header_string',help='Add a custom header to the HTTP request.')
    parser.add_argument('-loc', action="store_true",dest='location',help='Print "Location" header when found')
    parser.add_argument('-N', required=False, default=None,dest='nf_code',help='Ignore responses with this HTTP code.')
    parser.add_argument('-o', required=False, default=None,dest='output_file',help='Save output to disk')
    parser.add_argument('-p', required=False, default=None,dest='proxyaddr_port',help='Use this proxy. (Default port is 1080)')
    parser.add_argument('-P', required=False, default=None,dest='proxy_data',help='Proxy Authentication <username:password>.')
    parser.add_argument('-v',  action="store_true",dest='NOT_FOUND_PAGES',help='Show also NOT_FOUND pages.')
    parser.add_argument('-s',  action="store_true",dest='scan_dirs',help='scan directories on the specific website.')
    parser.add_argument('-r',  action="store_true",dest='recurs',help='search in all found directoies.')
    parser.add_argument('-f',  action="store_true",dest='NOT_FOUND',help='Fine tunning of NOT_FOUND (404) detection.')
    parser.add_argument('-z', required=False, default=None,dest='delay',help='Add a millisecond delay to not cause excessive Flood.')
    parser.add_argument('-c', required=False, default=None,dest='cookie',help='cookiestring')
    parser.add_argument('-n', required=False, default=None,dest='procnum',help='number of processes')
    parser.add_argument('-M', required=False, default=None,dest='extfound',help='Try variations on a found filename.')
    parser.add_argument('-X', required=False, default=None,dest='extvar',help='Add file extensions to wordlist contents.')
    parser.add_argument('--not', required=False, default=None,dest='notintitle',help='Show URLS if not substring in title.')
    parser.add_argument('-u', required=False, default=None,dest='basicauth',help='Basic authorization user:password.')
    parser.add_argument('-E', required=False, default=None,dest='certpath',help='Path to certificate.')


    options = parser.parse_args()
    if not options.http_template:
        parser.error("[-] Please specify an URL TEMPLATE, use --help for more info")
    return options

def myprint(*msg, **kwargs):
	global DEBUGFLAG
	if DEBUGFLAG:
		print("DEBUG:   ",end=" ")
		print(*msg, **kwargs)

def myinput(*msg, **kwargs):
	global DEBUGFLAG
	if DEBUGFLAG:
		pass
		#input(*msg, **kwargs)

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


def replacedolar(dictlist,queue,url,extvars=[]):
	myprint('replacedolar')
	for item in word_generator(dictlist):
		# myprint(item)
		if Counter(url)['$']==1 and extvars:
			queue.put(url.replace('$',item,1))
			for ext in extvars:
				queue.put(url.replace('$',item+ext,1))
			continue
		elif Counter(url)['$']==1:
			queue.put(url.replace('$',item,1))
			# print(url,1)
			continue
		else:
			newurl=url.replace('$',item,1)
		if '$' in newurl:
		    for it in word_generator(dictlist):
		        if Counter(newurl)['$']==1 and extvars:
		            for ext in extvars:
		                queue.put(newurl.replace('$',it+ext,1))
		            queue.put(newurl.replace('$',it,1))
					# queue.put(newurl.replace('$',it,1))
		    newurl=replacedolar(dictlist,queue,newurl,extvars)
		else:
		    if Counter(newurl)['$']==1 and extvars:
		        for ext in extvars:
		            queue.put(newurl+ext)
		        queue.put(newurl)
		    else:
		        queue.put(newurl)
		    return newurl


def superProc(options,queue,number,totalNumber,dirlist,lock):
	HEADERS= {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36'}
	PROXIES={}
	reqparam={'headers':HEADERS}
	user=password=None
	myprint("superproc started")
	nf_codes=[]
	mimetypes.add_type('text/html','.php',strict=True)
	mimetypes.add_type('text/html','.aspx',strict=True)
	mimetypes.add_type('text/plain','.ini',strict=True)
	mimetypes.add_type('text/plain','.log',strict=True)
	if options.certpath:
		reqparam['verify']=options.certpath
	if options.basicauth:
		username,password=options.basicauth.split(':')
		reqparam['auth']=HTTPBasicAuth(user, password)
	if options.cookie:
		HEADERS['Cookie']=options.cookie
	if options.proxyaddr_port:
		proxyaddr,proxyport=options.proxyaddr_port.split(':')
		PROXIES['http']=f'http://{proxyaddr}:{proxyport}'
		PROXIES['https']=f'https://{proxyaddr}:{proxyport}'
		if options.proxy_data:
			user,password=options.proxy_data.split(':')
			for ky,vl in PROXIES.items():
				PROXIES[ky]=PROXIES[ky].replace(f'{ky}://',f'{ky}://{user}:{password}@')
		print(PROXIES)
		reqparam['proxies']=PROXIES
	if options.useragent:
		HEADERS['User-Agent']=options.useragent
	if options.header_string:
		ky,vl=options.header_string.split(':')
		HEADERS[ky]=vl
		# print(HEADERS)
	if options.nf_code:
		nf_codes=list(map(int,options.nf_code.split(',')))
		myprint(nf_codes)

	while True:


		while not queue.empty():
			title=''
			link=queue.get()	
			myprint(link)
			precentage=1		
			if link.startswith('TERMINATE'):
				print('superproc TERMINATED')
				return
			try:
				# if totalNumber.value>0:
				# 	precentage=number.value/(totalNumber.value/100)
				if options.delay:
					time.sleep(int(options.delay)/1000)
				reqparam['url']=link
				res=requests.get(**reqparam)
				code=res.status_code
				try:
					contenttType=res.headers['Content-Type']
				except KeyError:
					contenttType='text/plain'					
				contenttType=contenttType.split(';')[0]
				length=len(res.text)
				mimtype=mimetypes.guess_type(link,strict=True)

				if code==200 and options.extfound:
					extfound=options.extfound.split(",")
					for ext in extfound:
						print(link+ext)
						try:
							reqparam['url']=link+ext
							rs=requests.get(**reqparam)
							mimtype=mimetypes.guess_type(link+ext,strict=True)
							if rs.status_code not in nf_codes:
								if rs.status_code in [403,200,301]:
									if mimtype[0]==contenttType:
										print(f"+{link+ext} ((CODE={rs.status_code}|LEN={len(rs.text)}))")
									else:
										print(f"-{link+ext} ((CODE={rs.status_code}|LEN={len(rs.text)}))")
								else:
									print(f"-{link+ext} ((CODE={rs.status_code}|LEN={len(rs.text)}))")
								if options.output_file:
									with open(options.output_file,'a',encoding='utf-8') as fl:
										fl.write(f"+{link+ext} ((CODE={rs.status_code}|LEN={len(rs.text)}))\n")
						except ConnectionError:
							pass

				if options.NOT_FOUND and code==404:
					print(linkres)
					if options.output_file:
						with open(options.output_file,'a',encoding='utf-8') as fl:
							fl.writelines(linkres+"\n")					
				if code not in nf_codes:
					try:
						res1=re.search(r'<title>([^>]+)<\/title>',res.text)
						title=res1[1]
						if options.notintitle and options.notintitle in title:
							continue

						title=re.sub('\s+',' ',title)
						if res1:
							print(f"{link=} Title:{res1[1]}")


					except TypeError:
						pass
				if 200<=code<=301:
					if contenttType=='text/html' and options.recurs:
						# Scan dirs should be here
						listdirs=dirScan(link,reqparam)
						myprint('listdir ',listdirs)
						for dirr in listdirs:
							myprint(dirr)

							try:
								with lock:								
									if  dirr not in dirlist:
										myprint(f'newdir detected {dirr}')
										myprint(dirlist)
										dirlist.append(dirr)
										myprint(dirlist)
									else:
										listdirs.remove(dirr)
							except multiprocessing.managers.RemoteError:
						 		print("RemoteError")
						with lock:
							if "/" in dirlist:
								dirlist.remove('/')
							dirlist.insert(0,'/')
						websiteurl=re.sub(r'^(\w{3,5}:\/\/(?:[\w\d\._-]+)+)\/.+',r'\1',link)
						myprint(f"{websiteurl=}")
						for dirr in listdirs:
							url=websiteurl+dirr
							myprint(f"{url=}")
							res=requests.get(url,headers=HEADERS)
							if 200<=res.status_code<400:
								print(f'+++++DIRECTORY {url}')
								if "Index of" in res.text:
									print(f"{url} is opendirectory")
								for fl in ['index.html','index.php','default.aspx']:
									try:
										fl=url+fl
										reqparam['url']=fl
										res=requests.get(**reqparam)
										if res.status_code==200:
											code2=res.status_code
											length2=len(res.text)
											print(f"Default file {fl} exists (CODE2={code2}|LEN2={length2})")
									except ConnectionError:
										pass
							else:
								if dirr in dirlist:
									myprint(f"remove {dirr} {res.status_code}")
									dirlist.remove(dirr)


							# print(dirlist)

					if mimtype[0]==contenttType or re.search(r"\/\.\w+$",link) or re.search(r'^(\w{3,5}:\/\/(?:[\w\d\._-]+)+)$',link):
						linkres=f"+{link} (CODE={code}|LEN={length})\n"# {number.value} %{precentage}"
					else:
						linkres=f"-{link} (CODE={code}|LEN={length}|Type={contenttType}) {mimtype}"#\n{number.value} Links %{precentage}"
				else:
					linkres=f"-{link} (CODE={code}|LEN={length})"#\n{number.value} Links %{precentage}"
				if options.location:
				 	headers=res.headers
				 	try:
				 		linkres+=f"Location {headers['Location']}"
				 	except:
				 		pass

				if nf_codes:
					if code not in nf_codes:
						print(linkres)
						if options.output_file:
							with open(options.output_file,'a',encoding='utf-8') as fl:
								fl.writelines(linkres+"\n")
				else:
					print(linkres)
					if options.output_file:
						with open(options.output_file,'a',encoding='utf-8') as fl:
							fl.writelines(linkres+"\n")					


			except ConnectionError:
				if options.NOT_FOUND_PAGES:
					print(f"NOT_FOUND_PAGE: {link}")
				myprint("[-]Connection problems")
			finally:
				precentage=1
				# if totalNumber.value>0:
				# 	precentage=number.value/(totalNumber.value/100)
				# print(f"\rPROGRESS: {number.value} of {totalNumber.value if totalNumber.value!=0 else 'Unknown'} %{precentage:00.2f}",end='\r')
				# y.value+=1

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

def dirScan(link,reqparam):
	dirlist=list()
	try:
		reqparam['url']=link
		res=requests.get(**reqparam)
		websiteurl=re.sub(r'^(\w{3,5}:\/\/)',r'',link)
		results=re.findall(re.escape(websiteurl)+"((?:\/[\w\d\._-]+)+\/).*",res.text)
		myprint(results)
		for dir in results:
			dirlist.append(dir)		
		results=re.findall(r'href=([\'\"])(\/?(?:[\w\d_-]+\/)+)[^\'\"]+\1',res.text)
		myprint(results)
		for dir in results:
			if dir[1][0]!='/':
				myprint('/'+dir[1])
				dirlist.append('/'+dir[1])
			else:
				dirlist.append(dir[1])
		dirlist=list(set(dirlist))
		return dirlist
	except ConnectionError:
		return dirlist

def reformat_httptemplate(http_template):
	http_template_list=[]
	global template_list
	wildcharlist=[]
	strt,end=[],[]
	res=re.search(r'(\(\?(?:[^()]+,)+[^()]+\))',http_template,flags=re.I|re.M)
	if res:
		items=res[1][2:-1].split(',')
		for item in items:
			myprint(item)
			new_template=re.sub(r'(\(\?(?:[^()]+,)+[^()]+\))',item,http_template,1)
			myprint(new_template)
			http_template_list.append([new_template,caluclate_order(new_template)])
			http_template_list= reformat_httptemplate(new_template)			
		#http_template = re.sub('(\(\?(?:[^()]+,)+[^()]+\))',"",http_template,1)
		myprint(http_template)
		myprint(http_template_list)
		# input()
	res=re.search(r"(\[.\-.\]|\((?:[^()]+,)*[^()]+\))(\{(?:\d\,)?\d\})",http_template,flags=re.I|re.M)	
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
			for it in res[1][1:-1].split(','):
				wildcharlist.append((res[1],it))
		myprint(wildcharlist)
		if res[2]:
			for it in range(strtnum,endnum+1):
				http_template_list.append(http_template)
				myprint("res*it:",res[1]*it," it=",it," startnum ",strtnum,' endnum ',endnum)
				http_template_list[-1]=re.sub("(\[.\-.\]|\((?:[^()]+,)*[^()]+\))(\{(?:\d\,)?\d\})",res[1]*it,http_template_list[-1],1)
		else:
			http_template=re.sub("(\[.\-.\]|\((?:[^()]+,)*[^()]+\))(\{(?\d\,)?\d\})","!",http_template,1)
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

def scanDirs(websiteurl,HEADERS):
	dirlist=list()
	myprint(f"scanDirs {websiteurl}")
	try:

		res=requests.get(websiteurl,headers=HEADERS)
		websiteurl=re.sub(r'^(\w{3,5}:\/\/)',r'',websiteurl)
		results=re.findall(re.escape(websiteurl)+"((?:\/[\w\d\._-]+)+\/).*",res.text)
		myprint(results)
		for dir in results:
			dirlist.append(dir)

		results=re.findall(r'href=([\'\"])(\/?(?:[\w\d_-]+\/)+)[^\'\"]+\1',res.text)
		myprint(results)
		for dir in results:
			if dir[1][0]!='/':
				myprint('/'+dir[1])
				dirlist.append('/'+dir[1])
			else:
				dirlist.append(dir[1])
		myprint(websiteurl+"/robots.txt+sitemap.xml")
		for file in ["robots.txt","sitemap.xml"]:
			try:
				res=requests.get('https://'+websiteurl+file,headers=HEADERS)
				results=re.findall(r"(?:\s|^)(\/.+\/)(?:\s*|$)",res.text)
				myprint(results)
				for dir in results:
					myprint(dir)
					dirlist.append(dir)

			except:
				pass			
		dirlist=list(set(dirlist))
		# print(dirlist)
		return dirlist
	except:
		print('no results')
		return dirlist
	

def main(dirCounter):
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
	extvars=list()
	manager=Manager()
	number=manager.Value('i',0)	
	dirlist=manager.list()
	totalnumber=manager.Value('i',0)	
	lock=manager.Lock()
	if options.extvar:
		extvars=options.extvar.split(',')

	if options.procnum:
		PROC_NUM=int(options.procnum)
	http_template=options.http_template
	procs=[]
	dt=datetime.now()
	print(dt.strftime('START_TIME: %a %b %d %H:%M:%S %Y'))
	for num in range(0,PROC_NUM):
		prc=Process(target=superProc,args=(options,queue,number,totalnumber,dirlist,lock,))
		prc.start()
		procs.append(prc)	
	if not options.http_length:
		http_length=44

	else:
		http_length=options.http_length
	if options.dictionary:
		dictionaryList=list()
		word_dictionary=options.dictionary
		dictionaryList=options.dictionary.split(',')
		print(f"WORDLIST_FILES: {dictionaryList} ")

		wordcounter=0
		for dictpath in dictionaryList:
			if dictpath.startswith('http://') or dictpath.startswith('https://'):
				path=urlparse(dictpath).path
				path=os.path.basename(path)
				if path!='' or path!='/':
					downloadFile(dictpath,path)
					dictpath=path

			if os.path.exists(dictpath):
				wordcounter+=count_lines(dictpath,50_000)
		word_list=word_generator(dictionaryList)
		totalnumber.value=wordcounter*(len(extvars)+1)

		dolarCounter=Counter(http_template)
		dolarCounter=dolarCounter['$']
		myprint(dolarCounter)


	if options.scan_dirs:

		
		prevdir=0
		websiteurl=re.sub('^(\w{3,5}:\/\/(?:[\w\d_-]+\.)+[\w\d_-]+)\/.*',r'\1',http_template)			
		print(f"URLBASE: {websiteurl}")
		mydirlist=scanDirs(websiteurl,HEADERS)
		with lock:
			for it in mydirlist:
				if not it in dirlist:
					dirlist.append(it)
			for dirr in mydirlist:
				myprint(dirr)
				while dirr!='/':
					dirr=re.sub(r'\/[^/]+\/$','/',dirr)
					if not dirr in dirlist:
						dirlist.append(dirr)

		with lock:
			#dirlist=manager.list(list(set(dirlist)))
			if "/" in dirlist:
				dirlist.remove('/')
			dirlist.insert(0,'/')
			print("dirlist ",dirlist)
		# with lock:
			for dirr in dirlist:
				url=websiteurl+dirr
				res=requests.get(url,headers=HEADERS)
				if 200<=res.status_code<400:
					print(f'+++++DIRECTORY {url}')
					if "Index of" in res.text:
						print(f"{url} is opendirectory")
					for fl in ['index.html','index.php','default.aspx']:
						try:
							fl=url+fl
							res=requests.get(fl,headers=HEADERS)
							if res.status_code==200:
								code=res.status_code
								length=len(res.text)
								print(f"Default file {fl} exists (CODE={code}|LEN={length})")
								queue.put(fl)

						except ConnectionError:
							pass

				else:
					dirlist.remove(dirr)
		# with lock:
			print(dirlist)

		if options.recurs:
			print("recurs")
			# with lock:
			totalnumber.value=len(word_list)*len(dirlist)
			while dirCounter.value!=len(dirlist):
				for words in word_list:
					if len(dirlist)==0:
						dirIndex=0
						print('len 0')
						break
					else:
						dirIndex=dirCounter.value % len(dirlist)
						time.sleep(0.005)
						curidx=dirlist[dirIndex]
						if prevdir!=curidx:
							print(f"[!]Scan directory {curidx}")
							prevdir=curidx
					url=websiteurl+dirlist[dirIndex]+words
					if extvars:
						queue.put(url)
						for ext in extvars:
							queue.put(url+ext)
					else:
						queue.put(url)					
				dirCounter.value+=1
			for _ in range(PROC_NUM):
				queue.put('TERMINATE')
			for prc in procs:
				prc.join()
			dt=datetime.now()
			print(dt.strftime('END_TIME: %a %b %d %H:%M:%S %Y'))			
			return

		for words in wordProduct:
			# print(dirlist)
			if len(dirlist)==0:
				dirIndex=0
				print('len 0')
			else:
				dirIndex=dirCounter.value % len(dirlist)
				time.sleep(0.005)
				curidx=dirlist[dirIndex]
				if prevdir!=curidx:
					print(f"[!]Scan directory {curidx}")
					prevdir=curidx
			url=websiteurl+dirlist[dirIndex]+words[0]
			# print(url)
			if extvars:
				queue.put(url)
				for ext in extvars:
					queue.put(url+ext)
			else:
				queue.put(url)

		for _ in range(PROC_NUM):
			queue.put('TERMINATE')
		for prc in procs:
			prc.join()
		dt=datetime.now()
		print(dt.strftime('END_TIME: %a %b %d %H:%M:%S %Y'))			
		# input()
		return
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
				new_template=re.sub("\(((?:[^()]+,)*[^()]+)\)\?","",http_template,1)
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
				res=re.search(r"\(((?:[^()]+,)*[^()]+)\)\??",http_template,flags=re.I|re.M)
				if res:
					myprint(f"startposition {http_template}  ", res.start(),'results ',res)

					wildcharlist.append((res[1],res[1].split(',')))
					
					http_template_list[idx][0]=re.sub("\(((?:[^()]+,)*[^()]+)\)\??","!",http_template_list[idx][0],1)
					http_template=re.sub("\(((?:[^()]+,)*[^()]+)\)\??","!",http_template,1)
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
	myprint('tut2')
	totnmbr=1
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
		for wldchr,chrlst in wildcharlist:
			supercharlist.append(chrlst)
			totnmbr*=len(chrlst)

		totalnumber.value*=totnmbr
		myprint(f"{totalnumber.value=}")
		print(f"{masks_list[-1][-1]}*{len(chrStr)}")		
		if masks_list[-1][-1]>0:
			totalnumber.value*=masks_list[-1][-1]*len(chrStr)
		myprint(f"{totalnumber.value=} 2")

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
								if '$' in newresstr:
									replacedolar(dictionaryList,queue,newresstr,extvars)
								else:
									queue.put(newresstr)
								break
						newresstr=resstr

				else:
					if not resstr in all_http_results:
						myprint(resstr,' ',len(resstr))
						all_http_results.append(resstr)
						while queue.qsize()>1000000:
							pass
						if '$' in resstr:
							replacedolar(dictionaryList,queue,resstr,extvars)
						else:
							queue.put(resstr)

	for _ in range(PROC_NUM):
		queue.put('TERMINATE')
	myprint(all_http_results)
	for prc in procs:
		prc.join()

if __name__ == '__main__':
	mypid=os.getpid()
	multiprocessing.freeze_support()
	clr()	
	manager=Manager()
	dirCounter=manager.Value('i',0)
	prc=Process(target=main,args=(dirCounter,))
	prc.start()
	while True:
		p=psutil.Process(mypid)
		ch=readchar.readchar()
		try:
			ans=str(ch,encoding='UTF-8').lower()
		except:
			ans=ch.lower()
		if ans=='s':
			print('[!]Suspendprocesses')
			chldlist=p.children(recursive=True)
			for prc in chldlist:
				prc.suspend()
		elif ans=='r':
			print('[!]Resume processes')
			chldlist=p.children(recursive=True)
			for prc in chldlist:
				prc.resume()			
		elif ans=='q':
			print('[!]Terminated processes')
			chldlist=p.children(recursive=True)
			for prc in chldlist:
				prc.kill()	
			sys.exit(0)		
		elif ans=='n':
			dirCounter.value+=1
			print(f"[!] Go to next directory")


