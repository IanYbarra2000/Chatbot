import pickle
import random
import nltk
import sys
from nltk.util import ngrams
from nltk import word_tokenize
from nltk import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def searchOnMiss(tkn):
    """This function is called when a match to a specific keyword cannot be found and uses cosine similarity on a tfidf vector to suggest a possible match

    Args:
        tkn ([string]): tokens taken from the user input
    """

    cosine = dict()

    reqVocab = set(tkn)
    vocabDict = dict()

    tfidfV=TfidfVectorizer()
    txt=' '.join(tkn)

    for x in knowledge.keys():
        ktxt = ' '.join(knowledge[x])
        vm = tfidfV.fit_transform([txt,ktxt])
        csm = cosine_similarity(vm)
        cosine[x] = csm[0,1]
    max = 0
    maxI = None
    for x in cosine.keys():
        if(cosine[x]>max and x not in UserInfo['history'].keys()):
            max=cosine[x]
            maxI=x
    print("I'm not exactly sure what you mean. Were you refering to",maxI+"?")
    YoN = input(name+": ")
    if(yesOrNo(YoN)):
        updateHistory(maxI)
    
    

def processRequest(req):
    """Takes the user's input(or request) and returns tokens and lemmas from said text input

    Args:
        req (string): the user's input

    Returns:
        ([string],[string]): a tuple containing the tokens and lemmas
    """
    tokens = nltk.word_tokenize(req.lower())
    
    ####
    stopWords = set(stopwords.words('english'))
    tokens = [t for t in tokens if not t in stopWords]
    ####
    lemmatizer = WordNetLemmatizer()
    lems = [lemmatizer.lemmatize(t) for t in tokens]
    return (lems,tokens)
def matchPhrase(tkn):
    """can get a partial match on an input or match based on multiple words

    Args:
        tkn ([string]): tokens taken from the user input

    Returns:
        [string]: the key of that is found to match the input
    """

    #tries to find match three times
    #starts with trying to match trigrams as to avoid returning a partial match incorrectly
    #requirements to match get less demanding with each set of for loops
    trigram = list(ngrams(tkn,3))
    for k in knowledge.keys():
        t = nltk.word_tokenize(k.lower())
        stopWords = set(stopwords.words('english'))#
        t = [s for s in t if not s in stopWords]#
        ktrigram = list(ngrams(t,3))
        for kb in ktrigram:
            if(kb in trigram):
                return k
    bigram = list(ngrams(tkn,2))
    for k in knowledge.keys():
        t = nltk.word_tokenize(k.lower())
        stopWords = set(stopwords.words('english'))#
        t = [s for s in t if not s in stopWords]#
        kbigram = list(ngrams(t,2))
        for kb in kbigram:
            if(kb in bigram):
                return k
    for k in knowledge.keys():
        #print(k)
        t = nltk.word_tokenize(k.lower())
        stopWords = set(stopwords.words('english'))#
        t = [s for s in t if not s in stopWords]#
        for kt in t:
            if(kt in tkn):
                #print(kt,'in',tkn)
                return k
    
    return None
def end():
    print("Brando: Thanks for using the chatbot. Goodbye, "+name+".")
    sys.exit()
def yesOrNo(txt):
    """processes yes or no responses

    Args:
        txt (string): user input

    Returns:
        boolean: returns true if answer is determined to be yes and no if not
    """
    proc = nltk.word_tokenize(txt)
    y = ['yes','sure','okay','yeah','absolutely','indeed','ya','yup','yep','totally','alright','certainly','definitely','gladly','indubitably','undoubtedly']
    for w in proc:
        if(w in y):
            return True
    return False

def updateHistory(kToUpdate):
    """updates the user's history in the user.p file and retrieves relevant information from the knowledge base

    Args:
        kToUpdate (string): the key that will be used to access information in the knowledge base and that will be entered into the user history
    """

    try:
        callNum=0
        if(kToUpdate in UserInfo['history'].keys()):
            callNum = UserInfo['history'][kToUpdate]+1
            UserInfo['history'][kToUpdate] = callNum

            if(callNum>len(knowledge[kToUpdate])-1): #If a specific keyword has been called more times than the number responses available it cycles back to the beginning while still maintaining a record of the count
                callNum=callNum%len(knowledge[kToUpdate])
            print("Brando: You've already asked about",kToUpdate+". I will tell you something else about it if I can.")
            print("Brando:",knowledge[kToUpdate][callNum])
        else:
            UserInfo['history'][kToUpdate]=0
            print("Brando:",knowledge[kToUpdate][0])
    except Exception as e:
         #stores history as a dictionary in with the keyword as the key and the number of times it has been asked about as the value
        UserInfo['history'] = dict()
        UserInfo['history'][kToUpdate] = 0

        print("Brando:",knowledge[kToUpdate][0])
    pickle.dump(UserInfo,open('Users/'+name+'.p','wb'))

    print("Brando: Would you like more information on",kToUpdate+"?")
    YoN = input(name+": ")
    if(yesOrNo(YoN)):
        updateHistory(kToUpdate)
def getExamples():
    """gives five random keys from the knowledge base to show the users examples of searches they can perform

    Returns:
        [string]: list of examples
    """
    ex = set()
    index=0
    keyArr = list(knowledge.keys())
    while(len(ex)<=5):
        index = random.randint(0,len(keyArr)-1)
        ex.add(keyArr[index])
    return list(ex)

def synsetMatching(lemma):
    """determines which topic category the user wants to ask about

    Args:
        lemma ([string]): the lemmas from the user's input

    Returns:
        string: the tag corresponding to the topic category
    """

    loc = ['location','place','city','country','land','nation','world','planet','site','metropolis','state','area','someplace']
    char = ['character','person','someone','individual','people']
    cult = ['culture','civilisation','civilization']
    era = ['era','event','timeperiod','epoch','battle','timeperiods']
    mag = ['magic','sorcery','witchcraft','enchantment','conjuration','wizard','necromancy','bewitchment','magical','illusion','spell','investiture']
    obj = ['object','item','material','substance','ore','fabric','textile']
    life = ['species','creature','beast','fauna','specie','animal','lifeform','lifeforms']

    if(lemma in loc):
        return 'loc'
    elif(lemma in char):
        return 'char'
    elif(lemma in cult):
        return 'cult'
    elif(lemma in era):
        return 'era'
    elif(lemma in mag):
        return 'mag'
    elif(lemma in obj):
        return 'obj'
    elif(lemma in life):
        return 'life'
    return
    
def topicQuestion(tg):
    """processes questions about specific items once a topic has been selected

    Args:
        tg (string): the tag corresponding to the topic category
    """
    global knowledge
    knowledge = pickle.load(open('knowledge/'+tg+'_knowledgeBase.p','rb'))
    topic = None
    
    if(tag =='loc'):

        topic = 'location'
    elif(tag =='char'):
        topic = 'character'
    elif(tag =='cult'):
        topic = 'culture'
    elif(tag =='era'):
        topic = 'era or event'
    elif(tag =='mag'):
        topic = 'magic or investiture'
    elif(tag =='obj'):
        topic = 'object or material'
    elif(tag =='life'):
        topic = 'lifeform or creature'
    examples = getExamples()
    print("Brando: What",topic,"would you like to know about? (Ex: "+examples[0]+', '+examples[1]+', '+examples[2]+', '+examples[3]+', '+examples[4]+')')
    req = input(name+": ")
    lems = processRequest(req)
    tok = lems[1]
    lems = lems[0]
    #print(tok,lems)
    for x in lems:
        if(x =='exit' or x=='stop'):
            end()
        if(x in knowledge.keys()):
                keywords.append(x)
    if(len(keywords)!=0):
        for x in keywords:
            updateHistory(x)
    else:
        #print('match Phrase')
        key = matchPhrase(tok)
        if(key is not None):
            updateHistory(key)
        else:
            searchOnMiss(tok)
            #print("Brando:","I don't know what you mean")
    print("Brando: Would you like to ask another question about a",topic+"?")
    YoN = input(name+": ")
    if(yesOrNo(YoN)):
        topicQuestion(tg)

knowledge = dict()
#char_knowledge=pickle.load(open('char_knowledgeBase.p','rb'))
#loc_knowledge=pickle.load(open('loc_knowledgeBase.p','rb'))
#mag_knowledge=pickle.load(open('mag_knowledgeBase.p','rb'))
#life_knowledge=pickle.load(open('life_knowledgeBase.p','rb'))
#obj_knowledge=pickle.load(open('obj_knowledgeBase.p','rb'))
#era_knowledge=pickle.load(open('era_knowledgeBase.p','rb'))
#print(era_knowledge['Battle of Alta'])
#cult_knowledge=pickle.load(open('cult_knowledgeBase.p','rb'))
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
    print("Brando: Welcome back",name+".")
except:
    UserInfo['name'] = name

    pickle.dump(UserInfo,open('Users/'+name+'.p','wb'))

    print("Brando: Hello,",name+". I am Brando, a chatbot to assist with basic questions about the lore of the Cosmere.")


while(True):
    print("Brando: Please choose a topic area you are interested in learning more about. Said topic areas include characters, cultures, events or timeperiods, creatures or lifeforms, locations, magic, or objects and materials.")
    request = input(name+": ")

    #preprocessing
    lemmas = processRequest(request)
    token = lemmas[1]
    lemmas = lemmas[0]


    keywords=[]
    tag = None
    for x in lemmas:
        if(x =='exit' or x=='stop'):
            end()
        tag = synsetMatching(x)
        if(tag):
            break
    if(tag is None):
        print("Brando:","I don't know what you mean")
    else:
        topicQuestion(tag)
        