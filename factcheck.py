import json
import praw
from os import environ
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

api_key = os.environ['API_KEY']

user_query = "voter fraud 2020"

factCheckService = build("factchecktools", "v1alpha1", developerKey=api_key)
request = factCheckService.claims().search(query=user_query)
response = request.execute()
print(response)