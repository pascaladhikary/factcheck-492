import json
import praw
from os import environ
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

from rake_nltk import Rake


reddit = praw.Reddit(
    client_id="wI-pXr1QHXxV6YOosAUNkQ",
    client_secret="eeDdlXIEEagpH-J51_WsivXEXS8bFA",
    password="factobot492",
    user_agent="facotbot by u/factobot-492",
    username="factobot-492",
)



subreddit = reddit.subreddit("PoliticalDiscussion")
is_rules = True

test_query = ''
for submission in subreddit.hot(limit=3):
    if is_rules:
        is_rules = False
        continue
    # print("Title: ", submission.title)
    # print("Text: ", submission.selftext)
    # print("Score: ", submission.score)
    # print("---------------------------------\n")

    test_query = submission.selftext

print(test_query)

text = test_query

# extract keywords
r = Rake()
r.extract_keywords_from_text(text)
result = r.get_ranked_phrases()

# print keywords
api_key = os.environ['API_KEY']


for r in result:
    user_query = r

    factCheckService = build("factchecktools", "v1alpha1", developerKey=api_key)
    request = factCheckService.claims().search(query=user_query)
    response = request.execute()
    if response:
        # break
        print(user_query)
        # print(response)
        for claim in response['claims']:
            print('text', claim['text'])
            for cr in claim['claimReview']:
                print(cr['textualRating'])
            # print('claimreview \n', claim['claimReview'][0]['textualRating'])
            # print(['title'])

            # stretch goal: check for claim similarity and only output the best one
            break
        break


