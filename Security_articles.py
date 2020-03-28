# -*- coding: UTF-8 -*-
#megaload 2019.05.08
import requests
import re
from bs4 import BeautifulSoup
import datetime as d
import json
import execjs
'''
logfile=open("./kanxuelog.txt",'a+')
logfile.seek(0)  
log=str(logfile.read())
'''
date=str(d.datetime.now().strftime("%Y.%m.%d-%H:%M:%S"))
cookies={'a.ccess_token':'21_R00VlXpzNQMw3H8WEnZsq-ZtyYiRllLsFBq4XRxfnPDUCl0Ej-fvjmK7yHjpYJbNr4k9hapKcWEnlxTwg7-P9xqwih8078AV3vSLBHJ1JJvsNVsHozHTneTv98mnJG_Hd1yuO9BvMZPmuFYISSRjADANNM',
'ulevel':'0',
'headimgurl':'http%3A//thirdwx.qlogo.cn/mmopen/N8ib2O8BRS9H4Sm81FDaqu5eMqB507DpvGic7c53AdFD0T91m9WnqK3a4vewXED91qX5YYeg6akRK4Lvq1zCaDbprAVeciau8ks/132',
'nickname':'raddyfiy',
'openid':'ofrYt1HiN7W3lscynLOPLjebqFAU'}

headers={
'Referer': 'www.cnvd.org.cn',
"Pragma": "no-cache",
"Cache-Control": "no-cache",
"DNT": "1",
'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}



def weichat(url,file): #获取微信公众号。从微信抓太麻烦，所以改抓二手搬运网站“今天看啥”。。。
    
    logfile=open(file,'a+')  
    logfile.seek(0)  
    log=str(logfile.read())

    responsetxt=requests.get(url,headers=headers).text
    soup = BeautifulSoup(responsetxt, 'html.parser')
    for j in soup.find_all(name='span',attrs={"class":"item_title"}):
        k=j.find(name='a')
        if k.string in log:
            break
        print(k.string)
        print(str(k['href']))
        logfile.write(k.string+'\n')
    logfile.write(date+'\n')
    logfile.close()

def get2(): #另一个二手网站，暂时用不到
    logfile=open("./kanxuelog.txt",'a+')  
    logfile.seek(0)  
    log=str(logfile.read())

    url='https://www.vreadtech.com/hh.php?id=ikanxue'
    responsetxt=requests.get(url,headers=headers,cookies=cookies).text
    soup = BeautifulSoup(responsetxt, 'html.parser')
    #link=str(re.findall(r"^iac-tit[\w]+2019$",responsetxt))
    for k in soup.find_all(name='a',attrs={"class":"iac-tit"}):
        if k.string in log:
            break
        print(k.string)
        print(str(k['href'])+'\n')
        logfile.write(k.string+'\n')
    logfile.write(date+'\n')
    logfile.close()

def daily():
        #只找最近一天的推送
    url='https://www.anquanke.com/tag/%E6%AF%8F%E6%97%A5%E5%AE%89%E5%85%A8%E7%83%AD%E7%82%B9'
    responsetxt=requests.get(url,headers=headers).text
    soup = BeautifulSoup(responsetxt, 'html.parser')
    today=soup.find(attrs={"class":"article-item common-item"})
    url=today.find_next('a')['href']
    url='https://www.anquanke.com'+url
    #print(url)
    responsetxt=requests.get(url,headers=headers,cookies=cookies).text
    soup = BeautifulSoup(responsetxt, 'html.parser')
    for k in soup.find_all(name='div',attrs={"class":"block-content"}):
        for title in k.find_all(attrs={"class":"report-title"}): #每个block是个子分类，里面有多篇文章，挨个抓
            link=title.find_next('a')#找文章标题下面最近的链接，不然容易错位
            print(title.string)
            print(link['href'])

def anquanke(url,file):
    logfile=open(file,'a+')  
    logfile.seek(0)  
    log=str(logfile.read())

    responsetxt=requests.get(url,headers=headers).text
    soup = BeautifulSoup(responsetxt, 'html.parser')
    for article in soup.find_all(attrs={"class":"info-content"}):
        title=article.find('a')
        if title.string in log:
            break
        print(title.string)
        print('https://www.anquanke.com'+title['href'])
        logfile.write(title.string+'\n')
    logfile.write(date+'\n')
    logfile.close()

def xctfmatchs(file): #从攻防世界抓取xctf赛事
    logfile=open(file,'a+')  
    logfile.seek(0)  
    log=str(logfile.read())
    url='https://adworld.xctf.org.cn/api/evts/list?limit=4&offset=0' #抓Ajax请求页
    responsetxt=requests.get(url,headers=headers).text
    responsejson=json.loads(responsetxt) #将得到的json解析，后面逐步分离json
    for match in responsejson['rows']:
        if match['name_zh'] in log:
            break
        print(match['name_zh'])
        #print(match['start_time'][:10]+'至'+match['end_time'][:10])
        print('https://adworld.xctf.org.cn/competition/detail?id&hash='+match['hash'])
        logfile.write(match['name_zh']+'\n')
    logfile.write(date+'\n')
    logfile.close()

def cnvd():     #待续，这个是前端生成token，慢慢研究
    logfile=open("cnvvdnews.txt","a+")
    logfile.seek(0) 
    log=str(logfile.read())
    cookies={"__jsluid_s":"3734af27db6f0557f1a0e9336baa4997",
    "JSESSIONID":"FFD56ADFD60B43468A88B054856C8A4C",
    "__jsl_clearance":"1563288909.617|0|SO4zmhAnyLl%2FJ%2BRo79OEco5Qe3s%3D"}
    url="https://www.cnvd.org.cn/webinfo/list?type=2"
    web=requests.session()
    responsetxt=web.get(url,headers=headers,cookies=cookies).text
    print(responsetxt)

    soup = BeautifulSoup(responsetxt, 'html.parser')

    for k in soup.find_all('tr'):
        news=k.find('a')
        print(news.string)

    logfile.close()
    




print("安全聚合"+date[:10])
print("吾爱/看雪公众号文章")
weichat("http://www.jintiankansha.me/column/pzkWRd2WNI","wuailog.txt")     #抓吾爱公众号，并记录进度
weichat("http://www.jintiankansha.me/column/4G0kim9xmc","kanxuelog.txt")       #抓看雪公众号，并记录进度
print('安全客每日安全热点')
daily()    #抓安全客的每日安全热点
print('活动')
anquanke('https://www.anquanke.com/tag/%E6%B4%BB%E5%8A%A8','huodong.txt')
print('xctf赛事')
xctfmatchs('xctfmatchs.txt')




