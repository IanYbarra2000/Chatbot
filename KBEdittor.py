import pickle
import requests
import nltk
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import re

char_knowledge = dict()
loc_knowledge = dict()
mag_knowledge = dict()
life_knowledge = dict()
obj_knowledge = dict()
era_knowledge = dict()
cult_knowledge = dict()

def scrapeLoc(url):


    pg = requests.get(url)
    strained = SoupStrainer(id='mw-content-text')
    full = BeautifulSoup(pg.content,'html.parser')
    s = BeautifulSoup(pg.content,'html.parser',parse_only=strained)

    title = full.find("h1").get_text()
    reg = re.compile('User:')
    if(reg.search(title) or title=='Template:Date'):
        return
    start_at = s.find(id="toc")
    if(start_at is not None):
        target = start_at.find_all_previous("p", limit=2)
    else:
        start_at=s.find(id='row-spoiler-notice')
        target = start_at.find_all_next("p",limit=2)
    text = ""
    reg = re.compile('This wiki can now have')
    for x in target:
        
        
        if(x.get_text()[0]=='“' or reg.search(x.get_text())):
            continue
        
        text +=x.get_text()
    text=' '.join(text.split())

    text = re.sub(r'[\d\[\]]+', '', text)
    sents = nltk.sent_tokenize(text)
    return (title,sents)

def scrapeChar(url):

    pg = requests.get(url)
    strained = SoupStrainer(id='mw-content-text')
    full = BeautifulSoup(pg.content,'html.parser')
    s = BeautifulSoup(pg.content,'html.parser',parse_only=strained)

    title = full.find("h1").get_text()
    start_at = s.find("blockquote")
    if(start_at is not None):
        target = start_at.find_all_next("p", limit=4)
    else:
        target = full.find_all("p",limit=4)
    text = ""
    reg = re.compile('This wiki can now have')
    for x in target:
        
        if(x.get_text()[0]=='“' or reg.search(x.get_text())):
            continue
        
        text +=x.get_text()
    text=' '.join(text.split())

    text = re.sub(r'[\d\[\]]+', '', text)
    sents = nltk.sent_tokenize(text)
    return (title,sents)

def scrape_links(url,type): 
    pg = requests.get(url)

    strained = SoupStrainer(id="mw-pages")
    s = BeautifulSoup(pg.content,'html.parser',parse_only=strained)
    for l in s.find_all('a'):
        if(l.get('href')!='None'):
            print("finished",l.get('href'))
            link = "https://coppermind.net"+l.get('href')
            if(type=='char'):
                text = scrapeChar(link)
                if(text and text[1]):
                    char_knowledge[text[0]]=text[1]
            if(type=='loc'):
                text = scrapeLoc(link)
                if(text and text[1]):
                    loc_knowledge[text[0]]=text[1]
            if(type=='mag'):
                text = scrapeLoc(link)
                if(text and text[1]):
                    mag_knowledge[text[0]]=text[1]
            if(type=='life'):
                text = scrapeLoc(link)
                if(text and text[1]):
                    life_knowledge[text[0]]=text[1]
            if(type=='obj'):
                text = scrapeLoc(link)
                if(text and text[1]):
                    obj_knowledge[text[0]]=text[1]
            if(type=='era'):
                text = scrapeLoc(link)
                if(text and text[1]):
                    era_knowledge[text[0]]=text[1]
            if(type=='cult'):
                text = scrapeLoc(link)
                if(text and text[1]):
                    cult_knowledge[text[0]]=text[1]
            

scrape_links('https://coppermind.net/wiki/Category:Characters','char')
scrape_links('https://coppermind.net/wiki/Category:Locations','loc')
scrape_links('https://coppermind.net/wiki/Category:Magic','mag')
scrape_links('https://coppermind.net/wiki/Category:Lifeforms','life')
scrape_links('https://coppermind.net/wiki/Category:Magical_entities','life')
scrape_links('https://coppermind.net/wiki/Category:Objects_and_Materials','obj')
scrape_links('https://coppermind.net/wiki/Category:Events_and_Eras','era')
scrape_links('https://coppermind.net/wiki/Category:Culture','cult')
pickle.dump(char_knowledge,open('knowledge/char_knowledgeBase.p','wb'))
pickle.dump(loc_knowledge,open('knowledge/loc_knowledgeBase.p','wb'))
pickle.dump(mag_knowledge,open('knowledge/mag_knowledgeBase.p','wb'))
pickle.dump(life_knowledge,open('knowledge/life_knowledgeBase.p','wb'))
pickle.dump(obj_knowledge,open('knowledge/obj_knowledgeBase.p','wb'))
pickle.dump(era_knowledge,open('knowledge/era_knowledgeBase.p','wb'))
pickle.dump(cult_knowledge,open('knowledge/cult_knowledgeBase.p','wb'))


