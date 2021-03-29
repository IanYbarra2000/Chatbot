import pickle
import nltk
import random
from nltk import word_tokenize
from nltk import WordNetLemmatizer
from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ListTrainer
knowledge = pickle.load(open('knowledgeBase.p','rb'))
if(False):

    bot = ChatBot('Norman')

    trainer = ListTrainer(bot)

    #trainer.train("chatterbot.corpus.english")

    knowledge = pickle.load(open('knowledgeBase.p','rb'))
    print(knowledge)
    for topic in knowledge:
        for r in topic:
            trainer.train([topic,r])

    #request = 'Hello'
    while(True):
        request = Statement(input('You: '))
        response = bot.get_response(request)
        print('bot: ',response)

while(True):
    request = input("You: ")
    tokens = nltk.word_tokenize(request.lower())
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(t) for t in tokens]
    print(lemmas)
    keywords=[] 
    for x in lemmas:
        if(x in knowledge.keys()):
            keywords.append(x)
    if(len(keywords)!=0):
        for x in keywords:
            print(knowledge[x][random.randint(0,len(knowledge[x]))])
    else:
        print("I don't know what you mean")