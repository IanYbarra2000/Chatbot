import pickle
import nltk
import random
from nltk import word_tokenize
from nltk import WordNetLemmatizer
#from chatterbot import ChatBot
#from chatterbot.conversation import Statement
#from chatterbot.trainers import ListTrainer
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

#TO DO:
#-Store more personal information than name
#-Think of how to incorporate that info into responses
#-Incorporate more of the NLP techniques learned in class
#-expand knowledge base by a lot
#-Probably want to polish the word detection stuff but not quite sure how yet

UserInfo = dict()
print("Brando: What is your name?")
name = input("You: ")
try:
    UserInfo = pickle.load(open('Users/'+name+'.p','rb'))
    print("Brando: Welcome back",name+".\nBrando: Please ask your questions.")
except:
    UserInfo['name'] = name

    pickle.dump(UserInfo,open('Users/'+name+'.p','wb'))

    print("Brando: Hello,",name+". I am Brando, a chatbot to assist with basic questions about the lore of the Cosmere.\nBrando: Please ask your questions.")

while(True):
    request = input(name+": ")

    #preprocessing
    tokens = nltk.word_tokenize(request.lower())
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(t) for t in tokens]


    keywords=[] 
    for x in lemmas:
        if(x in knowledge.keys()):
            keywords.append(x)
    if(len(keywords)!=0):
        for x in keywords:
            print("Brando:",knowledge[x][random.randint(0,len(knowledge[x])-1)])
    else:
        print("Brando:","I don't know what you mean")
