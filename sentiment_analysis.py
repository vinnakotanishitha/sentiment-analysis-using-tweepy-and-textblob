#!/usr/bin/python

import sys,os
import tweepy
from textblob import TextBlob
from credentials import Consumer_Key, Consumer_Secret, Access_Token, Access_Token_Secret



class MyStreamListener(tweepy.StreamListener):

    counter = 0

    def on_status(self, status):
        if (int(self.counter) > int(num_tweets)):
            return False
        else:
            return True
        print(self.counter, '/', num_tweets,' --- ',status.text)
#        print(status.text)
        analysis = TextBlob(status.text)
        self.counter += 1
        print('========>positive' if analysis.sentiment.polarity > 0 else '========>neutral' if analysis.sentiment.polarity == 0 else '========>negative')

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False
#       print('========> polarity = ',analysis.sentiment.polarity)
#       print('========> subjectivity = ',analysis.sentiment.subjectivity)

choice = str(raw_input("Choices available: \n(1)From a document\n(2)From Twitter\nAnswer: "))
while(choice not in ("1","2")):
    choice = str(raw_input("Choices available: \n(1)From a document\n(2)From Twitter\nAnswer: "))
print("###################Starting#################")

def document():
    try:
        print("==>Opening Document")
        f = open("document.txt","r")
        #print(f.read())
        print("==>Starting analysis")
        analysis = TextBlob(f.read())
        for sentence in analysis.sentences:
            print(sentence)
            print('========>positive' if analysis.sentiment.polarity > 0 else '========>neutral' if analysis.sentiment.polarity == 0 else '========>negative')
    except:
        sys.stderr.write('Failed to open files.\n')

def twitter():
    try:
        auth = tweepy.OAuthHandler(Consumer_Key, Consumer_Secret)
        auth.set_access_token(Access_Token, Access_Token_Secret)
        api = tweepy.API(auth)
    except:
        sys.stderr.write('Authentication using tweepy failed.\n')

    target = raw_input("Enter the word to search twitter with: ")

    stream_choice = str(raw_input("Do you need a stream? -- yes/no:  ")).lower()
    while(stream_choice not in ("yes","no")):
        stream_choice = str(raw_input("Do you need a stream? -- yes/no:  ")).lower()

    if(stream_choice == "yes"):
        global num_tweets
        num_tweets = raw_input("Enter the number of tweets to be streamed ")
        print('######################',' Connecting Stream ','#########################')
        myStreamListener = MyStreamListener()
        myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
        print('Starting Stream')
        myStream.filter(track=[target])
        print('Passed stream filter')
        myStream.disconnect()
        print('######################',' disconnecting Stream ','#########################')
    else:
        tweets = api.search(target)
        for tweet in tweets:
            analysis = TextBlob(tweet.text)
            print(TextBlob(tweet.text))
            print('========>positive' if analysis.sentiment.polarity > 0 else '========>neutral' if analysis.sentiment.polarity == 0 else '========>negative')




def errorMsg():
    sys.stderr.write("Incorrect Input.\n")

#switcher = {'1': document, '2': twitter }
#switcher.get(choice,errorMsg)
#print("############# After switcher ######################")


if choice == "1":
    document()
elif choice == "2":
    twitter()
else:
    errorMsg()
print("################### Ending #########################")
