import re
from twitter import *
import json
import requests

class jsonObj: #intialize json object
    def __init__(self,tweetID,text,numOfLikes,authorID,username):
        self.tweetID = tweetID
        self.text = text
        self.numOfLikes = numOfLikes
        self.authorID = authorID
        self.username = username

def writeTweetID(tweetID):
    data = tweetID
    with open('tweetID.json', 'w') as f:
        json.dump(data, f)

def readTweetID():
    with open('tweetID.json') as json_file:
        data = json.load(json_file)
        return data

bearer_token = ''
token_secret = ''
consumer_key = ''
consumer_secret = ''
# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
searchURL = "https://api.twitter.com/2/tweets/search/recent"
t = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(search_url, headers, params):
    response = requests.request("GET", search_url, headers=headers, params=params)
    print("\n\n")
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def getMaximumLikes(): #reads from json file
    max = -1
    maxObj = [] #contains the maximum tweet
    with open('data.json') as json_file:
        data = json.load(json_file)
        print(data)

    for p in data['data']:
        text = p['text']
        numOfLikes = p['public_metrics']['like_count']
        tweetID = p['id']
        authorID = p['author_id']

        if(numOfLikes >= max):
            max = numOfLikes
            maxObj = jsonObj(tweetID,text,numOfLikes,authorID,None)

    for p in data['includes']['users']:
        if(p['id'] == maxObj.authorID):
            maxObj.username = p['username']
            break
    print(f"{maxObj.tweetID}\n{maxObj.text}\n{maxObj.numOfLikes}\n{maxObj.authorID}\n{maxObj.username}\n")
    return maxObj

def makeJsonQuery(tweetID):
    queryURL = {'query':'to:poembotAR','tweet.fields':'public_metrics,author_id','since_id':f'{tweetID}','expansions':'referenced_tweets.id.author_id'}
    headers = create_headers(bearer_token)
    json1 = connect_to_endpoint(searchURL, headers, queryURL)
    with open('data.json', 'w') as f: #write into json
        json.dump(json1, f,indent=2)

def generateTweet(maxObj):
    maxObj = getMaximumLikes()
    x = re.sub(r'\@[^ ]*\ ', '', maxObj.text)
    y = f"\nتم النشر بواسطة @{maxObj.username}"
    z = f"{x}\n{y}"
    print(z)
    t.statuses.update(status= z, verify=False)
    TweetID = t.search.tweets(q=z)['statuses'][0]['id'] #get last tweet id
    writeTweetID(TweetID)

def main():
    print("newTweet:- "+ str(readTweetID()))
    if(readTweetID() != None):
        makeJsonQuery(readTweetID())
        max = getMaximumLikes()
        generateTweet(max)
if __name__ == "__main__":
   main()
