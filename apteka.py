from bs4 import BeautifulSoup
from multiprocessing import Pool,Process,Queue,Lock
import requests
import lxml
import time
import re
import undetected_chromedriver.v2 as uc
from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import Action chains
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType


import colorama
from colorama import init, Fore, Back, Style
# essential for Windows environment
init()
# all available foreground colors
FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
# all available background colors
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
# brightness values
BRIGHTNESS = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]


def print_with_color(s, color=Fore.WHITE, brightness=Style.NORMAL, **kwargs):
    """Utility function wrapping the regular `print()` function 
    but with colors and brightness"""
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)

ua=UserAgent()
def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

def get_prices(queue,lock):
    lock.acquire()
    print('get_prices')

    options = uc.ChromeOptions()
    prox=Proxy()
    PROXY = "socks5://localhost:9050" # IP:PORT or HOST:PORT
    userAgent = ua.random
    options.add_argument("--headless")
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--no-sandbox") 
    options.add_argument(f'--user-agent={userAgent}')
    drivers=uc.Chrome(browser_executable_path=r"c:\Program Files\Google\Chrome\Application\chrome.exe",options=options) 
    lock.release()

    while True:

        while not queue.empty():
        
            link=queue.get()
            # link=re.sub(r'pharmacy/(\w+)/filter',f"pharmacy/{city}/filter",link)
            drivers.get(url=link)
            # time.sleep(3)
            try:
                cards=drivers.find_elements_by_class_name('address-card')
                for cnt,card in enumerate(cards):
                    if cnt<5:
                        apteka=card.find_element_by_class_name('address-card__header--section').text
                        price=card.find_element_by_class_name('filter-group__list--item-row').text
                        apteka=re.sub(r'Як потрапити',"",apteka)
                        if cnt in [0,1]:
                            print_with_color(apteka,color=Back.WHITE+Fore.BLACK, brightness=Style.NORMAL)
                            print_with_color(price,color=Back.WHITE+Fore.BLUE, brightness=Style.NORMAL)                            
                        else:
                            print(apteka)
                            print(price)
                        print('+'*50)     
            except:
                print('[-]Вибачте нічого не знайдено')

if __name__=='__main__':
    pills=input('Що шукаємо:')
    # city=input('В якому місті:')
    pills=pills.strip()
    queue=Queue()
    lock = Lock()

    procs=[]
    procs.append(Process(target=get_prices,args=(queue,lock)))
    for proc in procs:
        proc.start()
    
    # signal TOR for a new connection 
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="torProxy@123")
        controller.signal(Signal.NEWNYM)
        lock.acquire()
        options = uc.ChromeOptions()
        prox=Proxy()
        PROXY = "socks5://localhost:9050" # IP:PORT or HOST:PORT
        userAgent = ua.random
        print(userAgent)
        options.add_argument("--headless")
        #options.add_argument("--disable-dev-shm-usage")
        options.add_argument('--log-level=3')
        # options.add_argument("--no-sandbox")        
        # options.add_argument('--proxy-server=%s' % PROXY)
        options.add_argument(f'--user-agent={userAgent}')
        driver=uc.Chrome(browser_executable_path=r"c:\Program Files\Google\Chrome\Application\chrome.exe",options=options)
        lock.release()
        #driver=webdriver.Chrome(executable_path=r'd:\Users\tonnyr2\bin\chromedriver.exe',options=chrome_options)
        driver.get(f'https://tabletki.ua/uk/search/{pills}/')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        lnks=soup.find_all('div',class_='row category-card__card-row no-border flex-column catalog-search__section')[0].find('ul',class_='mb-3')
        print(lnks)
        lnks=lnks.find_all('a')
        catlist=[]
        disclink='https://tabletki.ua/uk/category/{}/filter/sort=2/'
        for item in lnks:
            print(item)
            category=str(item.get('href'))
            ans=input(f'Шукати товар {item.text} Y/N? ')
            if ans.lower()=='y':
                print(category[0])
                res=re.search(r'(\d+)/$',category)
                if res:
                    cat=res.group(1)
                    print(cat)
                    catlist.append(cat)
                else:
                    
                    catlist.append(category)
        for lnk in catlist:
            if bool([ele for ele in ['0','1','2','3','4','5','6','7','8','9'] if (ele in lnk) ]) and len(lnk)<6:
                print(disclink.format(lnk))
                driver.get(disclink.format(lnk))
            else:
                print(f'https://tabletki.ua{lnk}')
                driver.get(f'https://tabletki.ua{lnk}')                
            links=driver.find_elements_by_class_name('card__category--bottom')
            linklist=[]
            for cnt,link in enumerate(links):
                if cnt<3:
                    try:
                        tovarLnk=link.find_element_by_tag_name('a').get_attribute('href').strip()
                        print(tovarLnk)
                        # tovarLnk=re.sub(r'pharmacy/(\w+)/',f"pharmacy/{city}/",tovarLnk)
                        linklist.append(tovarLnk)
                    except:
                        pass
                else:
                    break
                for tovar in linklist:
                    driver.get(tovar)
                    try:
                        btn=driver.find_element(By.XPATH,'//*[@id="findProduct"]').get_attribute('href')+'filter/s=price/'
                        # btn=re.sub(r'pharmacy/(\w+)/filter',f"pharmacy/{city}/filter",btn)
                        print(btn)
                        queue.put(btn)
                    except:
                        print('[-]Нема елементу з id=findProduct')
                        
                # time.sleep(5)
            # time.sleep(5)
        for proc in procs:
            proc.join()             
        time.sleep(60)