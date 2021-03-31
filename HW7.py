import pickle
import nltk
from nltk.util import ngrams
import random
from nltk import word_tokenize
from nltk import WordNetLemmatizer
#from chatterbot import ChatBot
#from chatterbot.conversation import Statement
#from chatterbot.trainers import ListTrainer
def matchPhrase(tkn):
    for k in knowledge.keys():
        t = nltk.word_tokenize(k.lower())
        for kt in t:
            if(kt in tkn):
                return k
    bigram = list(ngrams(tkn,2))
    for k in knowledge.keys():
        t = nltk.word_tokenize(k.lower())
        kbigram = list(ngrams(t,2))
        for kb in kbigram:
            if(kb in bigram):
                return k
    return None

def updateHistory(kToUpdate):
    try:
        callNum=0
        if(kToUpdate in UserInfo['history'].keys()):
            callNum = UserInfo['history'][kToUpdate]+1
            UserInfo['history'][kToUpdate] = callNum

            if(callNum>len(knowledge[kToUpdate])-1): #If a specific keyword has been called more times than the number responses available it cycles back to the beginning while still maintaining a record of the count
                callNum=callNum%len(knowledge[kToUpdate])
            print("Brando: You've already asked about",kToUpdate+". I will tell you something else about it if I can.")
            print("Brando:",knowledge[kToUpdate][0][callNum])
        else:
            UserInfo['history'][kToUpdate]=0
            print("Brando:",knowledge[kToUpdate][0][0])
    except Exception as e:
         #stores history as a dictionary in with the keyword as the key and the number of times it has been asked about as the value
        UserInfo['history'] = dict()
        UserInfo['history'][kToUpdate] = 0

        print("Brando:",knowledge[kToUpdate][0][0])
    pickle.dump(UserInfo,open('Users/'+name+'.p','wb'))




knowledge = pickle.load(open('t_knowledgeBase.p','rb'))
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
            updateHistory(x)
    else:
        key = matchPhrase(tokens)
        if(key is not None):
            updateHistory(key)
        else:
            print("Brando:","I don't know what you mean")


