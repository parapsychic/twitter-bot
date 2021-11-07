### TO DO ###
# [x] Day specific retweet routine
# [ ] Adding user to blocklist by username and then converting to id and storing it in blocked users
# [ ] Front end
# [ ] Like and follow routines


import tweepy
import time
import random
from datetime import datetime
import json
import _thread

### CONSTANTS ###
#in minutes
timeDelay = 10
timeDelay = timeDelay * 60


### FILES AND LOGS ###
blockList='Blocked_Users.txt'
queries='Queries.txt'
logfile="log.txt"
keyfile="keys.json"
day_specific_query_rules='day_specific_query_rules.json'

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
    currentTime = str(datetime.now()) # time object
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

def getAuthors(tweet):
    author = tweet.author_id
    return author

def isBlockedUser(author, refAuthor):
    if refAuthor is not None:
        if checkBlock(refAuthor):
            return(True)
    return checkBlock(author)

def followUser(author, refAuthor):
    coinflip = random.choice([True, False])
    log("Coin flipped : " + str(coinflip))
    
    if coinflip is True:
        if refAuthor is not None:
            client.follow(refAuthor)
            log("Followed user: " + client.get_user(id=refAuthor).data.username)
        client.follow(author)
        log("Followed user: " + client.get_user(id=author).data.username)

### SEARCHING LOGIC ###
#Convert Hashtags files to a list
with open(queries) as file:
    searches = file.readlines()
    searches = [line.rstrip() for line in searches]

def SelectSearchQuery():
    today = datetime.today()
    weekday = today.strftime("%a")
    log("Day: " + weekday)
    
    with open(day_specific_query_rules, "r") as queryrules:
        daySpecificQueryDict = json.load(queryrules)

    if weekday in daySpecificQueryDict:
        return daySpecificQueryDict[weekday]

    selectQ=random.randrange(0,len(searches))
    query = searches[selectQ]
    return query

def retweet():
    while(True):
        #Select the hashtag to search from list
        query = SelectSearchQuery() 
        log(query)
        #do the search
        tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'],expansions='referenced_tweets.id.author_id', max_results=10)
        
        #select one tweet to retweet
        randomNumber=random.randint(0,9)
        tweet=tweets.data[randomNumber]
    
        #find authors 
        author = getAuthors(tweet)
        if tweet.referenced_tweets is None:
            log("not RT")
            refAuthor=None
        else:
            refTweet = client.get_tweet(id=tweet.referenced_tweets[0].id, expansions='author_id')[0]
            refAuthor = refTweet.author_id
        
    
    
        #see if it's blocked, if not retweet
        if not isBlockedUser(author, refAuthor):
            log("Retweeted from:" + client.get_user(id=tweet.author_id).data.username + " Tweet id: " + str(tweet.id))
            client.retweet(tweet.id)
    
        #do a coin flip and follow user
            followUser(author, refAuthor)
        #if blocked, return to While
        else: 
            continue
        
        #if retweeted, sleep for delay
        time.sleep(timeDelay)
        
def like():
    while(True):
        #Select the hashtag to search from list
        query = SelectSearchQuery() 
        log(query)
        #do the search
        tweets = client.search_recent_tweets(query=query, tweet_fields=['context_annotations', 'created_at'],expansions='referenced_tweets.id.author_id', max_results=10)
        
        #select one tweet to retweet
        randomNumber=random.randint(0,9)
        tweet=tweets.data[randomNumber]
    
        #find authors 
        author = getAuthors(tweet)
        if tweet.referenced_tweets is None:
            log("not RT")
        else:
            refTweet = client.get_tweet(id=tweet.referenced_tweets[0].id, expansions='author_id')[0]
            refAuthor = refTweet.author_id
        
    
    
        #see if it's blocked, if not retweet
        if not isBlockedUser(author, refAuthor):
            log("Liked from:" + client.get_user(id=tweet.author_id).data.username + " Tweet id: " + str(tweet.id))
            client.like(tweet.id)
    
        #do a coin flip and follow user
            followUser(author, refAuthor)
        #if blocked, return to While
        else: 
            continue
        
        #if retweeted, sleep for delay
        time.sleep(timeDelay)
        
try:
    _thread.start_new_thread( retweet,() )
    _thread.start_new_thread( like,() )
except:
    log("Threads have failed")

while 1:
    pass
