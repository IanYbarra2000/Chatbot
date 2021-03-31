import pickle
import requests
import nltk
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import re

knowledge = pickle.load(open('knowledgeBase.p','rb'))





def scrapeTxt(url):
    """takes list of URL's and writes the text from the associated websites to documents

    Args:
        URL_list (list[string]): list of URLs whose associated webpages are to be scraped
    """

    pg = requests.get(url)
    strained = SoupStrainer(id='mw-content-text')
    full = BeautifulSoup(pg.content,'html.parser')
    s = BeautifulSoup(pg.content,'html.parser',parse_only=strained)

    title = full.find("h1").get_text()
    start_at = s.find("blockquote")
    if(start_at is not None):
        target = start_at.find_all_next("p", limit=4)
    else:
        target = full.find_all("p",limit=2)
    text = ""
    for x in target:
        if(x.get_text()[0]=='“' or x.get_text()[0:16]=='This wiki can now'):
            continue
        
        text +=x.get_text()
    text=' '.join(text.split())

    text = re.sub(r'[\d\[\]]+', '', text)
    sents = nltk.sent_tokenize(text)
    return (title,sents)

def scrape_characters():
    url = 'https://coppermind.net/wiki/Category:Characters'
    pg = requests.get(url)

    strained = SoupStrainer(id="mw-pages")
    s = BeautifulSoup(pg.content,'html.parser',parse_only=strained)
    for l in s.find_all('a'):
        #print(l.get('href'))
        if(l.get('href')!='None'):
            print("finished",l.get('href'))
            link = "https://coppermind.net"+l.get('href')
            text = scrapeTxt(link)
            knowledge[text[0]]=(text[1],'character')
            

scrape_characters()
pickle.dump(knowledge,open('t_knowledgeBase.p','wb'))
