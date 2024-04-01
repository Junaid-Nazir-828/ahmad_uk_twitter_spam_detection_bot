# This file has the full flow of the bot that is 
# 1. Get all the mentions
# 2. Check last answered mention from twitter.json
# 3. Get the next mention data
# 4. Process the text and reply reply
# 5. Update since_id
from requests_oauthlib import OAuth1Session
import requests
from check_tweet import check_tweet
import json
import time
# import asyncio
import re
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAAPEsgEAAAAALsttllHNoK4zJKOw9Kh99mvNhTs%3DRDvLiMPDo8sOb8U6rq1850v0BrAN1Nby7RFUL8KUetEOUKIBQr'

# Function to read data from JSON file
def read_since_id(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        return data.get("since_id", "")  # Return since_id value or empty string if not found

# Function to write data to JSON file
def write_since_id(filename, since_id):
    data = {"since_id": since_id}
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def create_url():
    # Replace with user ID below
    user_id = 1765744801788448768
    return "https://api.twitter.com/2/users/{}/mentions".format(user_id)

def get_params(since_id):    
    return {"tweet.fields": "created_at","expansions":"referenced_tweets.id","since_id":since_id}

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserMentionsPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        print("Error While Connecting : {}".format(response.text))
        return None        
    return response.json()

def get_mentions(since_id):    
    url = create_url()
    params = get_params(since_id)
    json_response = connect_to_endpoint(url, params)
    print(json.dumps(json_response, indent=4, sort_keys=True))
    return json_response


def send_reply(in_reply_to_tweet_id,text):
    consumer_key = 'YNQM6gBV7U4ej11fD8DBQr6FZ'
    consumer_secret = 'JxwpYMUZ3oWAySaJCdzz7pdtcuXrRmq61PkAU5HvaTsW95NXbw'
    access_token = '1765744801788448768-vIs0lzuB8XAk0fDh1HotuoeKRLSVpq'
    access_token_secret = 'I353kfyuxQhrISs2ikeRrAwtTMqOQQG5p0BXhSRm5Sqop'

    payload = {"text": text,"reply": {"in_reply_to_tweet_id": in_reply_to_tweet_id}}

    # Make the request
    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
    )
    # Making the request
    response = oauth.post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )

    if response.status_code != 201:
        print("Could not reply or already replied to {}".format(in_reply_to_tweet_id))
    else:
        print("Replied to {}".format(in_reply_to_tweet_id))        
    write_since_id("twitter.json",in_reply_to_tweet_id)
    print("Updated since_id in json file")

def handle_json(json_response):
    # print(json_response)
    if json_response == None or json_response["meta"]["result_count"] == 0:
        print("No Recent Mentions Retrieved")
    else:        
        for i in json_response["data"]:
            if "referenced_tweets" in i:
                mentioned_tweet_id = i["id"]
                text = ''
                
                for j in json_response["includes"]["tweets"]:
                    if i["referenced_tweets"][0]["id"] in j["edit_history_tweet_ids"]:
                        text = j["text"]
                        break
                
                if text == '':
                    print("--- ---- ---")
                else:
                    pattern = r'https://t\.co/[a-zA-Z0-9]+'
                    # Replace matched links with an empty string
                    cleaned_text = re.sub(pattern, '', text)
                    result = check_tweet(cleaned_text)
                    send_reply(mentioned_tweet_id,result)
            else:
                print("No Parent tweet to {}".format(i["id"]))

def handle_full_twitter_flow():
    while True:
        since_id = read_since_id("twitter.json")
        mentions = get_mentions(since_id)
        handle_json(mentions)
        print("Going to sleep for 5 minutes")
        time.sleep(300)

# handle_full_twitter_flow()