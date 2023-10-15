import random
import string
import os

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Tokenizacion del corpus
sent_tokens = None
word_tokens = None
lemmer = None

def LoadEngine():
    # Definicion del corpus
    f = open(
        os.getcwd()+'\corpus.txt',
        'r', errors='ignore')
    raw = f.read()
    raw = raw.lower()

    # Tokenizacion del corpus
    global sent_tokens
    global word_tokens
    global lemmer
    sent_tokens = sent_tokenize(raw)
    word_tokens = word_tokenize(raw)
    lemmer = WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(word_tokenize(text.lower().translate(remove_punct_dict)))

# Evaluar similitud Corpus - msg
def response(user_msg):
    chatbot_response = ''
    sent_tokens.append(user_msg)
    TfidfVec = TfidfVectorizer(
        tokenizer=LemNormalize,
        stop_words=stopwords.words('spanish')
        )
    tfid = TfidfVec.fit_transform(sent_tokens)
    
    vals = cosine_similarity(tfid[-1], tfid)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfid = flat[-2]
    
    if req_tfid == 0:
        chatbot_response = chatbot_response + 'Lo siento. No te he entendido'
    else:
        chatbot_response = chatbot_response + sent_tokens[idx]
        
        
    sent_tokens.remove(user_msg)
        
    return chatbot_response


# Procesamiento de Saludos
SALUDOS_INPUTS = ('hola', 'buenas', 'saludos',
                  'que tal', 'hey', 'buenos días')
SALUDOS_OUTPUTS = ['Hola', 'Hola, ¿Qué tal?', 'Hola, ¿Cómo te puedo ayudar?',
                   'Hola, encantado de hablar contigo']

def saludos(sentence):   
    for word in sent_tokenize(sentence.lower().translate(remove_punct_dict)):
        if word.lower() in SALUDOS_INPUTS:
            return random.choice(SALUDOS_OUTPUTS)
    for word in sentence.split():
        if word.lower() in SALUDOS_INPUTS:
            return random.choice(SALUDOS_OUTPUTS)
        
# Procesamiento de Agradecientos
THANKS_INPUTS = ('gracias', 'muchas gracias', 'agradecido')

def thanks(sentence):    
    for word in sent_tokenize(sentence.lower().translate(remove_punct_dict)):
        if word.lower() in THANKS_INPUTS:
            return 'No hay de que.' 
        
    for word in sentence.split():
        if word.lower() in THANKS_INPUTS:
            return 'No hay de que.' 