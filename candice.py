
# Importing Libraries
from newspaper import Article
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import numpy as np
import warnings
import pyttsx3 #pip install pyttsx3
import speech_recognition as sr #pip install speechRecognition
import datetime
import wikipedia #pip install wikipedia
import webbrowser


warnings.filterwarnings('ignore')

nltk.download('punkt', quiet = True)
nltk.download('wordnet', quiet = True)


# engine = pyttsx3.init('sapi5')
# voices = engine.getProperty('voices')
# # print(voices[1].id)
# engine.setProperty('voice', voices[0].id)
#
#
# def speak(audio):
#     engine.say(audio)
#     engine.runAndWait()
#
#
# def wishMe():
#     hour = int(datetime.datetime.now().hour)
#     if hour>=0 and hour<12:
#         speak("Good Morning!")
#
#     elif hour>=12 and hour<18:
#         speak("Good Afternoon!")
#
#     else:
#         speak("Good Evening!")
#
#     speak("Hello sir, I am Candice. If you want to know about me, just say introduce. To access through wikipedia, just say the topic and say wikipedia with it. To exit, just say bye")
#
#
# def takeCommand():
#     # It takes microphone input from the user and returns string output
#
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         r.pause_threshold = 1
#         audio = r.listen(source)
#
#     try:
#         print("Recognizing...")
#         query = r.recognize_google(audio, language='en-in')
#         print(f"User : {query}\n")
#
#     except Exception as e:
#         # print(e)
#         print("Say that again please...")
#         return "None"
#     return query


# article = Article("https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521")
# article.download()
# article.parse()
# article.nlp()
# corpus = article.text
# print(corpus)


f = open('CKD.txt', 'r', errors='ignore')
corpus = f.read()


text = corpus
sent_tokens = nltk.sent_tokenize(text)
# for i in sent_tokens:
#     print(i)


#Creating dictionary (key:value) pair to remove punctuations

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
# print(string.punctuation)
# print(remove_punct_dict)


#create a function to return a list of lemmatized lower case words after removing punctuations
def LemNormalize(text):
    return nltk.word_tokenize(text.lower().translate(remove_punct_dict))
# print(LemNormalize(text))


#Keyword Matching

#Greeting Inputs

GREETING_INPUTS = ["hi", "hello", "hola", "greetings", "wassup", "hey", "hiii", "hii", "hiiii", "hiiii", "sup", "what's up"]
GREETING_RESPONSE = ["Hey, hope you are fine", "Hello sir, Candice welcomes you",  "I am glad! You are talking to me"]
INTRO_INPUTS = ["introduce", "how can you hep me", "what can you do for me"]
INTRO_RESPONSE = "Hello sir, I am Candice. I am programmed to guide you about the Chronic Kidney Diseases in detail. I can also provide you with Wikipedia information about the topic. To get the wikipedia info about the topic, just add wikipedia to your input. Thank you!"
EXIT_INPUTS = ["bye", "ok bye", "byee", "byeee"]
EXIT_RESPONSE = "Good bye sir. It was nice talking to you. Have a nice day !"

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSE)

def Introduce(sentence):
    for word in sentence.split():
        if word.lower() in INTRO_INPUTS:
            return INTRO_RESPONSE

def Exit(sentence):
    for word in sentence.split():
        if word.lower() in EXIT_INPUTS:
            return EXIT_RESPONSE


def response(user_response):

    user_response = user_response.lower()
    # print(user_response)
    robo_response = ''

    sent_tokens.append(user_response)
    # print(sent_tokens)


    TfidfVec = TfidfVectorizer(tokenizer = LemNormalize, stop_words = 'english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    # print(tfidf)


    #Getting measure of similarity
    vals = cosine_similarity(tfidf[-1], tfidf)
    # print(vals)
    #getting index of most similar response
    idx = vals.argsort()[0][-2]
    #reducing dimensionality of vals
    flat = vals.flatten()
    #sort list in ascending order
    flat.sort()
    #get most similar score to user response
    score = flat[-2]
    # print(score)
    #if variable 'score' is 0, then there is no text similar to users response
    if(score == 0):
        robo_response = robo_response + "I apologize, I don't understand."
    else:
        robo_response = robo_response + sent_tokens[idx]
    # print(robo_response)


    sent_tokens.remove(user_response)
    return robo_response



def chat(user_response):
    flag = True
    while (flag == True):
        # query = takeCommand().lower()
        # query = input()
        # if 'wikipedia' in query:
        user_response = user_response.lower()
        if 'wikipedia' in user_response:
            # speak('Searching Wikipedia...')
            user_response = user_response.replace("wikipedia", "")
            results = wikipedia.summary(user_response, sentences=2)
            # speak("According to Wikipedia")
            # print("Candice : ", results)
            # speak(results)
            return "Wikipedia : " + results
        else:
            results = chatty(user_response)
            # print("Candice : ", results)
            # speak(results)

            if (results == EXIT_RESPONSE):
                flag = False
            return results

    # print("Candice : Hello, I am Candice. Enter 'bye' to exit.")
def chatty(user_response):
    if(Exit(user_response) == None):
        if(user_response == 'thanks' or user_response == 'thank you' or user_response == 'thankx'):
            print("Candice : You are Welcome. What more can I do for you?")
        elif(Introduce(user_response) != None):
            return(Introduce(user_response))
        else:

            if(greeting(user_response) != None):
                # print("Candice : " + greeting(user_response))
                return(greeting(user_response))
            else:
                # print("Candice : " + response(user_response))
                return (response(user_response))

    elif(Exit(user_response) != None):
        # print("Bye, it was good chatting with you. Have a nice day!")
        # print("Came to exit")
        return(Exit(user_response))



# if __name__ == "__main__":
#     wishMe()
#     flag = True
#     while(flag == True):
#         query = takeCommand().lower()
#         # query = input()
#         if 'wikipedia' in query:
#             speak('Searching Wikipedia...')
#             query = query.replace("wikipedia", "")
#             results = wikipedia.summary(query, sentences=2)
#             speak("According to Wikipedia")
#             print("Candice : ", results)
#             speak(results)
#         else:
#             results = chat(query)
#             print("Candice : ", results)
#             speak(results)
#             if(results == EXIT_RESPONSE):
#                 flag = False


























