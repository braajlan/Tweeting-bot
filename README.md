# Tweeting-bot
App used to choose from replies the tweet with the highest number of likes and publish it in https://twitter.com/poemBotAr

# pre-requirements:
1. make sure to fill the twitter API information:
bearer_token = ''
token_secret = ''
consumer_key = ''
consumer_secret = ''
#Don't delete the quote mark#

2. put the first tweet id in the tweetID.json
#needed one time only then all automated#

# running application:
step 1: launch the Tweeting request file via CLI
step 2: app search for the tweet id shown in tweetID.json file
step 3: app fetch the tweet id information in data.json file
step 4: app will make calculations per tweet in replies then make new tweet + store the new tweet id in tweetID.json
