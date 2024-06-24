import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import requests

#TOKEN = '7230213740:AAGpkqyw1JOcksTRXmq7gaDcEr2hPq7FIe4'
#CHANNEL_ID = '@Pmttg'
TOKEN = '7413438567:AAFSWk-fNlSDxbKU-RqGZTwcb996zEsjTpk' # MODSBOTS_BOT

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}	
def proxyfix(keyword):
    url = "https://raw.githubusercontent.com/ArrayIterator/proxy-lists/main/proxies/http.txt"#"https://www.proxyscan.io/download?type=http"
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
def noproxyfix(keyword):
    
    r = requests.get("https://translate.google.com/", timeout=5)
    print(r.status_code)
    stat = r.status_code
    if stat == 200:          
        translated = GoogleTranslator(source='auto', target='my').translate(text=keyword)
        return translated
    else:
        pass
        

def soup (url,filename):
    
    page = requests.get(url, headers=headers)       
    soup = BeautifulSoup(page.content, 'lxml') 
    #articles = soup.find_all("div", {"class": "entry-content wp-block-post-content has-global-padding is-layout-constrained wp-block-post-content-is-layout-constrained"})
    div_list = [div for div in soup.find_all('div', class_="entry-content wp-block-post-content has-global-padding is-layout-constrained wp-block-post-content-is-layout-constrained")]
    p_list = [div.find_all('p',class_="") for div in div_list]
    content = [item.text.strip() for p in p_list for item in p]
    with open(filename+ '.txt', 'w') as fp:
        pass
    for o in content:
        original = o
        f = open(filename+ '.txt',"a", encoding="utf-8")
        f.write("\n"+o)
        transalted = noproxyfix(str(o).replace('"',''))
        print(transalted)
        try:
            f = open(filename+ '.txt',"a", encoding="utf-8")
            f.write("\n"+transalted)
        except:
            pass
        
@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        #if user will try to write 'Profile' without subscription    
        if "https://" in message.text:
            e = await bot.send_message(message.from_user.id,'🚀I am translating your noval link🚀')
            filename = str(e.message_id)
            url = message.text
            soup(url,filename)
            file = open(filename + ".txt", "rb")
            await bot.send_document(message.from_user.id,file)
        
        else:
            await bot.send_message(message.from_user.id,'🚀something went wrong🚀')
    else:
        pass

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)   



#print(content)
