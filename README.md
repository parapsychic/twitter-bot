# twitter-bot
A simple twitter bot that retweets

1. Create a file called keys.json with consumer_key, consumer_secret, access_token, access_secret and bearer_token
2. Create Blocked_Users.txt with ids of users to block/not retweet. IDs are twitter IDs and not usernames. Fetch id using tweepy Client.get_user(username='johndoe')
3. Create Queries.txt with search queries/hashtags to retweet. One keyword on each line.
4. All logging will be done into log.txt
