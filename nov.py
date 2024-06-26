from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import requests
import numpy as np
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}	
header2 = {
    # Already added when you pass json=
    # 'Content-Type': 'application/json',
    'Authorization': 'Bearer 95ee7681558840b894f95632dbf72cf1a0a866090844451c86438a520f2155e1',
}
def proxyfix(keyword):
    url = "https://raw.githubusercontent.com/parserpp/ip_ports/main/proxyinfo.txt"#"https://www.proxyscan.io/download?type=http"
    proxis = requests.get(url).text
    proxis = proxis.splitlines()
    for proxy in proxis:
        print(f'checking {proxy}...')
        try:
            r = requests.get("https://translate.google.com/",proxies= {'http': proxy,'https': proxy}, timeout=5)
            print(r.status_code)
            stat = r.status_code
            if stat == 200:
                proxy = {'http': proxy,'https': proxy}
                translated = GoogleTranslator(source='auto', target='my', proxies=proxy).translate(text=keyword)
                return translated
                break
            else:
                pass
        except:
            pass


def tranxl8(o):
    json_data = {
        'source_language': 'en',
        'target_language': 'my',
        'sentences': o,
    }

    response = requests.post('https://api.xl8.ai/v1/trans/request/rt', headers=header2, json=json_data).json()
    #print(response)
    response['sentences']
    for x in  response['sentences']:
        return x

def nov():
    url = f"https://nomad-translations.com/carrying-a-lantern-in-daylight-calid/calid-chapter-5/"
    page = requests.get(url, headers=headers)       
    soup = BeautifulSoup(page.content, 'lxml') 
    #articles = soup.find_all("div", {"class": "entry-content wp-block-post-content has-global-padding is-layout-constrained wp-block-post-content-is-layout-constrained"})
    div_list = [div for div in soup.find_all('div', class_="entry-content wp-block-post-content has-global-padding is-layout-constrained wp-block-post-content-is-layout-constrained")]
    p_list = [div.find_all('p',class_="") for div in div_list]
    content = [item.text.strip() for p in p_list for item in p]

    for o in content:
        original = o
        f = open("example.txt","a", encoding="utf-8")
        f.write("\n"+o)

        #transalted = proxyfix(str(o).replace('"',''))
        #print(transalted)
        tran = []
        a = str(o).replace('"','')
        tran.append(a)
        translated = tranxl8(tran)
        f = open("example.txt","a", encoding="utf-8")
        f.write("\n"+translated)

def proxyfixer(a):
    b = a
    url = "https://raw.githubusercontent.com/parserpp/ip_ports/main/proxyinfo.txt"
    
    proxis = requests.get(url).text
    proxis = proxis.splitlines()
    for proxy in proxis:
        print(f'checking {proxy}...')
        try:
            r = requests.get("https://translate.google.com/",proxies= {'http': proxy,'https': proxy}, timeout=5)
            stat = r.status_code
            if stat == 200:
                #return {'http': proxy,'https': proxy}
                f = open('proxy.json')
                getData = json.load(f)
                with open("proxy.json", "r") as jsonFile:
                    data = json.load(jsonFile)
                    data["proxy"] = str(proxy)
                with open("proxy.json", "w") as jsonFile:
                    json.dump(data, jsonFile)
                jsonFile.close()
                return {'http': proxy,'https': proxy}
                break
            else:
                pass
        except:
           pass

def proxycheck(proxy):
    try:
        r = requests.get("https://translate.google.com/",proxies= {'http': proxy,'https': proxy}, timeout=5)
        stat = r.status_code
        print(stat)
        if stat == 200:
            return {'http': proxy,'https': proxy}
            
    except:
        print('find new one')
        new = proxyfixer('g')
        #print(e)
        return new


def req():
    pages = np.arange(1,3)# [1,2,3,4,5]
    for chapter in pages:
            url = f"https://nomad-translations.com/carrying-a-lantern-in-daylight-calid/calid-chapter-{chapter}/"
            page = requests.get(url, headers=headers)       
            soup = BeautifulSoup(page.content, 'lxml') 
            #articles = soup.find_all("div", {"class": "entry-content wp-block-post-content has-global-padding is-layout-constrained wp-block-post-content-is-layout-constrained"})
            div_list = [div for div in soup.find_all('div', class_="entry-content wp-block-post-content has-global-padding is-layout-constrained wp-block-post-content-is-layout-constrained")]
            p_list = [div.find_all('p',class_="") for div in div_list]
            content = [item.text.strip() for p in p_list for item in p]

            f = open('proxy.json')
            reqData = json.load(f)
            prox = reqData['proxy']    
            proxy = proxycheck(prox)


            with open(chapter+ '.txt', 'w') as fp:
                pass
            for o in content:
                original = o
                f = open(chapter+ '.txt',"a", encoding="utf-8")
                f.write("\n"+o)
                #proxy = {'http': proxy,'https': proxy}
                translated = GoogleTranslator(source='auto', target='my', proxies=proxy).translate(text=str(o).replace('"',''))
                
                
                print(translated)
                try:
                    f = open(chapter+ '.txt',"a", encoding="utf-8")
                    f.write("\n"+translated)
                except:
                    pass


req()
