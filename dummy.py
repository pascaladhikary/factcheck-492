import json
import praw
from os import environ
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

from rake_nltk import Rake


reddit = praw.Reddit(
    client_id="",
    client_secret="",
    password="",
    user_agent="",
    username="",
)

def submit_sample_post(text):
    subreddit = reddit.subreddit("testingground4bots")

    title = "[FACT CHECK CLAIM TEST]"
    body = text
    subreddit.submit(title, selftext=body)

    print("Post submitted successfully!")

def main():
    sample = "Did you guys hear this? Elon Musk thinks the Earth is flat!"
    submit_sample_post(sample)


if __name__ == "__main__":
    main()

