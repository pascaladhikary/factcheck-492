import json
import praw
from os import environ
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import nltk
import sklearn
from rake_nltk import Rake

# TODO: set bot account information
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    password="",
    user_agent="",
    username="",
)

def print_post(post):
    print("Title: ", post.title)
    print("Text: ", post.selftext)
    print("Score: ", post.score)
    print("---------------------------------\n")


def get_top_political_post():
    subreddit = reddit.subreddit("PoliticalDiscussion")
    is_rules = True

    for submission in subreddit.hot(limit=2):
        if is_rules:
            is_rules = False
            continue
        return submission

def get_posts(username):
    subreddit = reddit.subreddit("testingground4bots")
    user_posts = subreddit.search(f"author:{username}")

    return user_posts

def get_post(user_posts, post_title):
    for post in user_posts:
        if post.title == post_title:
            return post
        
def get_keywords(text):
    # extract keywords
    r = Rake()
    r.extract_keywords_from_text(text)
    result = r.get_ranked_phrases()
    return result

def comment(post, comment_text):
    post.reply(comment_text)
    print('commented successfully')

def get_mentions():
    # Retrieve all of your mentions
    mentions = reddit.inbox.mentions()
    # texts = []
    for mention in mentions:
        # Retrieve the post ID of the mention
        post_id = mention.parent_id.split("_")[1]
        
        # Print the post ID of the mention
        print(f"Mention on post ID {post_id}")
        post = reddit.submission(id=post_id)
        print(post.selftext)
        # texts.append((post.selftext, post))
        return post.selftext, post
    # return texts[-1]


def lexical_distance(query, claim):
    def preprocess(text):
        words = nltk.tokenize.word_tokenize(text.lower())
        words = [word for word in words if word not in nltk.corpus.stopwords.words('english')]
        lemmatizer = nltk.stem.WordNetLemmatizer()
        words = [lemmatizer.lemmatize(word) for word in words]
        return ' '.join(words)

    #query = "The quick brown fox jumps over the lazy dog"
    #claim = "bruh moment lol brown fox"
    paragraph1 = preprocess(query)
    paragraph2 = preprocess(claim)

    vectorizer = sklearn.feature_extraction.text.TfidfVectorizer()
    vectors = vectorizer.fit_transform([paragraph1, paragraph2])
    similarity = sklearn.metrics.pairwise.cosine_similarity(vectors[0], vectors[1])[0][0]
    return similarity


def get_best_claim(text):
    # TODO: set API key in environment
    # api_key = os.environ['API_KEY']
    # api_key = os.environ['API_KEY']
    resulted_claims = []
    key_phrases = get_keywords(text)

    
    claim_accuracy = {}

    for kps in key_phrases:
        kps_query = kps
        factCheckService = build("factchecktools", "v1alpha1", developerKey=api_key)
        request = factCheckService.claims().search(query=kps_query)
        response = request.execute()

        # If kps returns something from factcheck, handle
        if response:
            # print(kps_query)
            for claim in response['claims']:
                # print('text', claim['text'])
                for cr in claim['claimReview']:
                    # print(cr['textualRating'], 'hi')
                    claim_accuracy[claim['text']] = cr['textualRating']
                resulted_claims.append(claim['text'])
                break

    distances = []
    for claim in resulted_claims:
        distances.append((lexical_distance(text, claim), claim))

    distances.sort(key=lambda x: x[0], reverse = True)
    # distances.sort(key=lambda x: x[0])
    return(distances[0][1], distances[0][0], claim_accuracy[distances[0][1]])
    # print('Claim with minimized distance', distances[0][1], distances[0][0])
    # print(claim_accuracy)
        
def main():
    # username = "factobot-492"
    # posts = get_posts(username)
    # post = get_post(posts, 'test')
    # keywords = get_keywords(post.selftext)
    # # print(keywords)

    # top_post = get_top_political_post()
    # print_post(top_post)
    # keywords = get_keywords(top_post.selftext)
    # print(keywords)

    negative_textual_ratings = ['False', 'Altered', 'Partly False']

    text, post = get_mentions()
    claim, confidence, accuracy = get_best_claim(text)
    print(claim, confidence, accuracy)

    check = True
    if accuracy in negative_textual_ratings:
        check = False

    confidence = str(((1 - confidence) * 100))[:2]


    output = '''This claim is: {check}. I can say this with {confidence}% confidence. 
    \n \n 
    ---
    I am a primitive fact checking bot using the Google Fact Check API. \n 
    For more detailed fact-checking, please visit https://toolbox.google.com/factcheck/explorer/search/ \n
    Thank you for your patience as I learn and grow!'''.format(check=check, confidence = confidence)

    print(output)

    comment(post, output)
   
    # claim = "Claim with minimized distance Video shows Elon Musk admitting he is a flat earther 0.27519581217502304"
    # comment(post, "this is a comment")    
    # get_best_claim(text)




if __name__ == "__main__":
    main()


