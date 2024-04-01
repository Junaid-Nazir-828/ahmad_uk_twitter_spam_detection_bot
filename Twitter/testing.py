import requests
import json
import time
# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAAPEsgEAAAAALsttllHNoK4zJKOw9Kh99mvNhTs%3DRDvLiMPDo8sOb8U6rq1850v0BrAN1Nby7RFUL8KUetEOUKIBQr'

def create_url():
    # Replace with user ID below
    # user_id = 2244994945
    user_id = 1765744801788448768                
    return "https://api.twitter.com/2/users/{}/mentions".format(user_id)


def get_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at,conversation_id,text"}


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
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )

#     json_response = response.json()

#     # Extract next_token from the first page response
#     next_token = json_response.get("meta", {}).get("next_token")

#     # If there's a next_token, make request for the last page
#     if next_token:
#         params["pagination_token"] = next_token
#         response = requests.request("GET", url, auth=bearer_oauth, params=params)
#         print(response.status_code)
#         if response.status_code != 200:
#             raise Exception(
#                 "Request returned an error: {} {}".format(
#                     response.status_code, response.text
#                 )
#             )
        
#         json_response = response.json()

#     return json_response

# def connect_to_endpoint(url, params):
#     all_responses = []
#     next_token = None

#     while True:
#         if next_token:
#             params["pagination_token"] = next_token

#         response = requests.request("GET", url, auth=bearer_oauth, params=params)
#         print(response.status_code)
#         if response.status_code != 200:
#             raise Exception(
#                 "Request returned an error: {} {}".format(
#                     response.status_code, response.text
#                 )
#             )
        
#         json_response = response.json()        

#         with open("twitter_responses.json", "a") as file:
#             json.dump(json_response, file, indent=4)


#         # Check if there are more pages
#         if "meta" in json_response and "next_token" in json_response["meta"]:
#             next_token = json_response["meta"]["next_token"]
#             time.sleep(5)
#         else:
#             break

#     return all_responses


# def connect_to_endpoint(url, params):
#     response = requests.request("GET", url, auth=bearer_oauth, params=params)
#     print(response.status_code)
#     if response.status_code != 200:
#         raise Exception(
#             "Request returned an error: {} {}".format(
#                 response.status_code, response.text
#             )
#         )
#     return response.json()


def main():
    url = create_url()
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    print(json.dumps(json_response, indent=4, sort_keys=True))
    # with open("twitter_responses.json", "w") as file:
    #     json.dump(json_response, file, indent=4)

    # print("All responses have been saved to 'twitter_responses.json'.")

if __name__ == "__main__":
    main()
    