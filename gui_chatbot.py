import urllib

import nltk
import pyttsx3
import speech_recognition as sr
import pyaudio
from googlesearch import search
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model

model = load_model('chatbot_model.h5')
import json
import random

intents = json.loads(open('test.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

engine = pyttsx3.init()
r = sr.Recognizer()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.say('Hello World')
engine.runAndWait()

def speak_text(command):
    engine.say(command)
    engine.runAndWait()


def clean_up_sentence(sentence):
    # tokenize the pattern - splitting words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stemming every word - reducing to base form
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for words that exist in sentence
def bag_of_words(sentence, words, show_details=True):
    # tokenizing patterns
    sentence_words = clean_up_sentence(sentence)
    # bag of words - vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, word in enumerate(words):
            if word == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % word)
    return (np.array(bag))


def predict_class(sentence):
    # filter below  threshold predictions
    p = bag_of_words(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sorting strength probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json, sentance):
    global result
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if (i['tag'] == tag):
            if tag == 'getTime':
                result1 = random.choice(i['responses']), getTime()
                result = convertTuple(result1)
            elif tag == 'getDate':
                result1 = random.choice(i['responses']), getDate()
                result = convertTuple(result1)
            elif tag == 'square':
                result = square()
            elif tag == 'circle':
                result = circle()
            elif tag == 'triangle':
                result = triangle()
            # elif tag == 'search':
            #     research(sentance)
            #     result = " "
            else:
                result = random.choice(i['responses'])
            break
    return result


# def research(searchTitle):
#     search_queries = ["search", "check", "check out", "research"]
#     for query in search_queries:
#         if query in searchTitle:
#             searchTitle.replace(query, "", 1)
#
#     sites = ['nothing']
#     num = 0
#     for site in search(searchTitle, tld='com', lang='en', num=5, start=0, stop=5, pause=2.0):
#         num += 1
#         ChatBox.insert(END, "Bot: " + str(num) + ": " + site + '\n\n')
#         # speak_text(str(num) + site)
#         ChatBox.yview(END)
#         sites.insert(num, site)
#
#     speak_text("Which number site would you like to enter?")
#     MyText = ''
#     while MyText == '':
#         try:
#             with sr.Microphone() as source2:
#                 r.adjust_for_ambient_noise(source2, duration=0.05)
#                 audio2 = r.listen(source2)
#                 MyText = r.recognize_google(audio2)
#
#         except sr.RequestError as e:
#             print("Could not request results; {0}".format(e))
#
#         except sr.UnknownValueError:
#             print("unknown error occured")
#
#     if "one" in MyText or "first" in MyText:
#         f = urllib.request.urlopen(sites[1])
#         my_file = f.read()
#         print(my_file)



def getTime():
    from datetime import datetime
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def getDate():
    from datetime import datetime
    today = datetime.today()
    thisDay = today.strftime("%B %d, %Y")
    return thisDay


def square():
    return "\n******\n******\n******\n******\n******\n******"


def circle():
    return "\n     **\n" \
           "   *    *\n" \
           " *        *\n" \
           "*          *\n" \
           " *        *\n" \
           "   *    *\n" \
           "     **"


def triangle():
    return "\n   *   \n  ***  \n ***** \n*******"


def convertTuple(tup):
    str = ''.join(tup)
    return str


# Creating tkinter GUI
import tkinter
from tkinter import *


def send():
    MyText = ''
    while MyText == '':
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration = 0.05)
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occured")

    # msg = EntryBox.get("1.0", 'end-1c').strip()
    # EntryBox.delete("0.0", END)

    ChatBox.config(state=NORMAL)
    ChatBox.insert(END, "You: " + MyText + '\n\n')
    ChatBox.config(foreground="#446665", font=("Verdana", 12))

    ints = predict_class(MyText)
    res = getResponse(ints, intents, MyText)

    ChatBox.insert(END, "Bot: " + res + '\n\n')
    speak_text(res)

    ChatBox.config(state=DISABLED)
    ChatBox.yview(END)


root = Tk()
root.title("Chatbot")
root.geometry("400x500")
root.resizable(width=FALSE, height=FALSE)

# Create Chat window
ChatBox = Text(root, bd=0, bg="white", height="8", width="50", font="Arial", )

ChatBox.config(state=DISABLED)

# Bind scrollbar to Chat window
scrollbar = Scrollbar(root, command=ChatBox.yview, cursor="heart")
ChatBox['yscrollcommand'] = scrollbar.set

# Create Button to send message
SendButton = Button(root, font=("Verdana", 12, 'bold'), text="Activate                       ", width="50", height=5,
                    bd=0, bg="#f9a602", activebackground="#3c9d9b", fg='#000000',
                    command=send)

# Create the box to enter message
# EntryBox = Text(root, bd=0, bg="white", width="29", height="5", font="Arial")
# EntryBox.bind("<Return>", send)


# Place all components on the screen
scrollbar.place(x=376, y=6, height=386)
ChatBox.place(x=6, y=6, height=386, width=370)
# EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)

root.mainloop()
