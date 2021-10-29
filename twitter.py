### TO DO ###
# [ ] Day specific retweet routine
# [ ] Adding user to blocklist by username and then converting to id and storing it in blocked users
# [ ] Front end


import tweepy
import time
import random
from datetime import datetime
import json

### CONSTANTS ###
#in minutes
timeDelay = 10
timeDelay = timeDelay * 60


### FILES AND LOGS ###
blockList='Blocked_Users.txt'
queries='Queries.txt'
logfile="log.txt"
keyfile="keys.json"


### AUTHENTICATION ###
with open(keyfile, "r") as key:
    keys = json.load(key)

consumer_key = keys["consumer_key"]
consumer_secret = keys["consumer_secret"]
access_token = keys["access_token"]
access_token_secret = keys["access_token_secret"]
bearer_token = keys["bearer_token"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
client = tweepy.Client(bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)

### LOGGING ###
def log(toLog):
    if toLog is not str:
        str(toLog)
    print("logging " + toLog )
    logger = open(logfile, "a")
    currentTime = str(datetime.now().time()) # time object
    logger.write( toLog + " : " + currentTime + "\n" )
    logger.close()

log("Process Started: ")

### BLOCKING LOGIC ###
with open(blockList) as file:
    blockedUsers = file.readlines()
    blockedUsers = [line.rstrip() for line in blockedUsers]

#true if blocked
def checkBlock(author):
    for id in blockedUsers:
        id=int(id)
        
        if id == author:
            log("Blocked User: " + client.get_user(id=id).data.username)
            return True
    return False


def isBlockedUser(tweet):
    
    author = tweet.author_id

    if tweet.referenced_tweets is None:
        print("not RT")
    else:
        refTweet = client.get_tweet(id=tweet.referenced_tweets[0].id, expansions='author_id')[0]
        refAuthor = refTweet.author_id
        if checkBlock(refAuthor):
            return(True)


    return checkBlock(author)


### SEARCHING LOGIC ###
#Convert Hashtags files to a list
with open(queries) as file:
    searches = file.readlines()
    searches = [line.rstrip() for line in searches]

while(True):
    #Select the hashtag to search from list
    selectQ=random.randrange(0,len(searches))
    query = searches[selectQ]

    #do the search
    tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'],expansions='referenced_tweets.id.author_id', max_results=10)
    
    #select one tweet to retweet
    randomNumber=random.randint(0,9)
    tweet=tweets.data[randomNumber]

    #see if it's blocked, if not retweet
    if not isBlockedUser(tweet):
        log("Retweeted from:" + client.get_user(id=tweet.author_id).data.username + " Tweet id: " + str(tweet.id))
        client.retweet(tweet.id)
    #if blocked, return to While
    else: 
        continue
    
    #if retweeted, sleep for delay
    time.sleep(timeDelay)
    


        
