#!/usr/bin/env python
import requests
import sys
cnt=0
for link in sys.argv:
    if cnt>0:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; U; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.140 Safari/537.36",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }

        res = requests.get(link,headers=headers,stream=True,timeout=20)
        #print(res)
        html = res.text

        if(html.find("license_code:") != -1):
            t1 = html.split("license_code: '")
            t2 = t1[1].split("'")
            d = t2[0]
            d1 = d.replace('0', '1')
            
            f = d1[1:]
            
            c = 16

            t1 = html.split("function/0/")
            t2 = t1[len(t1)-1].split("'")
            orig = t2[0]
            
            j = int(len(f) / 2)
            
            k = int(f[0: j + 1])
            l = int(f[j:])
            g = l - k

            if g < 0:
                g = - g

            f = g
            g = k - l

            if g < 0:
                g = -g

            f += g
            f = int(f * 2)

            f = "" + str(f)
            i = int(c / 2) + 2
            m = ""
            g = 0
            while g < j+1:
                h = 1
                while h <= 4:
                    n = int(d[g + h]) + int(f[g])
                    if n >= i:
                        n -= i
                    m = str(m) + str(n)
                    h = h + 1
                g = g + 1

            t1 = orig.split("/")
            j = t1[5]

            h = j[0:32]
            i = m

            j = h
            k = len(h) - 1
            while k >= 0:
                l = k
                m = k

                i = str(i)
                while m < len(i):
                    l = l + int(i[m])
                    m = m + 1

                while l >= len(h):
                    l = l - len(h)

                n = ""
                o = 0
                while o < len(h):
                    if o == k:
                        n = n + h[l]
                    else:
                        if o == l:
                            n = n + h[k]
                        else:
                            n = n + h[o]

                    o = o + 1

                h = n

                k = k - 1

            link = orig.replace(j, h)


            response = requests.get(link,headers=headers,stream=True,timeout=20)
            
            if response.history:
                final_result = response.url
                print(final_result)
            else:
                print("Request was not redirected")
        else:
            print('none. Link Not found.') 
    cnt+=1
